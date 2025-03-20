# Improving AI weather prediction models using global mass and energy conservation schemes

Yingkai Sha, John S. Schreck, William Chapman, David John Gagne II

NSF National Center for Atmospheric Research, Boulder, Colorado, USA

## Abstract

Artificial Intelligence (AI) weather prediction (AIWP) models are powerful tools for medium-range forecasts but often lack physical consistency, leading to outputs that violate conservation laws. This study introduces a set of novel physics-based schemes designed to enforce the conservation of global dry air mass, moisture budget, and total atmospheric energy in AIWP models. The schemes are highly modular, allowing for seamless integration into a wide range of AI model architectures. Forecast experiments are conducted to demonstrate the benefit of conservation schemes using FuXi, an example AIWP model, modified and adapted for 1.0-degree grid spacing. Verification results show that the conservation schemes can guide the model in producing forecasts that obey conservation laws. The forecast skills of upper-air and surface variables are also improved, with longer forecast lead times receiving larger benefits. Notably, large performance gains are found in the total precipitation forecasts, owing to the reduction of drizzle bias. The proposed conservation schemes establish a foundation for implementing other physics-based schemes in the future. They also provide a new way to integrate atmospheric domain knowledge into the design and refinement of AIWP models.

## Resources

* NSF NCAR Research Data Archive, [ERA5 Reanalysis (0.25 Degree Latitude-Longitude Grid)](https://rda.ucar.edu/datasets/d633000/)
  * Note: this repository visits RDA internally, e.g., `/glade/campaign/collections/rda/data/d633000/e5.oper.an.pl/197901/`

* Google Research, Analysis-Ready, Cloud Optimized (ARCO) ERA5 [[link](https://cloud.google.com/storage/docs/public-datasets/era5)]

* IFS-HRES and ERA5 climatology from the Weatherbench2 project [[link](https://weatherbench2.readthedocs.io/en/latest/data-guide.html)]

* NSF NCAR MILES Community Research Earth Digital Intelligence Twin (CREDIT) [[link](https://github.com/NCAR/miles-credit)]

## Navigation

* Derivations of conservation schemes: [mass conservation](https://github.com/yingkaisha/CREDIT-physics-run/blob/main/physics/DEV01_global_mass_conservation_plevel.ipynb), [energy conservation](https://github.com/yingkaisha/CREDIT-physics-run/blob/main/physics/DEV01_global_energy_conservation_plevel.ipynb), [Pytorch integration](https://github.com/yingkaisha/CREDIT-physics-run/blob/main/physics/DEV02_conservation_schemes_pytorch.ipynb)
* Results: [Dry air mass conservation](https://github.com/yingkaisha/CREDIT-physics-run/blob/main/visualization/FIG03_dry_air_conserve.ipynb), [Moisture budget conservation](https://github.com/yingkaisha/CREDIT-physics-run/blob/main/visualization/FIG04_water_conserve.ipynb), [Total atmospheric energy conservation](https://github.com/yingkaisha/CREDIT-physics-run/blob/main/visualization/FIG05_energy_conserve.ipynb), [SEEPS](https://github.com/yingkaisha/CREDIT-physics-run/blob/main/visualization/FIG11_SEEPS.ipynb)

## Model weights

| Model name | Weights | Notes |
|------------|---------|-------|
| FuXi-base  | [link](https://huggingface.co/yingkaisha/FuXi-plevel-1deg/tree/main/FuXi-base) | The 1.0 degree FuXi baseline without conservation schemes |
| FuXi-physics | [link](https://huggingface.co/yingkaisha/FuXi-plevel-1deg/tree/main/FuXi-physics) | The 1.0 degree FuXi run with conservation schemes |

## Citation

Sha, Y., J. Schreck, W. Chapman, D. J. Gagne II, 2025a: Improving AI weather prediction models using global mass and energy conservation schemes. In review: Journal of Advances in Modeling Earth Systems. Pre-print: https://arxiv.org/abs/2501.05648

```
@article{sha2025improving,
  title={Improving AI weather prediction models using global mass and energy conservation schemes},
  author={Sha, Yingkai and Schreck, John S and Chapman, William and Gagne II, David John},
  journal={arXiv preprint arXiv:2501.05648},
  year={2025}
}
```

