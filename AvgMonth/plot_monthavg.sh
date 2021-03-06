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
    # plot cloud fraction (tot, low, mid, high) for calipso, modis and aladin
    ./plot_monthavg.py -f $DIRIN${var_calipso[0]}$EXT $DIRIN${var_calipso[1]}$EXT $DIRIN${var_calipso[2]}$EXT $DIRIN${var_calipso[3]}$EXT -m 0 -M 100 -rg $dom -namefig cl_frac_calipso
    ./plot_monthavg.py -f $DIRIN${var_modis[0]}$EXT $DIRIN${var_modis[1]}$EXT $DIRIN${var_modis[2]}$EXT $DIRIN${var_modis[3]}$EXT -m 0 -M 100 -rg $dom -namefig cl_frac_modis
    #./plot_monthavg.py -f $DIRIN${var_aladin[1]}$EXT $DIRIN${var_aladin[2]}$EXT $DIRIN${var_aladin[3]}$EXT $DIRIN${var_aladin[4]}$EXT -m 0 -M 100 -rg $dom -namefig cl_frac_aladin

    # plot pct for modis and isccp
    ./plot_monthavg.py -f $DIRIN${var_modis[4]}$EXT $DIRIN${var_isccp[2]}$EXT -m 900 -M 200 -rg $dom -namefig pct_modis_isccp
    
    # plot tau for modis ans isccp
    ./plot_monthavg.py -f $DIRIN${var_modis[5]}$EXT $DIRIN${var_isccp[3]}$EXT -m 0 -M 30 -rg $dom -namefig tau_modis_isccp
done





































