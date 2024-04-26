import xarray as xr
import cftime
from focitools import functions

def read_nemo(exp_list, time_list, esm_dir, 
              grid='grid_T', freq='1m', agrif_prefix='', decode_timedelta=True):
    """
    Read output from NEMO

    Input
    exp_list - List of experiment IDs, e.g. FOCI_GJK029
    time_list - List time slices to read
    esm_dir - Directory to experiments (usually named esm_experiments)
    
    Input (optional)
    grid - e.g. grid_T, grid_U, icemod, ptrc_T, etc. Default: grid_T
    freq - e.g. 1m, 5d. Default: 1m
    decode_timedelta - Decode time differences (True) or not (False). Default: True
    agrif_prefix - Prefix for AGRIF files, e.g. 1_. Default: empty string

    Note: 
    Xarray decodes timedelta to nanoseconds, which overflow after approx 300 years 
    (300 years is approx 2^63 ns). 
    Therefore, it is advisable to set decode_timedelta=False when reading tracer age files
    """
    
    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):

        # Note: In case of AGRIF, all files will have a prefix of 1_ or 2_ 
        if freq == '1y':
            files = '%s/%s/outdata/nemo/ym/%s%s*1y*%s.nc' % (esm_dir,exp,agrif_prefix,exp,grid)
        else:
            files = '%s/%s/outdata/nemo/%s%s*%s*%s.nc' % (esm_dir,exp,agrif_prefix,exp,freq,grid)
        print(files)
        
        # use function to read multi-file data set
        # Will use cftime, read in parallel, etc. 
        ds = functions.open_multifile_dataset(files).rename({'time_counter':'time'}).sel(time=time)
        
        ds_all.append(ds)
        
    return ds_all


def read_amoc(exp_list, time_list, esmdir):
    
    derived_list = ['moc','amoc_max_25.000N','amoc_max_45.000N']
    derived_name = ['moc','amoc25','amoc45']
    
    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):
        
        ds_derived = []
        
        for i,(derived,name) in enumerate(zip(derived_list,derived_name)):
            
            files = '%s/%s/derived/nemo/%s*%s.nc' % (esmdir,exp,exp,derived)
            
            # use function to read multi-file data set
            # Will use cftime, read in parallel, etc. 
            ds = functions.open_multifile_dataset(files).rename({'time_counter':'time'}).sel(time=time)
            
            # For overturning stream functions, add latitude on y coord
            if i == 0:
                lat = ds['nav_lat'][:,0].data
                ds = ds.assign_coords(lat=("y", lat))
            
            # Rename AMOC_MAX to amoc25 or amoc45
            if i > 0:
                ds = ds.rename({'AMOC_MAX':name})
            
            ds_derived.append(ds)
        
        # Merge into one dataset
        _ds = xr.merge(ds_derived)
        ds_all.append(_ds)
        
    return ds_all


def read_transports(exp_list, time_list, esmdir):
    
    transp_list = ['AFR_AUSTR','AM_AFR','AUS_AA','AUSTR_AM','BAFFIN','BERING',
                   'CAMPBELL','CUBA_FLORIDA','DAVIS','DENMARK_STRAIT','DRAKE',
                   'FLORIDA_BAHAMAS','FRAM','ICELAND_SCOTLAND','ITF',
                   'KERGUELEN','MOZAMBIQUE_CHANNEL','SOUTH_AFR']
    
    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):
        
        ds_derived = []
        
        for i,(transp,name) in enumerate(zip(transp_list,transp_list)):
            
            files = '%s/%s/derived/nemo/%s*%s_transports.nc' % (esmdir,exp,exp,transp)
            
            # use function to read multi-file data set
            # Will use cftime, read in parallel, etc. 
            ds = functions.open_multifile_dataset(files).rename({'time_counter':'time'}).sel(time=time)
            
            # each transport file has its own nav_lon etc, 
            # so we cant just merge all datasets
            # Need to select just the transport as time series
            
            # all variables in a list
            var_names = ds.keys()
            
            # find variable that starts with vtrp 
            v = [s for s in var_names if 'vtrp' in s][0]
            
            # select this variable alone
            da = ds[v].isel(x=0,y=0)
            
            # add to list
            ds_derived.append(da)
        
        # merge all DataArrays to one DataSet
        _ds = xr.merge(ds_derived)
        
        # add result to a list
        ds_all.append(_ds)
        
    return ds_all


def read_psi(exp_list, time_list, esm_dir):
    """
    Read barotropic stream function as computed with CDFTOOLS in the nemo_monitoring.sh script

    Input:
    exp_list - List of experiments
    time_list - List of time slices
    esm_dir - dir to experiments, usually named esm_experiments

    Output
    ds_all - List with all Datasets 
    """
    derived_list = ['psi']
    derived_name = ['psi']
    
    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):
        
        ds_derived = []
        
        for i,(derived,name) in enumerate(zip(derived_list,derived_name)):
            
            files = '%s/%s/derived/nemo/%s*%s.nc' % (esm_dir,exp,exp,derived)
            
            # use function to read multi-file data set
            # Will use cftime, read in parallel, etc. 
            ds = functions.open_multifile_dataset(files).rename({'time_counter':'time'}).sel(time=time)
            
            ds_derived.append(ds)
        
        _ds = xr.merge(ds_derived)
        ds_all.append(_ds)
        
    return ds_all    