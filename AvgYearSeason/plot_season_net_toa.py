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
from myfunctions import *

def generate_season_net_toa(fin1, fin2, fin3, fin4, data_type, vmin, vmax):
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
    
    file_name1 = os.path.basename(fin1)
    file_name2 = os.path.basename(fin2)
    file_name3 = os.path.basename(fin3)
    file_name4 = os.path.basename(fin4)

    var1 = file_name1.split("_")[0]
    var2 = file_name2.split("_")[0]
    var3 = file_name3.split("_")[0]
    var4 = file_name4.split("_")[0]
    
    # Open file as a dataset
    d1 = nc.Dataset(fin1)
    d2 = nc.Dataset(fin2)
    d3 = nc.Dataset(fin3)
    d4 = nc.Dataset(fin4)
    # Read data, latitude, longitude, time
    data1 = d1[var1][:,:,:]
    data2 = d2[var2][:,:,:]
    data3 = d3[var3][:,:,:]
    data4 = d4[var4][:,:,:]
    
    units = d1[var1].units
    lat = d1['lat'][:,:]
    lon = d1['lon'][:,:]

    d1.close()
    d2.close()
    d3.close()
    d4.close()

    # Temporal mean - season
    data_1=[0,0,0,0]
    data_2=[0,0,0,0]
    data_3=[0,0,0,0]
    data_4=[0,0,0,0]

    data_1_moy=[0,0,0,0]
    data_2_moy=[0,0,0,0]
    data_3_moy=[0,0,0,0]
    data_4_moy=[0,0,0,0]

    data_season=[0,0,0,0]

    for i in range(10):
        for j in range(4):
            data_1[j] = data_1[j] + data1[335+3*j+12*i] + data1[336+3*j+12*i] + data1[337+3*j+12*i]
            data_2[j] = data_2[j] + data2[335+3*j+12*i] + data2[336+3*j+12*i] + data2[337+3*j+12*i]
            data_3[j] = data_3[j] + data3[335+3*j+12*i] + data3[336+3*j+12*i] + data3[337+3*j+12*i]
            data_4[j] = data_4[j] + data4[335+3*j+12*i] + data4[336+3*j+12*i] + data4[337+3*j+12*i]
	
	for j in range(4):

		data_1_moy[j]= data_1[j]/30
		data_2_moy[j]= data_2[j]/30
		data_3_moy[j]= data_3[j]/30
		data_4_moy[j]= data_4[j]/30

	for j in range(4):
		
		data_season[j] = (data_2_moy[j] - data_1_moy[j]) + (data_4_moy[j] - data_3_moy[j])

    #PLOTS

    # Domain to be plotted
    bbox = [-24,44,14,56]

    # Map projection is Lambert Conformal (proj)
    fig, axes = plt.subplots(2,2,figsize=(15,10),subplot_kw=dict(projection=proj))
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

        ax.set_title('TOA CRE {0} ({1}) - [2007-2016] - {2}'.format(data_type, units, title_season[i]))

            # Plot data
        cs = ax.pcolormesh(lon,lat,data_season[i], transform=ccrs.PlateCarree(),
                    cmap=cm.gist_ncar, vmin=vmin, vmax=vmax, shading='gouraud')

    # Add colorbar
	fig.subplots_adjust(right=0.88, bottom=0.005, top = 0.95, wspace=0.5)
    cbar = fig.colorbar(cs, ax=axes, shrink=0.5, orientation='horizontal',pad=0.07)

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
    parser.add_argument("-f3", help="path to file", type=str, required=True)
    parser.add_argument("-f4", help="path to file", type=str, required=True)
    parser.add_argument("-t", help="data type (eg : LW, SW)", type=str, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=True )
    parser.add_argument("-M", help="max colorbar", type=float, required=True)
    args = parser.parse_args()
    
    fin1 = args.f1
    fin2 = args.f2
    fin3 = args.f3
    fin4 = args.f4
    vmin = args.m
    vmax = args.M
    data_type = args.t
    generate_season_net_toa(fin1, fin2, fin3, fin4, data_type, vmin, vmax)
