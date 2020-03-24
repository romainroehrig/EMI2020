#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import argparse

import netCDF4 as nc

import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt
from matplotlib import cm

import config
from var_legend import var_legend
from domains import domains
from myfunctions import *

def generate_per_month(fins, lat_min, lat_max, lon_min, lon_max, min_yaxis, max_yaxis, reg):
    # Where to save images
    # If the directory does not exist, we create it
    rep0 = config.repout
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    rep1 = os.path.join(rep0, 'monthavg')
    if not(os.path.exists(rep1)):
        os.makedirs(rep1)

    # config for plotting
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    plt.figure(figsize=(9,6))
    color_list = ['k','r','m','g']
    legend = []


    for id,f in enumerate(fins):
        file_name = os.path.basename(f)
        var = file_name.split("_")[0]
    
        # Open file as a dataset
        d = nc.Dataset(f)
    
        # Read data, latitude, longitude, time
        data = d[var][:,:,:] # time, latitude, longitude
        name = d[var].long_name
        units = d[var].units
        lat = d["lat"][:,:]
        lon = d["lon"][:,:]

        d.close()

        nt,nlat,nlon = data.shape
    
        # find coords of nearest point in grid from point (TARGET_LAT, TARGET_LON)
        target_x = []
        target_y = []
 
        for x in range(nlon):
            for y in range(nlat):
                if lat[y,x]>=lat_min and lat[y,x]<=lat_max and lon[y,x]>=lon_min and lon[y,x]<=lon_max:
                    target_x.append(x)
                    target_y.append(y)
                
        # Temporal mean - season
        data_month=[0,0,0,0,0,0,0,0,0,0,0,0]
        data_month_moy=[0,0,0,0,0,0,0,0,0,0,0,0]
    

        for i in range(10):
            for j in range(12):
                for k in range(len(target_x)):
                    data_month[j] = data_month[j] + data[j+12*i,target_y[k],target_x[k]] 
                
        for j in range(12):
            data_month_moy[j]= data_month[j]/(len(target_x)*10)
            
        data_month_moy_array = np.array(data_month_moy)
    
        
        # Plot data
        legend.append(var_legend[var])  
        plt.plot(months,data_month_moy_array,color_list[id])
    
    plt.legend(legend)
    plt.title('{} ({}) - {}\n[2007-2016]'.format(name, units, reg.replace("_", " ").title()))
    plt.xlabel('Month')
    plt.ylabel('{} ({})'.format(name, units))
    plt.ylim(min_yaxis, max_yaxis)
    plt.grid()
    
    # Save in png
    identity = "cl_fraction_{}".format(
    plot_name = '{}_{}.png'.format(identity, reg)
    plot_path = os.path.join(rep1, plot_name)
    plt.savefig(plot_path, bbox_inches='tight')
    print("Plot saved at {}".format(plot_path))
    plt.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", nargs="+", help="list of files to plot", type=str, required=True)
    parser.add_argument("-m", help="min y-axis", type=float, default=0, required=False )
    parser.add_argument("-M", help="max y-axis", type=float, default=100, required=False)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean", type=str, required=True)
    args = parser.parse_args()
    

    fins = args.f
    reg = args.rg
    lat_min, lat_max, lon_min, lon_max = domains[reg]
    min_yaxis = args.m
    max_yaxis = args.M

    generate_per_month(fins, lat_min, lat_max, lon_min, lon_max, min_yaxis, max_yaxis, reg)
