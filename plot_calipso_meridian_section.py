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
from sections import meridian_sections

def generate_calipso_meridian_section(fin, lon, vmin, vmax, reg):

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
    
    # Read data, latitude, longitude, time

    lons = d['lon'][:,:]
    sh = lons.shape
    m = find_lon(lon,lons)

    data = d[var][:,:,:,:]
    data = data[:,:,range(0,sh[0]),m]
    name = d[var].long_name
    units = d[var].units
    lats = d['lat'][:,:]
    lats = lats[range(0,sh[0]),m]
    alt40 = d['alt40'][:]/1000. # from m to km

    # Close netcdf file
    d.close()
    
    # Temporal mean
    data_moy = np.nanmean(data,axis=0)
    
    #####################
    # Plot data
    a, b = np.meshgrid(lats, alt40)
    plt.pcolormesh(a,b,data_moy, vmin=vmin, vmax=vmax, cmap=cm.gist_ncar)
    plt.title('{0} ({1})\n{2} (lon={3:3.1f}) [2007-2016]'.format(name,units, reg.replace("_", " ").title(),lon))
    plt.xlabel('Latitude (deg)')
    plt.ylim(0,18)
    plt.ylabel('Altitude (km)')
    
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
    #parser.add_argument("-lon", help="longitude", type=float, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=False, default=0)
    parser.add_argument("-M", help="max colorbar", type=float, required=False, default=100)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean or sahara", type=str, required=True)
    args = parser.parse_args()

    fin = args.f
    reg = args.rg
    lon = meridian_sections[reg]
    #lon = args.lon
    vmin = args.m
    vmax = args.M

    generate_calipso_meridian_section(fin, lon, vmin, vmax, reg)
