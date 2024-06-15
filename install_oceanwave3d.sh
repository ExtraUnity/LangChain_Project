#!/bin/bash
set -e
cd ../OceanWave3D-Fortran90/docker #Clone repository instead
docker build --no-cache -t docker_oceanwave3d .