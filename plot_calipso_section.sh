#!/bin/sh

#########################
# OPTIONS
#########################

# Directory where to find simulation file
DIRIN=/Volumes/CNRM/TMP/simulations/EMI2020/AAD50-2.21c_v3/M/
#DIRIN=../calipso

# File extension
EXT=_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc

# variable list
variables='clcalipso clcalipsoice clcalipsoliq'

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

# MERIDIAN

for sec in $meridian_sections
do
  for var in $variables
  do
    echo "Meridian:" $sec"," $var 
    ./plot_calipso_meridian_section.py -f $DIRIN$var$EXT -rg $sec
  done
done

# ZONAL

for sec in $zonal_sections
do
  for var in $variables
  do
    echo "Zonal:" $sec"," $var
    ./plot_calipso_zonal_section.py -f $DIRIN$var$EXT -rg $sec
  done
done

