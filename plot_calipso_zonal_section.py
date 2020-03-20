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

def generate_calipso_zonal_section(fin, ind_lat, vmin, vmax, reg):

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
    data = d[var][:,:,ind_lat,:]
    name = d[var].long_name
    units = d[var].units
    lon = d['lon'][ind_lat,:]
    alt40 = d['alt40'][:]

    # Close netcdf file
    d.close()
    
    # Temporal mean
    data_moy = np.nanmean(data,axis=0)
    
    #####################
    # Plot data
    
    
    # Plot data
    a, b = np.meshgrid(lon, alt40)
    plt.pcolormesh(a,b,data_moy, vmin=vmin, vmax=vmax, cmap=cm.gist_ncar)
    plt.title('{0} ({1}) - {2}\n[2007-2016]'.format(name,units,reg.replace("_", " ").title()))
    plt.xlabel('Longitude (deg)')
    plt.ylabel('Altitude (m)')
    
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
    #parser.add_argument("-ilat", help="indice fixed latitude for the section", type=float, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=False, default=0)
    parser.add_argument("-M", help="max colorbar", type=float, required=False, default=100)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean or sahara", type=str, required=True)
    args = parser.parse_args()

    fin = args.f
    reg = args.rg
    ind_lat = zonal_sections[reg]
    #ind_lat = args.ilat
    vmin = args.m
    vmax = args.M
    
    generate_calipso_zonal_section(fin, ind_lat, vmin, vmax, reg)
