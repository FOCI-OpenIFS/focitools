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
    # but the grid_T files have "deptht" etc so we need to rename
    ds_mesh = xr.open_dataset(mesh_mask_file)
    
    # dx dy
    dxt, dyt = ds_mesh['e1t'].squeeze(), ds_mesh['e2t'].squeeze()
    dxu, dyu = ds_mesh['e1u'].squeeze(), ds_mesh['e2u'].squeeze()
    dxv, dyv = ds_mesh['e1v'].squeeze(), ds_mesh['e2v'].squeeze()
    
    # dz (3D field)
    dzt = ds_mesh['e3t_0'].rename({'z':'deptht'}).squeeze()
    dzu = ds_mesh['e3u_0'].rename({'z':'depthu'}).squeeze()
    dzv = ds_mesh['e3v_0'].rename({'z':'depthv'}).squeeze()
    dzt.name = 'dzt'
    dzu.name = 'dzu'
    dzv.name = 'dzv'
    
    # areacello - Ocean cell area (T points)
    # We use squeeze to remove 1-element time dimension
    areacello = (ds_mesh['e1t'] * ds_mesh['e2t']).squeeze()
    areacello.name = 'areacello'
    areacello = areacello.assign_attrs(units='m2')
    
    areacello_u = (dxu * dyu).squeeze()
    areacello_u.name = 'areacello_u'
    areacello_v = (dxv * dyv).squeeze()
    areacello_v.name = 'areacello_v'
    
    # volcello - Ocean cell volume (T points)
    # transpose so that depth is 1st dim
    volcello = (dxt * dyt * dzt).squeeze().transpose('deptht','y','x')
    volcello.name = 'volcello'
    volcello = volcello.assign_attrs(units='m3')
    
    # masscello - Mass of ocean cells per area
    # In NEMO, this is rho0 * volcello / areacello
    # (note: with key_vvl, dz is no longer constant in time)
    # Also, transpose so that depth is first dimension
    masscello = (volcello * 1026.0 / areacello).transpose('deptht','y','x')
    masscello.name = 'masscello'
    masscello = masscello.assign_attrs(units = 'kg/m2')
    
    # masks
    tmask = ds_mesh['tmask'].rename({'z':'deptht'}).squeeze()
    tmask.name = 'tmask'
    umask = ds_mesh['umask'].rename({'z':'depthu'}).squeeze()
    umask.name = 'umask'
    vmask = ds_mesh['vmask'].rename({'z':'depthv'}).squeeze()
    vmask.name = 'vmask'
    
    # depths 3D fields
    gdept = ds_mesh['gdept_0'].rename({'z':'deptht'})
    gdepu = ds_mesh['gdepu'].rename({'z':'depthu'})
    gdepv = ds_mesh['gdepv'].rename({'z':'depthv'})
    
    # compute depth as 2D fields
    # mask land, then take max values for each x,y cell
    deptho = gdept.where(tmask != 0).max('deptht').squeeze()
    deptho_u = gdepu.where(umask != 0).max('depthu').squeeze()
    deptho_v = gdepv.where(vmask != 0).max('depthv').squeeze()
    deptho.name = 'deptho'
    deptho_u.name = 'deptho_u'
    deptho_v.name = 'deptho_v'
    
    ds = xr.merge([areacello, areacello_u, areacello_v, 
                   dxt, dyt, 
                   dzt, dzu, dzv, 
                   volcello, masscello, 
                   deptho, deptho_u, deptho_v,
                   tmask, umask, vmask])
    
    return ds
    
    
def compute_dz_tilde(ssh, dz0, depth0, areacello):
    """
    Compute time varying cell thickness, volume and mass for runs with vvl
    
    When running with vvl, one should take care to store e3t, e3u, e3v etc
    but this function allows you to approximate them. 
    Using ssh from 5d or 1m output will not yield the same results as when 
    doing online calculations in NEMO, but the approximation is often within
    a few percent. 
    
    Input
    ssh - x,y,t field with ssh
    dz0 - x,y,z field with thickness assuming ssh=0
    depth0 - x,y field with depth assuming ssh=0
    areacella - x,y field with cell area
    """
    
    # Taken from NEMO code
    dz = dz0 * (1.0 + ssh/depth0)
    
    # Compute masscello
    masscello = dz * 1026.0 # [kg/m2]
    
    # Volume
    volcello = areacello * dz
    
    return dz, volcello, masscello
    