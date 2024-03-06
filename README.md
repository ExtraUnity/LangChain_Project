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



## Export environment to yaml

### For Windows
```
    conda env export --no-builds | findstr -v "^prefix: " > environment.yaml
```

### For Mac/Linux
```
    conda env export --no-builds | grep -v "^prefix: " > environment.yaml
```

## Update environment from yaml
```
    conda env update -n <myenv> -f environment.yaml --prune
```