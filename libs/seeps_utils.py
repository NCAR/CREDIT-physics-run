'''
xxx
'''

import numpy as np
import xarray as xr

import functools
import typing as t
import dataclasses
from typing import Callable, Optional, Union, Sequence


class SEEPSThreshold:
    """Compute SEEPS thresholds (heavy/light) and fraction of dry grid points using xarray only."""

    def __init__(self, dry_threshold_mm: float, var: str):
        # Convert mm to m
        self.dry_threshold_m = dry_threshold_mm / 1000.0
        self.var = var

    def compute(
        self,
        ds: xr.Dataset,
        dim: Union[str, Sequence[str]],
        weights: Optional[xr.DataArray] = None,
    ) -> xr.Dataset:
        ds_var = ds[self.var]

        # Identify dry conditions
        is_dry = ds_var < self.dry_threshold_m
        dry_fraction = is_dry.mean(dim=dim)

        # Select only non-dry values
        not_dry = ds_var.where(~is_dry)
        
        # Ensure the dimension(s) used for quantile are not chunked multiple times
        # If dim is a string, convert it to a list for uniform processing
        if isinstance(dim, str):
            dim_list = [dim]
        else:
            dim_list = list(dim)

        # Rechunk each dimension to have a single chunk along that dimension
        # This ensures quantile can be computed without errors
        chunking = {d: -1 for d in dim_list if d in not_dry.dims}
        if chunking:
            not_dry = not_dry.chunk(chunking)

        # Compute the two-thirds quantile for the heavy precipitation threshold
        if weights is not None:
            heavy_threshold = not_dry.weighted(weights).quantile(2/3, dim=dim_list)
        else:
            heavy_threshold = not_dry.quantile(2/3, dim=dim_list)

        # Create output dataset
        out = xr.Dataset(
            {
                f'{self.var}_seeps_threshold': heavy_threshold.drop_vars('quantile'),
                f'{self.var}_seeps_dry_fraction': dry_fraction,
            }
        )
        return out

@dataclasses.dataclass
class Region:
    """
    Region selector for spatially averaged metrics.
    .apply() method is called before spatial averaging in the Metrics classes.
    Region selection can be either applied as an operation on the dataset itself
    or a weights dataset, typically the latitude weights. The latter option is
    required to implement non-box regions without the use of .where() which would
    clash with skipna=False used as default in the metrics. The way this is
    implemented is by multiplying the input weights with a boolean weight dataset.
    
    Since sometimes the dataset and sometimes the weights are modified, these must
    be used together, most likely insice the _spatial_average function defined in
    metrics.py.
    """

    def apply(
      self, dataset: xr.Dataset, weights: xr.DataArray
    ) -> tuple[xr.Dataset, xr.DataArray]:
        
        """Apply region selection to dataset and/or weights.
        
        Args:
          dataset: Spatial metric, i.e. RMSE
          weights: Weights dataset, i.e. latitude weights
        
        Returns:
          dataset: Potentially modified (sliced) dataset.
          weights: Potentially modified weights data array, to be used in
          combination with dataset, e.g. in _spatial_average().
        """
        raise NotImplementedError

@dataclasses.dataclass
class Metric:
    """Base class for metrics."""

    def compute_chunk(
      self,
      forecast: xr.Dataset,
      truth: xr.Dataset,
      region: t.Optional[Region] = None,
      skipna: bool = False,
    ) -> xr.Dataset:
        
        """Evaluate this metric on a temporal chunk of data.
        
        The metric should be evaluated independently for each time (averaging over
        time is performed later, on multiple chunks). Thus `forecast` and `truth`
        chunks should cover the full spatial extent of the data, but not necessarily
        all times.
        
        Args:
          forecast: dataset of forecasts to evaluate.
          truth: dataset of ground truth. Should have the same variables as
            forecast.
          region: Region class. .apply() method is called inside before spatial
            averaging.
          skipna: Whether to skip NaN values in both forecasts and observations
            during evaluation.
        
        Returns:
          Dataset with metric results for each variable in forecasts/truth, without
          spatial dimensions (latitude/longitude).
        """
        raise NotImplementedError

    def compute(
      self,
      forecast: xr.Dataset,
      truth: xr.Dataset,
      region: t.Optional[Region] = None,
      skipna: bool = False,
    ) -> xr.Dataset:
        """Evaluate this metric on datasets with full temporal coverages."""
        if "time" in forecast.dims:
          avg_dim = "time"
        elif "init_time" in forecast.dims:
          avg_dim = "init_time"
        else:
          raise ValueError(
              f"Forecast has neither valid_time or init_time dimension {forecast}"
          )
        return self.compute_chunk(
            forecast, truth, region=region, skipna=skipna
        ).mean(
            avg_dim,
            skipna=skipna,
        )

