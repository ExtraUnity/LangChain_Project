# LangChain_Project

## Instructions for running the development environment
In order to run the program correctly, you must have the following:
-   Created and activated the conda environment
-   Have docker installed and running
-   Install MATLAB and have an active license (only for visualization of output)


### Creating conda environment
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

### Installing MATLAB
In order to visualize the output of the simulations, you need to have MATLAB 2024a installed. This can be downloaded from:
https://se.mathworks.com/downloads/

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

