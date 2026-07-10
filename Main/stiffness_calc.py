# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Point python where to find the source code for the class 

import sys
sys.path.insert(0, "Functions")


# Import opensim and other used libraries
import opensim as osim
import numpy as np
import matplotlib.pyplot as plt
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
# st.do_stat_op("Main\Set-up\Moblarms\stat_op_setup.xml",file_name)

# Find the activations using the static optimisation with tendon compliance
activation = so.loop_fibre_length(model,state,file_name)


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
H_1 = ma.calc_H_Mobl(model,state)

# Multiply H matrix with activations to find end point forces
F_1 = np.matmul(H_1,activations)
#tester = np.matmul(test,activations)



# print(tester)


body_interest : osim.Body = model.get_BodySet().get("hand")
pointframe = body_interest.getMassCenter()
frame = body_interest.findBaseFrame()
point_1 = frame.findStationLocationInGround(state,pointframe)



stiffness = np.zeros((30,3))
state = model.initSystem()
deflections = np.zeros((30,3))
magnitude = np.zeros(30)

j = 0
for coor in model.getCoordinateSet():
    name = coor.getName()
    if name == "elv_angle" or name == "shoulder_elv" or name == "shoulder_rot" or name == "elbow_flexion":
        
        for i in range(2):
            s2 = model.initSystem()  
            value = coor.getValue(state)
            if name == "elv_angle":
                value2 = value - 0.035 + 0.070*i 
            else:
                value2 = value - 0.023 + 0.046*i
            coor.setValue(s2,value2)
            model.equilibrateMuscles(s2)
            elv_angle_rad = s2.getY()[10]
            shoulder_elv_rad = s2.getY()[11]
            shoulder_rot_rad = s2.getY()[13]
            elbow_flexion_rad = s2.getY()[14]
            
            # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
            position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
            # Find the related coordinates of the Mobl_arms model
            position_file.find_related_coor()
            # Write the initial position and stationary kinematics file
            file_name = position_file.stat_kine_file_H()
            H_new = ma.calc_H_Mobl(model,s2)
            F_new = np.matmul(H_new,activations)
            


            frame = body_interest.findBaseFrame()
            point_new = frame.findStationLocationInGround(s2,pointframe)
            # point_new = body_interest.getPositionInGround(s2)
            defl = point_new.to_numpy()-point_1.to_numpy()
            deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
            delF = -(F_new-F_1)
            delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
            stiff = delFmag/deflmag
            stiffdir = defl/deflmag
            deflections[j] = defl
            stiffness[j] = stiff*stiffdir
            magnitude[j] = deflmag
            j += 1
            


coord_angle = model.getCoordinateSet().get("elv_angle")
coord_elv = model.getCoordinateSet().get("shoulder_elv")
coord_rot = model.getCoordinateSet().get("shoulder_rot")
coord_elbow = model.getCoordinateSet().get("elbow_flexion")



for i in range(2):
    s2 = model.initSystem()  
    value_angle = coord_angle.getValue(state)
    value_elv = coord_elv.getValue(state)
    
    value_angle2 = value_angle - 0.017 + 0.035*i 
    value_elv2 = value_elv + 0.017 - 0.035*i 
    

    coord_angle.setValue(s2,value_angle2)
    coord_elv.setValue(s2,value_elv2)
    
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[8+i] = defl
    stiffness[8+i] = stiff*stiffdir
    magnitude[8+i] = deflmag