class SpatialSEEPS(Metric):
    """Computes Stable Equitable Error in Probability Space.
    
    Definition in Rodwell et al. (2010):
    https://www.ecmwf.int/en/elibrary/76205-new-equitable-score-suitable-verifying-precipitation-nwp
    
    Attributes:
    climatology: climatology dataset containing seeps_threshold [meters] and
      seeps_dry_fraction [0-1] for given precip_name.
    dry_threshold_mm: Dry threhsold in mm, same as used to compute
      climatological values.
    precip_name: Name of precipitation variable, e.g. total_precipitation_24hr.
    min_p1: Mask out values with smaller average dry fraction.
    max_p1: Mask out values with larger average dry fraction.
    p1: Average dry fraction.
    """
    def __init__(
        self,
        climatology: xr.Dataset,
        dry_threshold_mm: float = 0.25,
        precip_name: str = "total_precipitation_24hr",
        min_p1: float = 0.1,
        max_p1: float = 0.85
    ):
        # Initialize the base Metric class without extra arguments
        super().__init__()

        self.climatology = climatology
        self.dry_threshold_mm = dry_threshold_mm
        self.precip_name = precip_name
        self.min_p1 = min_p1
        self.max_p1 = max_p1
        
    @functools.cached_property
    def p1(self) -> xr.DataArray:
        dry_fraction = self.climatology[f"{self.precip_name}_seeps_dry_fraction"]
        return dry_fraction.compute()

    def _convert_precip_to_seeps_cat(self, ds):
        """Helper function for SEEPS computation. Converts values to categories."""
        wet_threshold = self.climatology[f"{self.precip_name}_seeps_threshold"]
        # Convert to SI units [meters]
        dry_threshold = self.dry_threshold_mm / 1000.0
        da = ds[self.precip_name]
        wet_threshold_for_valid_time = wet_threshold.load()

        dry = da < dry_threshold
        light = np.logical_and(da > dry_threshold, da < wet_threshold_for_valid_time)
        heavy = da >= wet_threshold_for_valid_time
        result = xr.concat(
            [dry, light, heavy],
            dim=xr.DataArray(["dry", "light", "heavy"], dims=["seeps_cat"]),
        )
        
        # Convert NaNs back to NaNs
        result = result.astype("int").where(da.notnull())
        return result

    def compute_chunk(
        self,
        forecast: xr.Dataset,
        truth: xr.Dataset,
        region: t.Optional[Region] = None,
        skipna: bool = False,
    ) -> xr.Dataset:
        del skipna  # Ignored, must be effectively True because of p1 mask.
        forecast_cat = self._convert_precip_to_seeps_cat(forecast)
        truth_cat = self._convert_precip_to_seeps_cat(truth)

        # Compute contingency table
        out = (
            forecast_cat.rename({"seeps_cat": "forecast_cat"})
            * truth_cat.rename({"seeps_cat": "truth_cat"})
        ).compute()
        
        # Compute scoring matrix
        scoring_matrix = [
            [xr.zeros_like(self.p1), 1 / (1 - self.p1), 4 / (1 - self.p1)],
            [1 / self.p1, xr.zeros_like(self.p1), 3 / (1 - self.p1)],
            [
                1 / self.p1 + 3 / (2 + self.p1),
                3 / (2 + self.p1),
                xr.zeros_like(self.p1),
            ],
        ]
        das = []
        for mat in scoring_matrix:
          das.append(xr.concat(mat, dim=out.truth_cat))
        scoring_matrix = 0.5 * xr.concat(das, dim=out.forecast_cat)
        scoring_matrix = scoring_matrix.compute()
        
        # Take dot product
        result = xr.dot(out, scoring_matrix, dims=("forecast_cat", "truth_cat"))
        
        # Mask out p1 thresholds
        result = result.where(self.p1 < self.max_p1, np.nan)
        result = result.where(self.p1 > self.min_p1, np.nan)
        return xr.Dataset({f"{self.precip_name}": result})
