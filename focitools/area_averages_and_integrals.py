import numpy as np
import xarray as xr

def area_mean(data, lon_name='lon', lat_name='lat'):
    """
    Compute area average for data on a lon/lat grid. 
    Designed for OpenIFS and ECHAM, but should work for any
    data on lon/lat grid. 

    Input:
    data - DataArray with lon and lat as dimensions

    lon_name (optional) - name of lon dimension, default: lon
    lat_name (optional) - name of lat dimension, default: lat
    
    Output: 
    data_mean - DataArray with area-weighted average
    """

    # make a copy of array
    data_copy = data.copy()
    
    # cast longitude and latitude to radians
    data_copy[lon_name] = np.deg2rad(data_copy[lon_name]) 
    data_copy[lat_name] = np.deg2rad(data_copy[lat_name])

    # sort data so that we always have lon = [0,2pi], lat = [-pi/2, pi/2]
    data_sorted = data_copy.sortby('lon').sortby('lat')
    
    # area weighting can be done by weighting by cos(latitude)
    weights = np.cos(data_sorted.lat)
    weights.name = "weights"

    # add weights to data and compute mean
    data_wgt = data_sorted.weighted(weights)
    data_mean = data_wgt.mean((lon_name, lat_name))
    
    return data_mean

def area_mean_nemo(data, mask, cell_area, x_name='x', y_name='y'):
    """
    Compute area average for NEMO data

    Input
    data - DataArray with x and y dimensions
    mask - land-sea mask
    cell_area - cell area (should be m2, but not required)

    x_name (optional) - name of x dimension (default: x)
    y_name (optional) - name of y dimension (default: y)

    Output
    data_mean - area mean over x and y
    """
    
    # Mask points where mask is not 1
    # and add cell_area as weight
    data_wgt = data.where(mask == 1).weighted(cell_area)

    # compute mean
    data_mean = data_wgt.mean((x_name, y_name))
    
    return data_mean


def zonal_mean_nemo(data, mask, cell_area, x_name='x', y_name='y', lat_name='nav_lat'):
    """
    Compute weighted zonal mean in NEMO data

    Input
    data - DataArray with NEMO data
    mask - land-sea mask
    cell_area - cell areas (should be m2 but not required)
    x_name (optional) - name of x dimension (default: x)

    """
    
    # Mask points where mask is not 1
    # and add cell_area as weight
    data_wgt = data.where(mask == 1).weighted(area)

    # compute mean
    data_mean = data_wgt.mean(x_name)

    # zonal mean of latitude
    lat_mean = data[lat_name].mean(x_name)
    
    return data_mean, lat_mean

#
# compute sea ice area
#
def seaice_areas(ds, areacello, lsm, sicname='ileadfra', latname='nav_lat'):
    """
    Compute sea-ice area and extent. 
    
    Sea-ice area (SIA) is total area of sea ice. 
    Sea-ice extent (SIE) is total area where sea-ice conc exceeds 15%. 
    
    Do calculations separately for Northern and Southern Hemisphere
    
    Input: 
    ds - Dataset with sea-ice fraction [0,1]. 
    areacello - Area in m2 for ocean cells
    lsm - Land-sea mask for ocean where 1 is ocean and 0 is land. 
    sicname - Name of sea-ice concentration (default: ileadfra)
    latname - Name of latitude array (default: nav_lat)
    
    Output
    ds - Dataset with the following variables:
         ar_sia - Arctic SIA
         an_sia - Antarctic SIA
         ar_sie - Arctic SIE
         an_sie - Antarctic SIE
         All are in million km2
    """
    
    
    # scale from m2 to million km2
    icescale = 1e-12
    
    # ice area = icefrac * cell area
    _nh = (ds[sicname].where(ds[latname] > 0) * areacello).sum(('x','y')) * icescale
    _sh = (ds[sicname].where(ds[latname] < 0) * areacello).sum(('x','y')) * icescale
    
    # ice extent = cell area where icefrac > 0.15
    _nh2 = (ds[sicname].where(ds[latname] > 0).where(ds[sicname] > 0.15) * areacello).sum(('x','y')) * icescale
    _sh2 = (ds[sicname].where(ds[latname] < 0).where(ds[sicname] > 0.15) * areacello).sum(('x','y')) * icescale
    
    # give dataarrays names
    _nh.name = 'ar_sia'
    _sh.name = 'an_sia'
    _nh2.name = 'ar_sie'
    _sh2.name = 'an_sie'
    _ds_n = _nh.to_dataset()
    _ds_s = _sh.to_dataset()
    _ds_n2 = _nh2.to_dataset()
    _ds_s2 = _sh2.to_dataset()
    
    # put results in one dataset
    _ds = xr.merge([_ds_n, _ds_s, _ds_n2, _ds_s2])
    
    return _ds


def ice_volumes(ds, areacello, lsm, latname='nav_lat', xname='x', yname='y'):
    """
    Compute sea-ice volume and mean thickness. 
    
    Sea-ice volume is the product of cell-averaged thickness and cell area
    Sea-ice thickness is the volume divided by total area. 
    
    Do calculations separately for Northern and Southern Hemisphere. 
    
    Input: 
    ds - Dataset with sea-ice fraction and cell-averaged thickness
    areacello - Area of ocean cells
    lsm - Land-sea mask where 1 is ocean and 0 is land. 
    latname (optional) - Name of latitude array (default: nav_lat)
    xname (optional) - Name of x dimension (default: x)
    yname (optional) - Name of y dimension (default: y)
    
    Output: 
    ds - Dataset containing the following variables
         ar_siv - Arctic SIV
         an_siv - Antarctic SIV
         ar_sit - Arctic SIT (=SIV/SIA)
         an_sit - Antarctic SIT (= SIV/SIA)
    """
    # scale from m3 to km3
    icescale = 1e-9
    
    # iicethic is cell average ice thickness
    # i.e. if half cell is covered by 2m thick ice, iicethic is 1m
    _nh = (ds['iicethic'].where(ds[latname] > 0) * areacello).sum(('x','y')) * icescale
    _sh = (ds['iicethic'].where(ds[latname] < 0) * areacello).sum(('x','y')) * icescale 
    
    # area-mean ice thickness where concentration >= 0.15
    nh_thk_wgt = ds['iicethic'].where(ds['ileadfra'] >= 0.15).where(ds[latname] > 0).weighted(areacello)
    sh_thk_wgt = ds['iicethic'].where(ds['ileadfra'] >= 0.15).where(ds[latname] < 0).weighted(areacello)
    _nh_thk = nh_thk_wgt.mean((xname,yname))
    _sh_thk = sh_thk_wgt.mean((xname,yname))
    
    _nh.name = 'ar_siv'
    _sh.name = 'an_siv'
    _ds_n = _nh.to_dataset()
    _ds_s = _sh.to_dataset()
    
    _nh_thk.name = 'ar_sit'
    _sh_thk.name = 'an_sit'
    _ds_n_thk = _nh_thk.to_dataset()
    _ds_s_thk = _sh_thk.to_dataset()
    
    _ds = xr.merge([_ds_n, _ds_s, _ds_n_thk, _ds_s_thk])
    
    return _ds