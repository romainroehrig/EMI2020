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

def generate_monthavg(fins, lat_min, lat_max, lon_min, lon_max, min_yaxis, max_yaxis, reg, namefig):
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
        
            
        # Plot data
        legend.append(var_legend[var])
        if var == "pctisccp" or var == "pctmodis":
        # if pct convert to hPa
            data_month_moy = [x/100 for x in data_month_moy] 
            units = "hPa"  
        plt.plot(months,data_month_moy,color_list[id])
    
    plt.legend(legend)

    simulators = ["isccp", "modis", "calipso"]
    for sim in simulators:
        var =  var.replace(sim,"")
    cl_frac = ["clt", "cltl", "cltm", "clth", "cll", "clm", "clh"]
    for i in range(len(cl_frac)):
        if var == cl_frac[i]:
            plt.title('Cloud Fraction ({}) - {}\n[2007-2016]'.format(units, reg.replace("_", " ").title()))
            plt.ylabel('Cloud Fraction ({})'.format(units))
        if var == "pct":
            plt.title('Cloud Top Pressure ({}) - {}\n[2007-2016]'.format(units, reg.replace("_", " ").title()))
            plt.ylabel('Cloud Top Pressure (hPa)')
        if var == "tau" or var == "taut":
            plt.title('Optical Thickness (-) - {}\n[2007-2016]'.format(reg.replace("_", " ").title()))
            plt.ylabel('Optical Thickness (-)')
    
    plt.xlabel('Month')
    plt.ylim(min_yaxis, max_yaxis)
    plt.grid()

    # Save in png
    plot_name = '{}_{}.png'.format(namefig, reg)
    plot_path = os.path.join(rep1, plot_name)
    plt.savefig(plot_path, bbox_inches='tight')
    print("Plot saved at {}".format(plot_path))
    plt.close()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", nargs="+", help="list of files to plot", type=str, required=True)
    parser.add_argument("-m", help="min y-axis", type=float, required=True )
    parser.add_argument("-M", help="max y-axis", type=float, required=True)
    parser.add_argument("-rg", help="region, underscore-separated lowercase, eg: atlantic_ocean", type=str, required=True)
    parser.add_argument("-namefig", help="name figure to save", type=str, required=True)
    args = parser.parse_args()
    

    fins = args.f
    reg = args.rg
    lat_min, lat_max, lon_min, lon_max = domains[reg]
    min_yaxis = args.m
    max_yaxis = args.M
    namefig = args.namefig

    generate_monthavg(fins, lat_min, lat_max, lon_min, lon_max, min_yaxis, max_yaxis, reg, namefig)