for i in range(2):
    s2 = model.initSystem()  
    value_angle = coord_angle.getValue(state)
    value_elbow = coord_elbow.getValue(state)
   
    value_angle2 = value_angle - 0.035 + 0.070*i
    value_elbow2 = value_elbow + 0.017 - 0.035*i 

    coord_angle.setValue(s2,value_angle2)
    coord_elbow.setValue(s2,value_elbow2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[10+i] = defl
    stiffness[10+i] = stiff*stiffdir
    magnitude[10+i] = deflmag



for i in range(2):
    s2 = model.initSystem()  
    value_angle = coord_angle.getValue(state)
    value_rot = coord_rot.getValue(state)
   
    value_angle2 = value_angle + 0.035 - 0.070*i 
    value_rot2 = value_rot + 0.017 - 0.035*i 

    coord_angle.setValue(s2,value_angle2)
    coord_rot.setValue(s2,value_rot2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[12+i] = defl
    stiffness[12+i] = stiff*stiffdir
    magnitude[12+i] = deflmag



for i in range(2):
    s2 = model.initSystem()  
    value_elv = coord_elv.getValue(state)
    value_elbow = coord_elbow.getValue(state)
   
    value_elv2 = value_elv + 0.023 - 0.046*i 
    value_elbow2 = value_elbow + 0.017 - 0.035*i 

    coord_elv.setValue(s2,value_elv2)
    coord_elbow.setValue(s2,value_elbow2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[14+i] = defl
    stiffness[14+i] = stiff*stiffdir
    magnitude[14+i] = deflmag




for i in range(2):
    s2 = model.initSystem()  
    value_elv = coord_elv.getValue(state)
    value_rot = coord_rot.getValue(state)
   
    value_elv2 = value_elv - 0.0085 + 0.017*i 
    value_rot2 = value_rot + 0.017 - 0.035*i 

    coord_elv.setValue(s2,value_elv2)
    coord_rot.setValue(s2,value_rot2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[16+i] = defl
    stiffness[16+i] = stiff*stiffdir
    magnitude[16+i] = deflmag


for i in range(2):
    s2 = model.initSystem()  
    
    value_elbow = coord_elbow.getValue(state)
    value_rot = coord_rot.getValue(state)
    
    value_elbow2 = value_elbow + 0.017 - 0.035*i 
    value_rot2 = value_rot + 0.0085 - 0.017*i 

    
    coord_elbow.setValue(s2,value_elbow2)
    coord_rot.setValue(s2,value_rot2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[18+i] = defl
    stiffness[18+i] = stiff*stiffdir
    magnitude[18+i] = deflmag





for i in range(2):
    s2 = model.initSystem()  
    value_angle = coord_angle.getValue(state)
    value_elv = coord_elv.getValue(state)
    value_elbow = coord_elbow.getValue(state)
    value_angle2 = value_angle - 0.035 + 0.070*i 
    value_elv2 = value_elv + 0.017 - 0.035*i 
    value_elbow2 = value_elbow + 0.017 - 0.035*i 

    coord_angle.setValue(s2,value_angle2)
    coord_elv.setValue(s2,value_elv2)
    coord_elbow.setValue(s2,value_elbow2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[20+i] = defl
    stiffness[20+i] = stiff*stiffdir
    magnitude[20+i] = deflmag


for i in range(2):
    s2 = model.initSystem()  
    value_angle = coord_angle.getValue(state)
    value_elv = coord_elv.getValue(state)
    value_rot = coord_rot.getValue(state)
    value_angle2 = value_angle - 0.0085 + 0.017*i 
    value_elv2 = value_elv + 0.017 - 0.035*i 
    value_rot2 = value_rot - 0.0085 + 0.017*i 

    coord_angle.setValue(s2,value_angle2)
    coord_elv.setValue(s2,value_elv2)
    coord_rot.setValue(s2,value_rot2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[22+i] = defl
    stiffness[22+i] = stiff*stiffdir
    magnitude[22+i] = deflmag



for i in range(2):
    s2 = model.initSystem()  
    value_angle = coord_angle.getValue(state)
    value_elbow = coord_elbow.getValue(state)
    value_rot = coord_rot.getValue(state)
    value_angle2 = value_angle - 0.017 + 0.035*i 
    value_elbow2 = value_elbow + 0.023 - 0.046*i 
    value_rot2 = value_rot - 0.017 + 0.035*i 

    coord_angle.setValue(s2,value_angle2)
    coord_elbow.setValue(s2,value_elbow2)
    coord_rot.setValue(s2,value_rot2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[24+i] = defl
    stiffness[24+i] = stiff*stiffdir
    magnitude[24+i] = deflmag


for i in range(2):
    s2 = model.initSystem()  
    value_elv = coord_elv.getValue(state)
    value_elbow = coord_elbow.getValue(state)
    value_rot = coord_rot.getValue(state)
    value_elv2 = value_elv - 0.023 + 0.046*i 
    value_elbow2 = value_elbow - 0.017 + 0.035*i 
    value_rot2 = value_rot + 0.017 - 0.035*i 

    coord_elv.setValue(s2,value_elv2)
    coord_elv.setValue(s2,value_elv2)
    coord_elbow.setValue(s2,value_elbow2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[26+i] = defl
    stiffness[26+i] = stiff*stiffdir
    magnitude[26+i] = deflmag


for i in range(2):
    s2 = model.initSystem() 
    value_angle = coord_angle.getValue(state) 
    value_elv = coord_elv.getValue(state)
    value_elbow = coord_elbow.getValue(state)
    value_rot = coord_rot.getValue(state)
    value_angle2 = value_angle - 0.035 + 0.070*i 
    value_elv2 = value_elv + 0.017 - 0.035*i 
    value_elbow2 = value_elbow + 0.017 - 0.035*i 
    value_rot2 = value_rot - 0.017 + 0.035*i 

    coord_angle.setValue(s2,value_angle2)
    coord_elv.setValue(s2,value_elv2)
    coord_elv.setValue(s2,value_elv2)
    coord_elbow.setValue(s2,value_elbow2)
    model.equilibrateMuscles(s2)
    elv_angle_rad = s2.getY()[10]
    shoulder_elv_rad = s2.getY()[11]
    shoulder_rot_rad = s2.getY()[13]
    elbow_flexion_rad = s2.getY()[14]
            
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
    # Find the related coordinates of the Mobl_arms model
    position_file.find_related_coor()
    # Write the initial position and stationary kinematics file
    file_name = position_file.stat_kine_file_H()
    H_new = ma.calc_H_Mobl(model,s2)
    F_new = np.matmul(H_new,activations)
            
    frame = body_interest.findBaseFrame()
    point_new = frame.findStationLocationInGround(s2,pointframe)
    defl = point_new.to_numpy()-point_1.to_numpy()
    deflmag = np.sqrt(defl[0]**2+defl[1]**2+defl[2]**2)
    delF = -(F_new-F_1)
    delFmag = np.sqrt(delF[0]**2+delF[1]**2+delF[2]**2)
    stiff = delFmag/deflmag
    stiffdir = defl/deflmag
    
    deflections[28+i] = defl
    stiffness[28+i] = stiff*stiffdir
    magnitude[28+i] = deflmag





print(stiffness)
print(deflections)
print(magnitude)

