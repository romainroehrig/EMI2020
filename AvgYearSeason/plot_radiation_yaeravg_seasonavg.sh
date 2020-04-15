#!/bin/sh

#########################
# OPTIONS
#########################

# Directory where to find simulation file
DIRIN=/Volumes/CNRM/TMP/simulations/EMI2020/AAD50-2.21c_v3/M/
EXT=_MED-44_ECMWF-ERAINT_evaluation_r1i1p1f2_CNRM-ALADIN64_v1_mon_200701-201612.nc

# Directory where to save plots
DIROUT=./quicklooks/

#########################
# Main part of the script
#########################

cat << EOF > config.py
repout = '$DIROUT'
EOF

######### YEAR #########
# TOA
./plot_lw_sw_toa.py -f1 rlut$EXT -f2 rlutcs$EXT -t LW -m 0 -M 40
./plot_lw_sw_toa.py  -f1 rsut$EXT -f2 rsutcs$EXT -t SW -m -80 -M 15
./plot_net_toa.py -f1 rsut$EXT -f2 rsutcs$EXT -f3 rlut$EXT -f4 rlutcs$EXT -m -50 -M 15 -t Net

# Surface
./plot_lw_sw_surface.py -f1 rlus$EXT  -f2 rlds$EXT  -f3 rluscs$EXT  -f4 rldscs$EXT  -t LW -m 0 -M 50
./plot_lw_sw_surface.py -f1 rsus$EXT  -f2 rsds$EXT  -f3 rsuscs$EXT  -f4 rsdscs$EXT  -t SW -m -90 -M 15
./plot_net_surface.py -f1 rsus$EXT -f2 rsds$EXT -f3 rsuscs$EXT -f4 rsdscs$EXT -f5 rlus$EXT -f6 rlds$EXT -f7 rluscs$EXT -f8 rldscs$EXT -t Net -m -50 -M 15


######### SEASON ##########
# TOA
./plot_season_lw_sw_surface.py -f1 rlus$EXT -f2 rlds$EXT -f3 rluscs$EXT -f4 rldscs$EXT -t LW -m 0 -M 60
./plot_season_lw_sw_surface.py -f1 rsus$EXT -f2 rsds$EXT -f3 rsuscs$EXT -f4 rsdscs$EXT -t SW -m -140 -M 20
./plot_season_net_toa.py -f1 rsut$EXT -f2 rsutcs$EXT -f3 rlut$EXT -f4 rlutcs$EXT -t Net -m -120 -M 30 

# Surface
./plot_season_lw_sw_toa.py  -f1 rlut$EXT -f2 rlutcs$EXT -t LW -m 0 -M 50
./plot_season_lw_sw_toa.py  -f1 rsut$EXT -f2 rsutcs$EXT -t SW -m -130 -M 20  
./plot_season_net_surface.py -f1 rsus$EXT -f2 rsds$EXT -f3 rsuscs$EXT -f4 rsdscs$EXT -f5 rlus$EXT -f6 rlds$EXT -f7 rluscs$EXT -f8 rldscs$EXT -t Net -m -120 -M 40



