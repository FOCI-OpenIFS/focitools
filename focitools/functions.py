def open_multifile_dataset(files, concat_dim="time_counter"):
    """
    Read a dataset from a list of files. 

    This function will read in parallel and use cftime. 
    """

    import cftime
    import xarray as xr
    
    # open multi-file data set. We need to use cftime since the normal python calendar stops working after 2300. 
    # also, we rename time variable from time_counter to time to make life easier
    ds = xr.open_mfdataset(files,combine='nested', 
                           concat_dim=concat_dim, use_cftime=True,
                           data_vars='minimal', coords='minimal',
                           compat='override',
                           parallel=True)
    
    return ds

#def load_exp_info(machine, expname):
#    """
#    
#    """

    