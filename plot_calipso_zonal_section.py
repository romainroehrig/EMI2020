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
from sections import zonal_sections

def generate_calipso_zonal_section(fin, lat, vmin, vmax, reg):

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

    lats = d['lat'][:,:]
    sh = lats.shape
    m = find_lat(lat,lats)

    data = d[var][:,:,:,:]
    data = data[:,:,m,range(0,sh[1])]
    name = d[var].long_name
    units = d[var].units
    lons = d['lon'][:,:]
    lons = lons[m,range(0,sh[1])]
    alt40 = d['alt40'][:]/1000. # from m to km

    # Close netcdf file
    d.close()
    
    # Temporal mean
    data_moy = np.nanmean(data,axis=0)
    
    #####################
    # Plot data
    
    
    # Plot data
    a, b = np.meshgrid(lons, alt40)
    plt.pcolormesh(a,b,data_moy, vmin=vmin, vmax=vmax, cmap=cm.gist_ncar)
    plt.title('{0} ({1})\n{2} (lat={3:3.1f}) [2007-2016]'.format(name,units,reg.replace("_", " ").title(),lat))
    plt.xlabel('Longitude (deg)')
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
    #parser.add_argument("-lat", help="latitude", type=float, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=False, default=0)
    parser.add_argument("-M", help="max colorbar", type=float, required=False, default=100)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean or sahara", type=str, required=True)
    args = parser.parse_args()

    fin = args.f
    reg = args.rg
    lat = zonal_sections[reg]
    #lat = args.lat
    vmin = args.m
    vmax = args.M
    
    generate_calipso_zonal_section(fin, lat, vmin, vmax, reg)
