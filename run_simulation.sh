#!/bin/bash
set -e
cd OceanWave3D-Fortran90/docker
cp ../examples/inputfiles/$1 OceanWave3D.inp
chmod +x run_oceanwave3d.sh
./run_oceanwave3d.sh OceanWave3D.inp

# #!/bin/bash
# # This script runs the Docker container for docker_oceanwave_final, mounting the current directory.
# #
# # By Allan P. Engsig-Karup, apek@dtu.dk.
# #
# # Example: (put the OceanWave3D.inp file in the current directory that is mounted to the docker container for it to access it)
# # ./run_oceanwave3d.sh OceanWave3D.inp

# # Path to the input file on the host
# host_input_file="$(pwd)/$1"

# # Path where the container expects the input file
# container_input_path="/build/OceanWave3D.inp"
# echo "Mount path"
# echo "$(pwd)/$1"
# docker run --name oceanwave3d-container -it -v "$host_input_file":"$container_input_path" docker_oceanwave3d
# docker start oceanwave3d-container
# docker exec oceanwave3d-container bash -c "cd /build && tar czf ep_files.tar.gz EP*"
# mkdir -p data
# rm -r data/*
# docker cp oceanwave3d-container:/build/ep_files.tar.gz "$(pwd)/data"
# cd data/
# tar xzf ep_files.tar.gz
# docker stop oceanwave3d-container
# docker rm oceanwave3d-container