#!/bin/bash
#This file is made by Christian
set -e
cd OceanWave3D-Fortran90/docker
cp ../examples/inputfiles/$1 OceanWave3D.inp
chmod +x run_oceanwave3d.sh
./run_oceanwave3d.sh OceanWave3D.inp