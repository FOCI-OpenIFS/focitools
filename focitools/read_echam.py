def read_echam(exp_list, time_list, esm_dir, grid='BOT', freq='mm', machine='nesh'):
    
    import xarray as xr
    import cftime 
    from focitools import functions
    
    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):
        
        if freq == '1y':
            files = '%s/%s/outdata/echam/ym/*1y*%s.nc' % (esm_dir,exp,grid)
        else:
            files = '%s/%s/outdata/echam/%s*%s*%s*.nc' % (esm_dir,exp,exp,grid,freq)
        print(files)

        _ds = functions.open_multifile_dataset(files, concat_dim='time')
        ds = _ds.sel(time=time)
        ds_all.append(ds)
        
    return ds_all