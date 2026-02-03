# OpenSim_code


## Description

Repository for code made for investigating the stiffness of a human arm using OpenSim


## Setup
In order to use the OpenSim library in python a few steps would need to be done in setup. For my instalation I used opensim 4.5 with python 3.8 The following steps are copied from the OpenSim documentation at: https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53085346/Scripting+in+Python

"-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
Manual installation (OpenSim 4.3 or later)
It is possible to manually install the OpenSim Python bindings, but this approach comes with a few caveats:

 If installing from a GUI distribution with OpenSim 4.3 or later, only Python 3.8 is supported.

While it is not necessary to use Conda to create a Python environment, you must use a 64-bit version of Python.

If you want to create a manual installation with a different version of Python, you must build the Python bindings from source.

The following instructions will refer to a directory <OPENSIM_INSTALL_DIR>, where you installed some version of OpenSim. On Windows this might look like C:\OpenSim 4.X, and on MacOS it might look like /Applications/OpenSim 4.X. The installation directory can be identified by the subfolders "bin" and "sdk". If you built from source on Mac or Linux, where the installation directory might use a Unix-like folder structure with subfolders "lib", "libexec", and "share".

To install, first navigate to the location of the OpenSim Python package within the OpenSim installation. If you are using OpenSim's GUI distribution, this location is <OPENSIM_INSTALL_DIR>/sdk/Python. If you built OpenSim from source on Mac or Linux, this location is likely <OPENSIM_INSTALL_DIR>/lib/python3.x/site-packages.

If on Windows, you may need to run the following command when using OpenSim 4.3 or later with Python 3.8. (If setup_win_python38.py does not exist in your distribution, then you can skip this step.)


$ python setup_win_python38.py


To install the OpenSim Python bindings on all platforms, run the following command. Note that if you have a Conda environment activated, this command with install OpenSim as a package into your Conda environment.


$ python -m pip install .


On Windows, you will likely need to set the Path environment variable to point to the "bin" folder in your OpenSim installation. To do this:

Press the Windows key and search for "Edit the system environment variables". Click the top search result.

Click "Environment Variables..." in the bottom right corner. Look for Path under "System variables".

Highlight the Path entry and click "Edit...".

Add a new entry with value <OPENSIM_INSTALL_DIR>/bin and move it to the top of the list.

Restart your terminal for the change to Path to take effect before testing your Python installation.

On Mac, you may need to update the DYLD_LIBRARY_PATH environment variable to point to the OpenSim and Simbody libraries. 


$ export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:<OPENSIM_INSTALL_DIR>/sdk/lib
$ export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:<OPENSIM_INSTALL_DIR>/sdk/Simbody/lib


You can place export commands in your ~/.bashrc file (or other terminal configuration file) so that they are set whenever you open up a new terminal.

Similarly on Linux, you may need to updated LD_LIBRARY_PATH.


$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<OPENSIM_INSTALL_DIR>/sdk/lib
$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:<OPENSIM_INSTALL_DIR>/sdk/Simbody/lib


Testing your installation 
After activating your Conda environment (or manually installed Python environment), run the following commands to test your OpenSim installation.


 python 
>>> import opensim as osim
>>> osim.GetVersionAndDate()


"----------------------------------------------------------------------------------------------------------------------------------------------------------------------------"

If these steps were executed correctly it should work. Sometimes the path environment to the bin folder does not work, for this reason these two lines are added at the beginning of each file containing code:


import os
os.add_dll_directory("C:/OpenSim 4.5/bin")


## Test_ankle

This folder contains a python script that runs a test for all important functions. If your environment is set up correctly it should result in the same graphs as found in the Resulting_figures folder.

## code_structure_new

This draw.io file contains a flowchart illustrating the order of the functions to use and what they output

## Functions

Folder containing the classes used for calculations

## Main

contains some code that uses the classes and the setup files and results from the experiments