# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Point python where to find the source code for the class 

import sys
sys.path.insert(0, "Functions")


# Import opensim and other used libraries
import opensim as osim
import numpy as np
from sklearn.linear_model import LinearRegression
import Generate_force_files as fs
import Generate_stationary_kinematics_MOBL as sk
import sta_op_tendon_comp as so
import Static_op_moments as st
import SRS_Mobl_arms as ma
np.set_printoptions(threshold=sys.maxsize)




# Initialise model and state and set coordinate angle
model = osim.Model(r"Main\Set-up\Moblarms\MOBL_ARMS.osim")

state = model.initSystem()

# Define state as wanted



# Calculate coordinate angles in both radians and degrees
  
elv_angle_deg = round(state.getY()[10]*180/np.pi,1)
shoulder_elv_deg = round(state.getY()[11]*180/np.pi,1)
shoulder_rot_deg = round(state.getY()[13]*180/np.pi,1)
elbow_flexion_deg = round(state.getY()[14]*180/np.pi,1)
elv_angle_rad = state.getY()[10]
shoulder_elv_rad = state.getY()[11]
shoulder_rot_rad = state.getY()[13]
elbow_flexion_rad = state.getY()[14]
  

# Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)

    
# Find the related coordinates of the Mobl_arms model
position_file.find_related_coor()

# Write the initial position and stationary kinematics file
file_name = position_file.stat_kine_file_H()


# Create a static optimisation with the actuators at the joints
st.do_stat_op("Main\Set-up\Moblarms\stat_op_setup.xml",file_name)

# Find the activations using the static optimisation with tendon compliance
activation = so.loop_fibre_length(model,state)


# Store activations and add a one at the beginning of the array representing passive effects
activations = [1]
for ac in activation:
    activations.append(ac.value)

Fmax, M, H = ma.calc_H_Mobl(model,state,activations)



