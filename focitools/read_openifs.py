def read_openifs(exp_list, time_list, esm_dir, grid='regular_sfc', freq='1m', chunk_grid='O96'):
    """
    Function to read OpenIFS data. 

    Input
    -----
    exp_list - List of experiment IDs to read data from
    time_list - List of time slices from each experiment, e.g. [slice('1990-01-01','2015-01-01')]
    esm_dir - Directory where all experiments are stored. Usually $WORK/esm-experiments/
    grid (optional) - What grid to use, e.g. grid_T, regular_sfc (default) etc
    freq (optional) - What time frequency of data to read, e.g. 5d, 1m (default), 1y
    chunk_grid (optional) - Chunking settings. Defaults to O96 which only chunks
                            along the time dimension

    Output
    ------
    ds_all - List with xarray.Dataset containing data from each experiment
    
    """
    
    import xarray as xr
    import cftime 
    from focitools import functions

    if chunk_grid == 'O96':
        # check if sfc is part of the grid, i.e. we are looking at surface 2D fields
        if 'sfc' in grid.split('_'):
            chunks = {'time_counter':240,'lat':-1, 'lon':-1}
        elif 'pl' in grid.split('_'):
            chunks = {'time_counter':12, 'pressure_levels':-1, 'lat':-1, 'lon':-1}
    
    # list for all data
    ds_all = []
    for exp,time in zip(exp_list,time_list):
        
        if freq == '1y':
            files = '%s/%s/outdata/oifs/ym/%s*1y*%s.nc' % (esm_dir,exp,exp,grid)
        else:
            files = '%s/%s/outdata/oifs/%s*%s*%s.nc' % (esm_dir,exp,exp,freq,grid)
        print(files)

        _ds = functions.open_multifile_dataset(files, chunks=chunks)

        # rename time_counter to time
        ds = _ds.rename({'time_counter':'time'}).sel(time=time)
        
        ds_all.append(ds)
        
    return ds_all