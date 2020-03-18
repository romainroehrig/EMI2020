#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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

from myfunctions import *

def generate_period(fin, vmin, vmax):
    
    # Where to save images
    # If the directory does not exist, we create it
    rep0 = './quicklooks'
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'period')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)
    
    # Projection for plotting
    proj = ccrs.LambertConformal(central_latitude = 37,
                                 central_longitude = 10,
                                 standard_parallels = (37, 37)
                                 )
    
    file_name = os.path.basename(fin)
    var = file_name.split("_")[0]
    
    # Open file as a dataset
    d = nc.Dataset(fin)
    # Read data, latitude, longitude, time
    data = d[var][:,:,:]
    name = d[var].long_name
    units = d[var].units
    lat = d['lat'][:,:]
    lon = d['lon'][:,:]
    d.close()
    
    # Temporal mean
    data_moy = np.nanmean(data,axis=0)
    
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
    
    # Plot data
    if var == "pctisccp" or var == "pctmodis":
        # if pct convert to hPa
        data_moy /= 100 
        units = "hPa"
    ax.set_title('{0} ({1}) - 2007 to 2016'.format(name,units))
        
    cs = ax.pcolormesh(lon,lat,data_moy, transform=ccrs.PlateCarree(),
            cmap=cm.gist_ncar, vmin=vmin, vmax=vmax,shading='gouraud')
    
    # Add colorbar
    cbar = fig.colorbar(cs, shrink=0.7, orientation='horizontal',pad=0.05)
    
    # Save in png
    plot_name = '{}.png'.format(var)
    plot_path = os.path.join(rep1, plot_name)
    plt.savefig(plot_path, bbox_inches='tight')
    print("Plot saved at {}".format(plot_path))
    plt.close()
    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="path to file", type=str, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=True)
    parser.add_argument("-M", help="max colorbar", type=float, required=True)
    args = parser.parse_args()
    
    fin = args.f
    vmin = args.m
    vmax = args.M

    generate_period(fin, vmin, vmax)
