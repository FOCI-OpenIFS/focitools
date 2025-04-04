def open_multifile_dataset(files, 
                           concat_dim='time_counter',
                           chunks={'time_counter':1,'lat':-1,'lon':-1}):
    """
    Read a dataset from a list of files. The list should contain files from the same grid, 
    e.g. grid_T files etc. 

    Input
    -----
    files - List of files, e.g. grid_T files
    concat_dim (optional) - Dimension to concatenate files over. 
                            Is time_counter for OpenIFS, NEMO
                            Is time for ECHAM
    chunks (optional) - Dictionary with chunks for each dimension

    Output
    ------
    ds - xarray.Dataset with data from all files merged into one dataset
    
    This function will read in parallel and use cftime. 
    Chunking is applied. By default, no chunking in lon,lat, and size 1 in time. 
    """

    import cftime
    import xarray as xr
    
    # open multi-file data set. We need to use cftime since the normal python calendar stops working after 2300. 
    # also, we rename time variable from time_counter to time to make life easier
    ds = xr.open_mfdataset(files,combine='nested', 
                           chunks=chunks,
                           concat_dim=concat_dim, use_cftime=True,
                           data_vars='minimal', coords='minimal',
                           compat='override',
                           parallel=True)
    
    return ds
    