# LangChain_Project

## Instructions for running the development environment
-  Download and install Anaconda from https://www.anaconda.com/download
    - On Windows, you need to add the bin folder to your PATH environment variable
    - On Linux, navigate to the Download folder, open terminal and run "bash Anaconda3-<LATEST_VERSION>-Linux-x86_64.sh",
      during installation there will be an option to add conda-init to PATH. Finally in terminal, run ~/.bashrc to source.
-  Download the repository from this GitHub
    - Navigate to this directory in CMD (Windows) or Bash (Mac or Linux)
-  Create the Conda environment by running the command:
     ```
      conda env create -n <env_name> -f environment.yaml
     ```
-  Activate the environment by running the command:
    ```
    conda activate <env_name>
    ```

### Installing docker
To run the OceanWave3D simulation you need docker installed and running.
You can download docker from docker from:
https://docs.docker.com/get-docker/

- On Linux, you also need to add docker to the user group in order for the program scripts to run docker commands
    ```
        sudo usermod -aG docker $USER
    ```

## Export environment to yaml
If you want to install a package and add it to the environment, run the 'conda env' command
given below depending on your system OS:

### For Windows
```
    conda env export --no-builds | findstr -v "^prefix: " > environment.yaml
```

### For Mac/Linux
```
    conda env export --no-builds | grep -v "^prefix: " > environment.yaml
```


## Update environment from yaml
If you want to refresh your own environment, after packages has been added to the environment:
```
    conda env update -n <env_name> -f environment.yaml --prune
```

## Running Flask Web GUI
To open the application GUI.

### For Windows
Make sure you are in the project folder directory "LANGCHAIN_PROJECT".
Then run the runflask.ps1 powershell script by entering:

```
.\runflask.ps1
```


### For Mac/Linux
Make sure you are in the project folder directory "LANGCHAIN_PROJECT".
Then run the runflask.sh bash script by entering:

```
./runflask.sh
```

## Visualizing OceanWave3D output
In order to visualize the output of the simulations, you need to have MATLAB 2024a installed. This can be downloaded from:
https://se.mathworks.com/downloads/