# Uses several functions to scale the opensim model to fit the Human Body Library model


import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

import sys
sys.path.insert(0, "Functions")

import opensim as osim
import model_scaler as ms




# Load unscaled OpenSim model and Human Body library model
scaling_factors = [["bone",1.1],["bone2",1.1]]
mass = 70
height = 1700
scaler = ms.model_scaler("Main\Set-up\DAS3\das3.osim","test\test", scaling_factors, mass, height)




# Compare the two to get the scaling factors


# Create setup file for scaling
scaler.make_setup_file()


# Scale the model
scaler.scale_model()