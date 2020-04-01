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
from sections import meridian_sections

def generate_meridian_section(fins, lon, vmin, vmax, reg, sim_mod):

    # Where to save images
    # If the directory does not exist, we create it
    rep0 = config.repout
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'yearavg')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)
    
    data_all = None

    for id,f in enumerate(fins):
        file_name = os.path.basename(f)
        var = file_name.split("_")[0]
    
    # Open file as a dataset
        d = nc.Dataset(f)
    
    # Read data, latitude, longitude, time
        time = d['time'][:]
        lons = d['lon'][:,:]
        sh = lons.shape
        m = find_lon(lon,lons)

        data = d[var][:,:,:]
        data = data[:,range(0,sh[0]),m]

        lats = d['lat'][:,:]
        lats = lats[range(0,sh[0]),m]
        
        d.close()

        # resize data as soon as we know the required dimensions
        if id == 0:
            data_all = np.zeros((len(time),len(range(0,sh[0])),3))
    
        for i in range(len(time)):
            data_all[i,:,id] = data[i,:]
            
        
    data_moy = np.nanmean(data_all,axis=0)

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
    parser.add_argument("-f", nargs="+", help="list of files", type=str, required=True)
    #parser.add_argument("-lon", help="longitude", type=float, required=True)
    parser.add_argument("-m", help="min colorbar", type=float, required=False, default=0)
    parser.add_argument("-M", help="max colorbar", type=float, required=False, default=100)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean or sahara", type=str, required=True)
    parser.add_argument("-sm", help="simulator or model", type=str, required=True)
    args = parser.parse_args()

    fins = args.f
    reg = args.rg
    lon = meridian_sections[reg]
    #lon = args.lon
    vmin = args.m
    vmax = args.M
    sim_mod = args.sm

    generate_meridian_section(fins, lon, vmin, vmax, reg, sim_mod)
