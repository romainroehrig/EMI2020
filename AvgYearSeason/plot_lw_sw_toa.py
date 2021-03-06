#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
sys.path.append("../Commons")
import os
import argparse

import netCDF4 as nc

import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt
from matplotlib import cm

import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import config
from myfunctions import *

def generate_lw_sw_toa_yearavg(fin1, fin2, data_type, vmin, vmax):
    # Where to save images
    # If the directory does not exist, we create it
    rep0 = config.repout
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'yearavg')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)
    
    # Projection for plotting
    proj = ccrs.LambertConformal(central_latitude = 37,
                                 central_longitude = 10,
                                 standard_parallels = (37, 37)
                                 )
    
    file_name1 = os.path.basename(fin1)
    file_name2 = os.path.basename(fin2)

    var1 = file_name1.split("_")[0]
    var2 = file_name2.split("_")[0]
    
    # Open file as a dataset
    d1 = nc.Dataset(fin1)
    d2 = nc.Dataset(fin2)

    # Read data, latitude, longitude, time
    data1 = d1[var1][:,:,:]
    data2 = d2[var2][:,:,:]
    units = d1[var1].units
    lat = d1['lat'][:,:]
    lon = d1['lon'][:,:]
    d1.close()
    d2.close()

    # Temporal mean - annual
    
    #data_moy1 = np.nanmean(data1[336:444,:,:],axis=0)
    data_moy1 = np.nanmean(data1[336:444,:,:],axis=0)
    data_moy2 = np.nanmean(data2[336:444,:,:],axis=0)
    data_diff = data_moy2 - data_moy1

    #PLOTS 
    # Domain to be plotted
    bbox = [-24,44,14,56]
    
    # Map projection is Lambert Conformal (proj)
    fig, ax = plt.subplots(figsize=(15,10),subplot_kw=dict(projection=proj))
    
    # Apply domain to be plotted
    ax.set_extent(bbox,crs=ccrs.PlateCarree())
    # Add coastlines
    ax.coastlines('50m')
    # Add country borders
    ax.add_feature(cf.BORDERS)
    
    # *must* call draw in order to get the axis boundary used to add ticks
    fig.canvas.draw()
    
    xticks = range(-180,181,10)
    yticks = range(-90,91,10)
    ax.gridlines(xlocs=xticks, ylocs=yticks,linestyle='--',lw=1,color='dimgrey')
    
    # Label the end-points of the gridlines using the custom tick makers:
    ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
    ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
    
    lambert_xticks(ax, xticks)
    lambert_yticks(ax, yticks)
    
    ax.set_title('TOA CRE {0} ({1}) - [2007-2016]'.format(data_type, units))
    
    # Plot data
    cs = ax.pcolormesh(lon,lat,data_diff, transform=ccrs.PlateCarree(),
            cmap=cm.gist_ncar, vmin=vmin, vmax=vmax,shading='gouraud')
    
    # Add colorbar
    cbar = fig.colorbar(cs, shrink=0.7, orientation='horizontal',pad=0.05)
    
    # Save in png
    plot_name = '{}_TOA_CRE.png'.format(data_type)
    plot_path = os.path.join(rep1, plot_name)
    plt.savefig(plot_path, bbox_inches='tight')
    print("Plot saved at {}".format(plot_path))
    plt.close()

    
   
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", help="path to file", type=str, required=True)
    parser.add_argument("-f2", help="path to file", type=str, required=True)
    parser.add_argument("-t", help="data type (eg : LW, SW)", type=str, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=True )
    parser.add_argument("-M", help="max colorbar", type=float, required=True)
    args = parser.parse_args()
    
    fin1 = args.f1
    fin2 = args.f2
    vmin = args.m
    vmax = args.M
    data_type = args.t
    generate_lw_sw_toa_yearavg(fin1, fin2, data_type, vmin, vmax)
