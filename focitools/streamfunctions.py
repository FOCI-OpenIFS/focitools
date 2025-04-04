import numpy as np
import xarray as xr

def compute_amoc_strength(da_amoc, amoc_lat=26.5):
    """
    Compute AMOC at a specific latitude (or NEMO point closest to it).

    Input
    -----
    da_amoc - xarray.DataArray with Atlantic overturning streamfunction.
              This should come from 
              da_amoc = focitools.read_amoc(...)['zomsfatl']
    amoc_lat - Latitude to compute AMOC at (default: 26.5N)

    Output
    ------
    amoc - AMOC time series
    """

    # Latitudes from NEMO grid
    nav_lat = da_amoc['lat'].data
    
    # Find j index closest to amoc_lat
    amoc_j26 = np.argmin( np.abs(nav_lat - amoc_lat) )
    print('AMOC latitude used: ',nav_lat[amoc_j26])
    
    # Take max stream function at specified latitude
    # Also drop unused dimensions
    amoc = da_amoc.sel(x=0,y=amoc_j26).max('depthw').drop('lat')

    return amoc
    