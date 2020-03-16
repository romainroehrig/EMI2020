#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os

import netCDF4 as nc

import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt
from matplotlib import cm

import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

from myfunctions import *

def generate_hist_all_period():

    # Where to save images
    rep0 = './quicklooks/'
    # If the directory does not exist, we create it
    if not(os.path.exists(rep0)):
        os.makedirs(rep0)
    
    # Projection for plotting
    proj = ccrs.LambertConformal(central_latitude = 37,
                                 central_longitude = 10,
                                 standard_parallels = (37, 37)
                                 )
    
    var = 'clisccp'
    
    # file to open
    fin = '{0}_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc'.format(var)
    
    # Open file as a dataset
    d = nc.Dataset(fin)
    lat_min = 37
    lat_max = 42.5
    lon_min = 3
    lon_max = 8.5
    
    # find coords of nearest point in grid from point (TARGET_LAT, TARGET_LON)
    
    target_x = []
    target_y = []
    
    # Read data, latitude, longitude, time
    
    
    name = d[var].long_name
    units = d[var].units
    lat = d['lat'][:,:]
    lon = d['lon'][:,:]
    tau = d['tau'][:]
    plev7 = d['plev7'][:]/100
    time = d['time'][:]

    dates = nc.num2date(d['time'][:],units=d['time'].units,calendar=d['time'].calendar)
    nlat,nlon = lat.shape
    for x in range(nlon):
        for y in range(nlat):
            if lat[y,x]>=lat_min and lat[y,x]<=lat_max and lon[y,x]>=lon_min and lon[y,x]<=lon_max:
                target_x.append(x)
                target_y.append(y)

    data = d[var][:,:,:,min(target_y):max(target_y),min(target_x):max(target_x)]
    
    d.close()
    
    print "target x {}".format(target_x)
    print "target y {}".format(target_y)

#    nt,nlat,nlon = data.shape
    print(lat[58,70])
    print(lon[58,70])
    
    print data.shape
    
    # Temporal mean
    data_moy = np.nanmean(data,axis=(0,3,4))
    # data_moy = np.resize(np.linspace(40*15,0,40*15),(15,40))
    
    #PLOTS
    plt.title('Cloud Fraction ISCCP - 2007 to 2016'.format(name,units))
    
    # Plot data
    
    a, b = np.meshgrid(plev7, tau)
    # a, b = np.meshgrid(np.linspace(0,41,40),np.linspace(0,16,15))

    # print "scatratio shape : {}".format(scatratio.shape)
    print "data_moy shape : {}".format(data_moy[:,:].shape)
    print "a shape : {}".format(data_moy[:,:].shape)
    print "b shape : {}".format(data_moy[:,:].shape)
    print "plev7 : {}".format(plev7)
    print "tau : {}".format(tau)
    print "b : {}".format(b)
    print "b : {}".format(b)
    print "datamoy : {}".format(data_moy)

    plt.pcolormesh(b,a,data_moy, cmap=cm.terrain)
    plt.xlabel('Optical Thickness (m)')
    plt.ylabel('Cloud Top Pressure (hPa)')
    
    # Add colorbar
    plt.colorbar()
    
    # Save in png
    print '{0}/period/{1}.png'.format(rep0,var)
    plt.xscale('log')
    plt.ylim(900,100)
    plt.savefig('{0}/period/{1}bis.png'.format(rep0,var),bbox_inches='tight')
    plt.close()

if __name__=="__main__":
    generate_hist_all_period()
