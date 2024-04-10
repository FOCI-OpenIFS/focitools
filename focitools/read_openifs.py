def read_openifs(exp_list, time_list, esm_dir, grid='regular_sfc', freq='1m'):
    """
    Function to read OpenIFS data
    """
    
    import xarray as xr
    import cftime 
    from focitools import functions
    
    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):
        
        if freq == '1y':
            files = '%s/%s/outdata/oifs/ym/%s*1y*%s.nc' % (esm_dir,exp,exp,grid)
        else:
            files = '%s/%s/outdata/oifs/%s*%s*%s.nc' % (esm_dir,exp,exp,freq,grid)
        print(files)
        
        _ds = functions.open_multifile_dataset(files)

        # rename time_counter to time
        ds = _ds.rename({'time_counter':'time'}).sel(time=time)
        
        ds_all.append(ds)
        
    return ds_all