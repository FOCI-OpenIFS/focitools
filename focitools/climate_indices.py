import numpy as np
import xarray as xr
from focitools import functions

def compute_nino_index(sst, index='NINO3.4', time_name='time'):
    """
    Compute ENSO indices from monthly SST anomalies using an area mean over the tropical Pacific. 
    The area and time averaging depends on the chosen index. 
    Also computes mask of months with El Nino or La Nina events for easy compositing. 
    
    Note
    ----
    The function also identifies El Nino and La Nina months, 
    so the user can easily compute an El Nino composite. 
    For u10 anomalies: 
    u10_comp = u10_anomalies.isel(time=en).mean('time')
    
    
    Reference
    ----
    https://climatedataguide.ucar.edu/climate-data/nino-sst-indices-nino-12-3-34-4-oni-and-tni

    Input
    -----
    sst - Monthly SST field as xarray.DataArray 
    index (optional) - which index to compute, 
                       'NINO1+2', 'NINO3', 'NINO3.4' (default), ONI. 
    time_name - Name of time dimension
    
    Output
    ------
    nino_norm - Monthly NINO index as xarray.DataArray
    en - True where El Nino event as numpy.array
    ln - True where La Nina event as numpy.array
    
    """
    
    # compute monthly anomalies
    sst_anom = sst.groupby(time_name+'.month') - sst.groupby(time_name+'.month').mean(time_name)
    
    # select region
    # NINO1+2: (0-10S, 90W-80W)
    # NINO3: (5N-5S, 150W-90W)
    # NINO3.4: (5N-5S, 170W-120W), 5-month running mean 
    # ONI: (5N-5S, 170W-120W), 3-month running mean
    if index = 'NINO1+2':
        sst_nino = sst_anom.sel(lon=slice(270,280), lat=slice(-10,0))
        runmean = 5
        
    elif index = 'NINO3':
        sst_nino = sst_anom.sel(lon=slice(210,270),lat=slice(-5,5))
        runmean = 5
    
    elif index = 'NINO3.4':
        sst_nino = sst_anom.sel(lon=slice(190,240),lat=slice(-5,5))
        runmean = 5
        el_nino_cut = 0.4
        la_nina_cut = -0.4
        
    elif index = 'ONI':
        sst_nino = sst_anom.sel(lon=slice(190,240),lat=slice(-5,5))
        runmean = 3
        el_nino_cut = 0.5
        la_nina_cut = -0.5
        
    # Average over region 
    nino_m = functions.area_mean(sst_nino)
    
    # Running mean
    nino_raw = nino_m.rolling(time=runmean, center=True).mean()
    
    # Find El Nino and La Nina events
    vals = nino_raw.fillna(0).data
    en = np.where(vals >= el_nino_cut)
    ln = np.where(vals <= la_nina_cut)
    
    # Normalise index
    nino = (nino_raw - nino_raw.mean(time_name)) / nino_raw.std(time_name)
    
    return nino, en, ln