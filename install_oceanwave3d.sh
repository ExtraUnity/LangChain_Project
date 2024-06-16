#!/bin/bash
set -e
git clone https://github.com/apengsigkarup/OceanWave3D-Fortran90.git || true
cd OceanWave3D-Fortran90
git switch botp
cd docker
cp ../../ThirdPartyLibs/Harwell.tar.gz Harwell.tar.gz
cp ../../ThirdPartyLibs/lapack-3.12.0.tar.gz lapack-3.12.0.tar.gz
cp ../../ThirdPartyLibs/SPARSKIT2.tar.gz SPARSKIT2.tar.gz
docker build --no-cache -t docker_oceanwave_final .