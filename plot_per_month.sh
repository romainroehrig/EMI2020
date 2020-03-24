#!/bin/bash

#########################
# OPTIONS
#########################

# Directory where to find simulation file
DIRIN=/Volumes/CNRM/TMP/simulations/EMI2020/AAD50-2.21c_v3/M/ 

var_modis=(cltmodis cllmodis clmmodis clhmodis pctmodis tautmodis)
var_calipso=(cltcalipso cllcalipso clmcalipso clhcalipso cltcalipsoice cltcalipsoliq)
var_aladin=(clt cltl cltm clth)
var_isccp=(cltisccp albisccp pctisccp tauisccp)

EXT=_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc

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

for dom in $domains
do
    ./plot_clt_month_box.py -f $DIRIN1${var_calipso[0]}$EXT $DIRIN1${var_calipso[1]}$EXT $DIRIN1${var_calipso[2]}$EXT $DIRIN1${var_calipso[3]}$EXT -rg $dom
    ./plot_clt_month_box.py -f $DIRIN2${var_modis[0]}$EXT $DIRIN2${var_modis[1]}$EXT $DIRIN2${var_modis[2]}$EXT $DIRIN2${var_modis[3]}$EXT -rg $dom
    ./plot_clt_month_box.py -f $DIRIN3${var_aladin[1]}$EXT $DIRIN3${var_aladin[2]}$EXT $DIRIN3${var_aladin[3]}$EXT $DIRIN3${var_aladin[4]}$EXT -rg $dom
done





































