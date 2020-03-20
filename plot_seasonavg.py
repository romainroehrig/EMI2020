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

import config
from myfunctions import *

def generate_season(fin, vmin, vmax):
    # Where to save images
    # If the directory does not exist, we create it
    rep0 = config.repout
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'seasonavg')
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

    # Temporal mean - season
    data_winter = data[0] + data[1]
    data_spring = 0
    data_summer = 0
    data_fall = 0

    for i in range(10):
        if i<9:
            data_winter = data_winter + data[11+12*i] + data[12+12*i] + data[13+12*i]
        data_spring = data_spring + data[2+12*i] + data[3+12*i] + data[4+12*i]
        data_summer = data_summer + data[5+12*i] + data[6+12*i] + data[7+12*i]
        data_fall = data_fall + data[8+12*i] + data[9+12*i] + data[10+12*i]

    data_winter_moy = data_winter/29
    data_spring_moy = data_spring/30
    data_summer_moy = data_summer/30
    data_fall_moy = data_fall/30

    #PLOTS

    # Domain to be plotted
    bbox = [-24,44,14,56]

    # Map projection is Lambert Conformal (proj)
    fig, axes = plt.subplots(2,2,figsize=(15,10),subplot_kw=dict(projection=proj))
    data_season = [data_winter_moy, data_spring_moy, data_summer_moy, data_fall_moy]
    title_season = ['winter','spring','summer','fall']

    for i, ax in enumerate(axes.flat):
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
            data_season[i] /= 100 
            units = "hPa"

        ax.set_title('{0} ({1})\n2007 to 2016 - {2}'.format(name,units,title_season[i]))

        cs = ax.pcolormesh(lon,lat,data_season[i], transform=ccrs.PlateCarree(),
        			cmap=cm.gist_ncar, vmin=vmin, vmax=vmax,shading='gouraud')

    # Add colorbar
    fig.subplots_adjust(right=0.8, hspace=0.5)
    cbar = fig.colorbar(cs, ax=axes[:,:], shrink=0.5, orientation='horizontal',pad=0.1)

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

    generate_season(fin, vmin, vmax)
