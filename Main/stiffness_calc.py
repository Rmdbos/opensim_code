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
import stiffness_MoBL_ARMS as ma
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


# # Make initial position file needed to check work in forward simulation
# stateStore = osim.Storage()
# sessionname = model.getName()
# columnlabels = osim.ArrayStr()
# statenames = model.getStateVariableNames()

# columnlabels.append("time")

# for i in range(statenames.getSize()):
#     columnlabels.append(statenames.getitem(i))

# stateStore.setColumnLabels(columnlabels)
# stateStore.setName(sessionname)
    
# Statevalues = model.getStateVariableValues(state)
# vector = osim.StateVector()
# vector.setStates(state.getTime(),Statevalues)
# stateStore.append(vector)


# stateStore.printToXML(r"Main\Set-up\Moblarms\Initial_position\test.sto")



# Store activations and add a one at the beginning of the array representing passive effects
activations = [1]
for ac in activation:
    activations.append(ac.value)


# Calculate H matrix
H_1,test = ma.calc_H_Mobl(model,state)

# Multiply H matrix with activations to find end point forces
F_1 = np.matmul(H_1,activations)
tester = np.matmul(test,activations)


print(F_1)
print(tester)


# body_interest = model.get_BodySet().get("hand")
# point_1 = body_interest.getPositionInGround(state)



# stiffness = np.zeros((8,3))



# j = 0
# for coor in model.getCoordinateSet():
#     name = coor.getName()
#     if name == "elv_angle" or name == "shoulder_elv" or name == "shoulder_rot" or name == "elbow_flexion":
#         s2 = state
#         for i in range(2):
#             value = coor.getValue(state)
#             value2 = value - 1 + 2*i
#             coor.setValue(s2,value2)
#             model.equilibrateMuscles(s2)
#             elv_angle_rad = state.getY()[10]
#             shoulder_elv_rad = state.getY()[11]
#             shoulder_rot_rad = state.getY()[13]
#             elbow_flexion_rad = state.getY()[14]
#             # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
#             position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
#             # Find the related coordinates of the Mobl_arms model
#             position_file.find_related_coor()
#             # Write the initial position and stationary kinematics file
#             file_name = position_file.stat_kine_file_H()
#             H_new = ma.calc_H_Mobl(model,state)
#             F_new = np.matmul(H_new,activations)
            
#             point_new = body_interest.getPositionInGround(s2)
#             defl = point_new.to_numpy()-point_1.to_numpy()
#             delF = -(F_new-F_1)
#             stiff = delF/defl
#             # print(dir(stiff))
#             stiffness[j] = stiff
#             j += 1
            

# print(stiffness)

