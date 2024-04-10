def read_echam(exp_list, time_list, esm_dir, grid='BOT', freq='mm', machine='nesh'):

    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):
        
        if freq == '1y':
            files = '%s/%s/outdata/oifs/ym/*1y*%s.nc' % (esm_dir,exp,grid)
        else:
            files = '%s/%s/outdata/echam/%s*%s*%s*.nc' % (esm_dir,exp,exp,grid,freq)
        print(files)

        _ds = open_multifile_dataset(files)
        ds = _ds.sel(time=time)
        ds_all.append(ds)
        
    return ds_all