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

def generate_meridian_section(fin1, fin2, fin3, lon, vmin, vmax, reg, sim_mod):

    # Where to save images
    # If the directory does not exist, we create it
    rep0 = config.repout
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'yearavg')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)
    
    file_name1 = os.path.basename(fin1)
    file_name2 = os.path.basename(fin2)
    file_name3 = os.path.basename(fin3)

    var1 = file_name1.split("_")[0]
    var2 = file_name2.split("_")[0]    
    var3 = file_name3.split("_")[0]
    
    # Open file as a dataset
    d1 = nc.Dataset(fin1)
    d2 = nc.Dataset(fin2)
    d3 = nc.Dataset(fin3)
    
    # Read data, latitude, longitude, time
    time = d1['time'][:]
    lons = d1['lon'][:,:]
    sh = lons.shape
    m = find_lon(lon,lons)

    data1 = d1[var1][:,:,:]
    data2 = d2[var2][:,:,:]
    data3 = d3[var3][:,:,:]
    
    data1 = data1[:,range(0,sh[0]),m]
    data2 = data2[:,range(0,sh[0]),m]
    data3 = data3[:,range(0,sh[0]),m]

    lats = d1['lat'][:,:]
    lats = lats[range(0,sh[0]),m]
    
    data = np.zeros((len(time),len(range(0,sh[0])),3))
    
    for i in range(len(time)):
        data[i,:,0] = data1[i,:]
        data[i,:,1] = data2[i,:]
        data[i,:,2] = data3[i,:]
        
    d1.close()
    d2.close()
    d3.close()
       
    data_moy = np.nanmean(data,axis=0)

    #######################
    # Plot data
    plt.figure(figsize=(20,3))
    z = np.array([0,3200,6600,10000])
    a, b = np.meshgrid(z,lats)
    plt.pcolormesh(b, a,data_moy,vmin=vmin,vmax=vmax,cmap=cm.gist_ncar)
    plt.title("Meridian vertical section {0} - Cloud Fraction (%)\n{1} (lon={2:3.1f}) [2007-2016]".format(sim_mod.upper(),reg.replace("_", " ").title(),lon))
    plt.xlabel("Latitude (deg)")
    plt.ylabel("Altitude (m)")
    
    # Add colorbar
    plt.colorbar()

    # Save in png
    var = "cl_frac"
    plot_name = '{}_{}_{}.png'.format(var, reg, sim_mod.lower())
    plot_path = os.path.join(rep1, plot_name)
    plt.savefig(plot_path, bbox_inches='tight')
    print("Plot saved at {}".format(plot_path))
    plt.close()
       

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f1", help="path to file 1", type=str, required=True)
    parser.add_argument("-f2", help="path to file 2", type=str, required=True)
    parser.add_argument("-f3", help="path to file 3", type=str, required=True)
    #parser.add_argument("-lon", help="longitude", type=float, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=False, default=0)
    parser.add_argument("-M", help="max colorbar", type=float, required=False, default=100)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean or sahara", type=str, required=True)
    parser.add_argument("-sm", help="simulator or model", type=str, required=True)
    args = parser.parse_args()

    fin1 = args.f1
    fin2 = args.f2
    fin3 = args.f3
    reg = args.rg
    lon = meridian_sections[reg]
    #lon = args.lon
    vmin = args.m
    vmax = args.M
    sim_mod = args.sm

    generate_meridian_section(fin1, fin2, fin3, lon, vmin, vmax, reg, sim_mod)
