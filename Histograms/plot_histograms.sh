#!/bin/sh

#########################
# OPTIONS
#########################

# Directory where to find simulation file
DIRIN=/Volumes/CNRM/TMP/simulations/EMI2020/AAD50-2.21c_v3/M/

# Simulation file for ISCCP histogram
FILEISCCP=$DIRIN/clisccp_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc
# Simulation file for MODIS histogram
FILEMODIS=$DIRIN/clmodis_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc
# Simulation file for CALIPSO histogram
FILECALIPSO=$DIRIN/cfadLidarsr532_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc

# Domains to plot (available domain are defined in domains.py)
domains='atlantic_ocean eastern_europe eastern_mediterranean eastern_sahara western_mediterranean western_sahara'

# Directory where to save plots
DIROUT=./quicklooks/

#########################
# Main part of the script
#########################

cat << EOF > config.py
repout = '$DIROUT'
EOF

### ANNUAL ###
# ISCCP histograms

for dom in $domains
do
  echo "ISCCP:" $dom 
  ./plot_hist_pct_tau.py -f $FILEISCCP -rg $dom -s ISCCP
done

# MODIS histograms

for dom in $domains
do
  echo "MODIS:" $dom	
  ./plot_hist_pct_tau.py -f $FILEMODIS -rg $dom -s MODIS
done

# CALIPSO histograms

for dom in $domains
do 
  echo "CALIPSO:" $dom
  ./plot_hist_scatratio.py -f $FILECALIPSO -rg $dom -s CALIPSO
done


### SEASON ###
# ISCCP histograms

for dom in $domains
do
  echo "ISCCP:" $dom 
  ./plot_hist_pct_tau_seasonavg.py -f $FILEISCCP -rg $dom -s ISCCP
done

# MODIS histograms

for dom in $domains
do
  echo "MODIS:" $dom 
  ./plot_hist_pct_tau_seasonavg.py -f $FILEMODIS -rg $dom -s MODIS
done