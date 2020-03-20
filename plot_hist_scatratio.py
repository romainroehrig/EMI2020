#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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

def generate_scat_period(fin, lat_min, lat_max, lon_min, lon_max, vmin, vmax, reg, sim):

    # Where to save images
    # If the directory does not exist, we create it
    rep0 = config.repout
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'yearavg')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)
        
    file_name = os.path.basename(fin)
    var = file_name.split("_")[0]
    
    # Open file as a dataset
    d = nc.Dataset(fin)
    
    # Prepare histogram axes
    scatratio_bounds = d['scatratio_bounds'][3:,:]
    nscatratio, nb = scatratio_bounds.shape 
    alt40_bounds = d['alt40_bounds'][:-7,:]/1000.
    nalt40, nb = alt40_bounds.shape

    scatratiob = np.zeros(nscatratio+1)
    scatratiob[0:nscatratio] = scatratio_bounds[0:nscatratio,0]
    scatratiob[nscatratio] = scatratio_bounds[nscatratio-1,1]

    xaxis = np.arange(0,nscatratio+1)

    alt40b = np.zeros(nalt40+1)
    alt40b[0:nalt40] = alt40_bounds[0:nalt40,0]
    alt40b[nalt40] = alt40_bounds[nalt40-1,1]

    
    
    # Read latitude, longitude
    lat = d['lat'][:,:]
    lon = d['lon'][:,:]

    # find coords of nearest point in grid from point (TARGET_LAT, TARGET_LON)
    target_x = []
    target_y = []

    nlat,nlon = lat.shape
    for x in range(nlon):
        for y in range(nlat):
            if lat[y,x]>=lat_min and lat[y,x]<=lat_max and lon[y,x]>=lon_min and lon[y,x]<=lon_max:
                target_x.append(x)
                target_y.append(y)
    data = d[var][:,3:,:-7,min(target_y):max(target_y),min(target_x):max(target_x)]

    # Close netcdf file
    d.close()

    # Temporal mean
    data_moy = np.nanmean(data,axis=(0,3,4))
    
    ####################
    # Plot data
    a, b = np.meshgrid(alt40b, xaxis)
    plt.pcolormesh(b,a,data_moy, vmin=vmin, vmax=vmax, cmap=cm.terrain)
    
    # X axis
    plt.xticks(xaxis[:-1],['{0:3d}'.format(int(x)) for x in scatratiob[:-1]])
    plt.xlabel('Scattering ratio')
    # Y axis
    plt.yticks((0,5,10,15))
    plt.ylabel('Altitude (km)')
    # display grid
    plt.grid(color='k', linestyle='--', linewidth=1)
    # Title
    plt.title('{0} Cloud Fraction (%)\n{1} [2007-2016]'.format(sim, reg.replace("_", " ").title()))
    
    # Add colorbar
    plt.colorbar()

    # Save in png
    plot_name = '{}_{}.png'.format(var, reg)
    plot_path = os.path.join(rep1, plot_name)
    plt.savefig(plot_path, bbox_inches='tight')
    print("Plot saved at {}".format(plot_path))
    plt.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="path to file", type=str, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=False, default=0)
    parser.add_argument("-M", help="max colorbar", type=float, required=False, default=0.08)
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

    generate_scat_period(fin, lat_min, lat_max, lon_min, lon_max, vmin, vmax, reg, sim)
