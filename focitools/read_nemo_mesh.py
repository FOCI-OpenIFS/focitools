def read_nemo_mesh(mesh_mask_file):
    """
    Read the NEMO mesh file, usually named mesh_mask.nc

    Input:
    mesh_mask_file - full path to the file

    Output: 
    ds - Dataset containing masks, cell area, volume etc
    """
    
    import xarray as xr

    print(' Open NEMO mesh_mask file : ')
    print(mesh_mask_file)
    
    # NEMO mesh file has "z" as vertical coordinate
    # but the grid_T files have "deptht" so we need to rename
    ds_mesh = xr.open_dataset(nemo_mesh)
    
    tarea = (ds_mesh['e1t'] * ds_mesh['e2t']).sel(t=0)
    tarea.name = 'tarea'
    dxt, dyt = ds_mesh['e1t'].sel(t=0), ds_mesh['e2t'].sel(t=0)
    tvol = (ds_mesh['e1t'] * ds_mesh['e2t'] * 
            ds_mesh['e3t_0']).sel(t=0).rename({'z':'deptht'})
    tvol.name = 'tvolume'
    tmask = ds_mesh['tmask'].sel(t=0).rename({'z':'deptht'})
    tmask.name = 'tmask'
    
    uarea = (ds_mesh['e1u'] * ds_mesh['e2u']).sel(t=0)
    uarea.name = 'uarea'
    umask = ds_mesh['umask'].sel(t=0).rename({'z':'deptht'})
    umask.name = 'umask'
    
    varea = (ds_mesh['e1v'] * ds_mesh['e2v']).sel(t=0)
    varea.name = 'varea'
    vmask = ds_mesh['vmask'].sel(t=0).rename({'z':'deptht'})
    vmask.name = 'vmask'
    
    ds = xr.merge([tarea, uarea, varea, dxt, dyt, tvol, tmask, umask, vmask])
    return ds