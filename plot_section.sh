#!/bin/bash

#########################
# OPTIONS
#########################

# Directory where to find simulation file
#DIRIN=/Volumes/CNRM/TMP/simulations/EMI2020/AAD50-2.21c_v3/M/
DIRIN1=../calipso/
DIRIN2=../modis/

# File extension
EXT=_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc

# variable list
calipso=(cllcalipso clmcalipso clhcalipso)
modis=(cllmodis clmmodis clhmodis)
aladin=(cltl cltm clth)

# Sections to plot (available sections are defined in sections.py)
meridian_sections='atlantic_ocean eastern_europe_sahara western_europe_sahara'
zonal_sections='mediterranean northern_europe sahara'

# Directory where to save plots
DIROUT=./quicklooks/

#########################
# Main part of the script
#########################

cat << EOF > config.py
repout = '$DIROUT'
EOF

# # MERIDIAN

for sec in $meridian_sections
do
    echo "Meridian:" $sec
    ./plot_section_meridian.py -f1 $DIRIN1${calipso[0]}$EXT -f2 $DIRIN1${calipso[1]}$EXT -f3 $DIRIN1${calipso[2]}$EXT -rg $sec -sm calipso
    ./plot_section_meridian.py -f1 $DIRIN2${modis[0]}$EXT -f2 $DIRIN2${modis[1]}$EXT -f3 $DIRIN2${modis[2]}$EXT -rg $sec -sm modis
    #./plot_section_zonal.py -f1 $DIRIN${aladin[0]}$EXT -f2 $DIRIN${aladin[1]}$EXT -f3 $DIRIN${aladin[2]}$EXT-rg $sec -sm aladin
done

# ZONAL

for sec in $zonal_sections
do
    echo "Zonal:" $sec
    ./plot_section_zonal.py -f1 $DIRIN1${calipso[0]}$EXT -f2 $DIRIN1${calipso[1]}$EXT -f3 $DIRIN1${calipso[2]}$EXT -rg $sec -sm calipso
    ./plot_section_zonal.py -f1 $DIRIN2${modis[0]}$EXT -f2 $DIRIN2${modis[1]}$EXT -f3 $DIRIN2${modis[2]}$EXT -rg $sec -sm modis
    #./plot_section_zonal.py -f1 $DIRIN${aladin[0]}$EXT -f2 $DIRIN${aladin[1]}$EXT -f3 $DIRIN${aladin[2]}$EXT -rg $sec -sm "aladin"
done
