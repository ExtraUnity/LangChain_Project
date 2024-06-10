#!/bin/bash
set -e
cd ../OceanWave3D-Fortran90/docker
docker build --no-cache -t docker_oceanwave3d .