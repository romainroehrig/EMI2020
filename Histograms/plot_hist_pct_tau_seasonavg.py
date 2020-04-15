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

from myfunctions import *

import config
from domains import domains

def generate_hist_period(fin, lat_min, lat_max, lon_min, lon_max, vmin, vmax, reg, sim):

    # Where to save images
    # If the directory does not exist, we create it
    rep0 = config.repout
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'seasonavg')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)
    
    file_name = os.path.basename(fin)
    var = file_name.split("_")[0]
    
    # Open file as a dataset
    d = nc.Dataset(fin)
    
    # Prepare histogram axes
    tau_bounds = d['tau_bounds'][:,:]
    ntau, nb = tau_bounds.shape 
    plev7_bounds = d['plev7_bounds'][:,:]/100.
    nplev7, nb = plev7_bounds.shape

    taub = np.zeros(ntau+1)
    taub[0:ntau] = tau_bounds[0:ntau,0]
    taub[ntau] = tau_bounds[ntau-1,1]

    xaxis = np.arange(0,ntau+1)

    plev7b = np.zeros(nplev7+1)
    plev7b[0:nplev7] = plev7_bounds[0:nplev7,0]
    plev7b[nplev7] = plev7_bounds[nplev7-1,1]

    # Read latitude, longitude
    lat = d['lat'][:,:]
    lon = d['lon'][:,:]

    # Extract domain (find coords of nearest point in grid from point)
    target_x = []
    target_y = []

    nlat,nlon = lat.shape
    for x in range(nlon):
        for y in range(nlat):
            if lat[y,x]>=lat_min and lat[y,x]<=lat_max and lon[y,x]>=lon_min and lon[y,x]<=lon_max:
                target_x.append(x)
                target_y.append(y)
    data = d[var][:,:,:,min(target_y):max(target_y),min(target_x):max(target_x)]
    
    # Close netcdf file
    d.close()
    
    # Spatial mean
    data_moy = ma.average(data,axis=(3,4))

    # Temporal mean - season
    data_winter = data_moy[0] + data_moy[1]
    data_spring = 0
    data_summer = 0
    data_fall = 0

    for i in range(10):
        if i<9:
            data_winter = data_winter + data_moy[11+12*i] + data_moy[12+12*i] + data_moy[13+12*i]
        data_spring = data_spring + data_moy[2+12*i] + data_moy[3+12*i] + data_moy[4+12*i]
        data_summer = data_summer + data_moy[5+12*i] + data_moy[6+12*i] + data_moy[7+12*i]
        data_fall = data_fall + data_moy[8+12*i] + data_moy[9+12*i] + data_moy[10+12*i]

    data_winter_moy = data_winter/29
    data_spring_moy = data_spring/30
    data_summer_moy = data_summer/30
    data_fall_moy = data_fall/30

    #PLOTS

    # Domain to be plotted
    bbox = [-24,44,14,56]

    # Map projection is Lambert Conformal (proj)
    fig, axes = plt.subplots(2,2,figsize=(14, 17))
    data_season = [data_winter_moy, data_spring_moy, data_summer_moy, data_fall_moy]
    title_season = ['winter','spring','summer','fall']

    for i, ax in enumerate(axes.flat):
        a, b = np.meshgrid(plev7b, xaxis)
        cs = ax.pcolormesh(b,a,data_season[i], vmin=vmin, vmax=vmax, cmap=cm.terrain)

        # X axis
        ax.set_xticks(xaxis[:-1])
        ax.set_xticklabels(['{0:3.1f}'.format(x) for x in taub[:-1]])
        ax.set_xlabel('Optical Thickness (-)')
        # Y axis
        ax.set_ylim(1000,0)
        ax.set_yticks(plev7b[:-1])
        ax.set_ylabel('Cloud Top Pressure (hPa)')
        # display grid
        ax.grid(color='k', linestyle='--', linewidth=1)
        # Title
        ax.set_title('{0} Cloud Fraction (%) - {1}\n[2007-2016] - {2}'.format(sim, reg.replace("_", " ").title(),title_season[i]))
    
    # Add colorbar
    fig.subplots_adjust(right=0.8, hspace=0.5)
    cbar = fig.colorbar(cs, ax=axes[:,:], shrink=0.5, orientation='horizontal',pad=0.1)    

     # Save in png
    plot_name = '{}_{}.png'.format(var, reg)
    plot_path = os.path.join(rep1, plot_name)
    plt.savefig(plot_path, bbox_inches='tight')
    print("Plot saved at {}".format(plot_path))
    plt.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f",  help="path to file", type=str,   required=True)
    parser.add_argument("-m",  help="min colorbar", type=float, required=False, default=0)
    parser.add_argument("-M",  help="max colorbar", type=float, required=False, default=8)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: {}".format(domains.keys()),\
                        type=str, required=True)
    parser.add_argument("-s", help="simulator", type=str, required=True)
    args = parser.parse_args()
    

    fin = args.f
    reg = args.rg
    lat_min, lat_max, lon_min, lon_max = domains[reg]
    vmin = args.m
    vmax = args.M
    sim = args.s

    generate_hist_period(fin, lat_min, lat_max, lon_min, lon_max, vmin, vmax, reg, sim)
