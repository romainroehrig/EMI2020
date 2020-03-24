#!/bin/sh

#########################
# OPTIONS
#########################

# Directory where to find simulation file
DIRIN=/Volumes/CNRM/TMP/simulations/EMI2020/AAD50-2.21c_v3/M/

var_alb='albisccp'
var_tau='tauisccp tautmodis'
var_pct='pctisccp pctmodis'
var_cl='cltisccp cltmodis cllmodis clmmodis clhmodis cltcalipso cllcalipso clmcalipso clhcalipso cltcalipsoice cltcalipsoliq clt cltl cltm clth'

EXT=_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc

# Directory where to save plots
DIROUT=./quicklooks/

#########################
# Main part of the script
#########################

cat << EOF > config.py
repout = '$DIROUT'
EOF

# Maps albedo
./plot_yearavg.py -f $DIRIN$var_alb$EXT -m 0 -M 1  
./plot_seasonavg.py -f $DIRIN$var_alb$EXT -m 0 -M 1 

# Maps optical thickness
for var in $var_tau
do
    ./plot_yearavg.py -f $DIRIN$var$EXT -m 0 -M 30
    ./plot_seasonavg.py -f $DIRIN$var$EXT -m 0 -M 30
done

# Maps top cloud pressure
for var in $var_pct
do
    ./plot_yearavg.py -f $DIRIN$var$EXT -m 300 -M 900
    ./plot_seasonavg.py -f $DIRIN$var$EXT -m 300 -M 900
done

# Maps cloud fraction
for var in $var_cl
do
    ./plot_yearavg.py -f $DIRIN$var$EXT -m 0 -M 100 
    ./plot_seasonavg.py -f $DIRIN$var$EXT -m 0 -M 100 
done
