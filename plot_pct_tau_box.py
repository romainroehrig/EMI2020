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


def generate_hist_period(fin, lat_min, lat_max, lon_min, lon_max, vmin, vmax, reg, sim):

    # Where to save images
    # If the directory does not exist, we create it
    rep0 = './quicklooks'
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'period')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)
    
    file_name = os.path.basename(fin)
    var = file_name.split("_")[0]
    
    # Open file as a dataset
    d = nc.Dataset(fin)
    
    # find coords of nearest point in grid from point (TARGET_LAT, TARGET_LON)
    target_x = []
    target_y = []
    
    # Read data, latitude, longitude, time
    lat = d['lat'][:,:]
    lon = d['lon'][:,:]
    tau = d['tau'][:]
    plev7 = d['plev7'][:]/100

    nlat,nlon = lat.shape
    for x in range(nlon):
        for y in range(nlat):
            if lat[y,x]>=lat_min and lat[y,x]<=lat_max and lon[y,x]>=lon_min and lon[y,x]<=lon_max:
                target_x.append(x)
                target_y.append(y)
    data = d[var][:,:,:,min(target_y):max(target_y),min(target_x):max(target_x)]
    
    d.close()
    
    # Temporal mean
    data_moy = np.nanmean(data,axis=(0,3,4))
    
    #PLOTS
    # Plot data
    a, b = np.meshgrid(plev7, tau)
    plt.pcolormesh(b,a,data_moy, vmin=vmin, vmax=vmax, cmap=cm.terrain)
    plt.xlabel('Optical Thickness (m)')
    plt.ylabel('Cloud Top Pressure (hPa)')
    plt.xscale('log')
    plt.ylim(900,100)
    plt.title('Cloud Fraction (%) {} - {} - 2007 to 2016'.format(sim, reg.replace("_", " ").title()))
    
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
    parser.add_argument("-lt", help="lat min", type=float, required=True)
    parser.add_argument("-Lt", help="lat max", type=float, required=True)
    parser.add_argument("-lg", help="long min", type=float, required=True)
    parser.add_argument("-Lg", help="long max", type=float, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=True)
    parser.add_argument("-M", help="max colorbar", type=float, required=True)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean", type=str, required=True)
    parser.add_argument("-s", help="simulator", type=str, required=True)
    args = parser.parse_args()
    print(args.f)

    fin = args.f
    lat_min = args.lt
    lat_max = args.Lt
    lon_min = args.lg
    lon_max = args.Lg
    vmin = args.m
    vmax = args.M
    reg = args.rg
    sim = args.s

    generate_hist_period(fin, lat_min, lat_max, lon_min, lon_max, vmin, vmax, reg, sim)
