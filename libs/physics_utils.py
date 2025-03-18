'''
This script containts functions for the computation of physcis-based 
relationships using xarray.Dataset.
-------------------------------------------------------
Content:
    - grid_area
    - pressure_integral
    - weighted_sum

Yingkai Sha
ksha@ucar.edu
'''

import xarray as xr
import numpy as np

R = 6371000  # m
GRAVITY = 9.80665
RHO_WATER = 1000.0 # kg/m^3
RAD_EARTH = 6371000 # m
LH_WATER = 2.26e6  # J/kg
CP_DRY = 1005 # J/kg K
CP_VAPOR = 1846 # J/kg K

# Function to compute grid cell areas
def grid_area(lat, lon):
    '''
    Compute grid cell areas on a sphere for a regular latitude-longitude grid.

    Args:
        lat: xarray.DataArray of latitudes in degrees, dimension 'latitude'
        lon: xarray.DataArray of longitudes in degrees, dimension 'longitude'

    Returns:
        area: xarray.DataArray of grid cell areas in square meters, dimensions ('latitude', 'longitude')
    '''
    
    lat_rad = np.deg2rad(lat)
    lon_rad = np.deg2rad(lon)
    
    # Compute sine of latitude
    sin_lat_rad = np.sin(lat_rad)
    
    # Compute gradient of sine of latitude (d_phi)
    d_phi = np.gradient(sin_lat_rad, axis=0, edge_order=2)
    
    # Compute gradient of longitude (d_lambda)
    d_lambda = np.gradient(lon_rad, axis=1, edge_order=2)
    
    # Adjust d_lambda to be within -π and π
    d_lambda = (d_lambda + np.pi) % (2 * np.pi) - np.pi
    
    # Compute grid cell area
    area = np.abs(RAD_EARTH**2 * d_phi * d_lambda)

    # Create DataArray for area with dimensions ('latitude', 'longitude')
    area = xr.DataArray(
        area,
        coords={'latitude': lat[:, 0], 'longitude': lon[0, :]},
        dims=['latitude', 'longitude']
    )

    return area

# Function to compute pressure integral
def pressure_integral(q, level_p):
    '''
    Compute the pressure level integral of a given quantity using xarray integration.

    Args:
        q: xarray.DataArray with dimensions including 'level'
        level_p: xarray.DataArray of pressure levels in Pa, with dimension 'level'

    Returns:
        xarray.DataArray: Pressure level integrals of q, with dimensions excluding 'level'
    '''
    # Assign 'level_p' as a coordinate
    q = q.assign_coords(level_p=level_p)

    # Integrate over 'level_p' using the trapezoidal rule
    Q = q.integrate(coord='level_p')

    return Q

# Function to compute weighted sum
def weighted_sum(data, weights, dims):
    '''
    Compute the weighted sum of a given quantity using xarray.

    Args:
        data: xarray.DataArray to be summed
        weights: xarray.DataArray of weights, broadcastable to data
        dims: dimensions over which to sum

    Returns:
        xarray.DataArray: weighted sum
    '''
    # Perform weighted sum
    return (data * weights).sum(dim=dims)