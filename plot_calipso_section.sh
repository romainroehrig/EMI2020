#!/bin/sh

#########################
# OPTIONS
#########################

# Directory where to find simulation file
#DIRIN=/Volumes/CNRM/TMP/simulations/EMI2020/AAD50-2.21c_v3/M/
DIRIN=../calipso

# Simulation file for CALIPSO ice fraction (section)
FILEICE=$DIRIN/clcalipsoice_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc
# Simulation file for CALIPSO liq fraction (section)
FILELIQ=$DIRIN/clcalipsoliq_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc
# Simulation file for CALIPSO tot fraction (section)
FILETOT=$DIRIN/clcalipso_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc

# Sections to plot (available sections are defined in sections.py)
meridian_sections='atlantic_ocean eastern_europe_sahara western_europe_sahara'
zonal_sections='mediterranean northen_europe sahara'

# Directory where to save plots
DIROUT=./quicklooks/

#########################
# Main part of the script
#########################

cat << EOF > config.py
repout = '$DIROUT'
EOF

# MERDIAN

for sec in $meridian_sections
do
  echo "Meridian:" $sec 
  ./plot_calipso_meridian_section.py -f $FILEICE -rg $sec
  ./plot_calipso_meridian_section.py -f $FILELIQ -rg $sec
  ./plot_calipso_meridian_section.py -f $FILETOT -rg $sec
done

# ZONAL

for sec in $zonal_sections
do
  echo "Zonal:" $sec
  
  ./plot_calipso_zonal_section.py -f $FILEICE -rg $sec
  ./plot_calipso_zonal_section.py -f $FILELIQ -rg $sec
  ./plot_calipso_zonal_section.py -f $FILETOT -rg $sec
done

