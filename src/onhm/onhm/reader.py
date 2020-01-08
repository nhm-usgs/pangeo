"""
Created on Thu Dec 12 08:00:48 2019

@author: markstro
"""

import xarray as xr
import glob
import os


def varbrowser(d="",word=""):
    """Returns a list with all files with the word/extension in it"""
    file = []
    for f in glob.glob(d + "/*" + word):
        if word in f:
            file.append(os.path.splitext(os.path.basename(f))[0])
    return file
    

# returns an xarray.Dataset
def get_DataSet(out_dir, exp):
    # get list of vars from ncf file names
    vars = varbrowser(out_dir, ".nc")
    
    # make a dataset with everything in the directory
    ds = xr.Dataset()
    first_hru = True
    first_seg = True
    for var in vars:
        foo = xr.open_dataset(out_dir + var + exp)
        
        if first_hru and "hruid" in foo.dims.keys():
            hru_lat = foo.get("hru_lat")
            ds['hru_lat'] = hru_lat
            hru_lon = foo.get("hru_lon")
            ds['hru_lon'] = hru_lon
            first_hru = False
            
        if first_seg and "segid" in foo.dims.keys():
            seg_lat = foo.get("seg_lat")
            ds['seg_lat'] = seg_lat
            seg_lon = foo.get("seg_lon")
            ds['seg_lon'] = seg_lon
            first_seg = False
    
        v = foo.get(var)
        ds[var] = v
    return ds
    

def get_feat_coord(feat, data_set, feat_id):
    lat_da = data_set[feat + '_lat']
    lat = lat_da[feat_id-1].values
    lon_da = data_set[feat + '_lon']
    lon = lon_da[feat_id-1].values
    return lat,lon


def get_hruids_for_box(ds_out, lat_min, lat_max, lon_min, lon_max, var):
    lat = ds_out.hru_lat
    sel = lat.sel(hruid=((lat.values >= lat_min) & (lat.values <= lat_max)))
    ids_1 = sel.hruid.values

    lon = ds_out.hru_lon
    sel_1 = lon.sel(hruid=ids_1)
    sel_2 = sel_1.sel(hruid=((sel_1.values >= lon_min) & (sel_1.values <= lon_max)))
    ids_2 = sel_2.hruid.values
    
    return ids_2
    