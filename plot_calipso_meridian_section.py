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

def generate_calipso_zonal_section_period(fin, ind_lon, vmin, vmax, reg):

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
    
    # Read data, latitude, longitude, time
    data = d[var][:,:,:,ind_lon]
    name = d[var].long_name
    units = d[var].units
    lat = d['lat'][:,ind_lon]
    alt40 = d['alt40'][:]
    d.close()
    
    # Temporal mean
    data_moy = np.nanmean(data,axis=0)
    
    #PLOTS
    plt.title('{0} ({1}) - {2} - 2007 to 2016'.format(name,units, reg.replace("_", " ").title()))
    
    # Plot data
    a, b = np.meshgrid(lat, alt40)
    plt.pcolormesh(a,b,data_moy, vmin=vmin, vmax=vmax, cmap=cm.gist_ncar)
    plt.xlabel('Latitude (deg)')
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
    parser.add_argument("-ilon", help="indice fixed longitude for the section", type=float, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=True)
    parser.add_argument("-M", help="max colorbar", type=float, required=True)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean or sahara", type=str, required=True)
    args = parser.parse_args()

    fin = args.f
    ind_lon = args.ilon
    vmin = args.m
    vmax = args.M
    reg = args.rg
    
    generate_calipso_zonal_section_period(fin, ind_lon, vmin, vmax, reg)
