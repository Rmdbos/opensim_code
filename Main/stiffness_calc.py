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
import matplotlib.pyplot as plt

import scipy.optimize
import Generate_force_files as fs
import Generate_stationary_kinematics_MOBL as sk
import sta_op_tendon_comp as so
import Static_op_moments as st
import testing_H_copy as ma
np.set_printoptions(threshold=sys.maxsize)




# Initialise model and state and set coordinate angle
model = osim.Model(r"Main\Set-up\test\test_simple_dependent.osim")

state = model.initSystem()



# Define state as wanted



# Calculate coordinate angles in both radians and degrees
  
# elv_angle_deg = round(state.getY()[10]*180/np.pi,1)
# shoulder_elv_deg = round(state.getY()[11]*180/np.pi,1)
# shoulder_rot_deg = round(state.getY()[13]*180/np.pi,1)
# elbow_flexion_deg = round(state.getY()[14]*180/np.pi,1)
# elv_angle_rad = state.getY()[10]
# shoulder_elv_rad = state.getY()[11]
# shoulder_rot_rad = state.getY()[13]
# elbow_flexion_rad = state.getY()[14]
  

# # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
# position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)

    
# Find the related coordinates of the Mobl_arms model
# position_file.find_related_coor()

# Write the initial position and stationary kinematics file
file_name = r"test_static_kinematics_ID_angle_0.mot"


st.do_stat_op(model,file_name)



activation = so.loop_fibre_length(model,state)

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


# stateStore.printToXML(r"Main\Set-up\test\Initial_position\test.sto")

activations = [1]
for ac in activation:
    activations.append(ac.value)



H_1  = ma.calc_H_test(model,state)
F_1 = np.matmul(H_1,activations)
# # ## T_1 = np.matmul(H_2,activations)
# tester = np.matmul(test,activations)

# print(F_1)
# print(tester)
# print(T_1)

body_interest = model.get_BodySet().get("arm2")
point_1 = body_interest.getPositionInGround(state)



stiffness = np.zeros((4,2))
state = model.initSystem()


j = 0
for coor in model.getCoordinateSet():
    name = coor.getName()
    if name == "rot_coord_0":
        print("test")
        
        for i in range(4):
            s2 = model.initSystem()  
            value = coor.getValue(state)
            value2 = value - 0.017 + 0.035*i 
            coor.setValue(s2,value2)


            model.equilibrateMuscles(s2)
            
            
            # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
            #position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms', 0,0,0,elv_angle_rad,shoulder_rot_rad,shoulder_elv_rad,elbow_flexion_rad)
            # Find the related coordinates of the Mobl_arms model
            #position_file.find_related_coor()
            # Write the initial position and stationary kinematics file
            #file_name = position_file.stat_kine_file_H()
            H_new = ma.calc_H_test(model,s2)
            F_new = np.matmul(H_new,activations)
            
            point_new = body_interest.getPositionInGround(s2)
            defl = point_new.to_numpy()-point_1.to_numpy()
            deflmag = np.sqrt(defl[0]**2+defl[1]**2)
            delF = -(F_new-F_1)
          
            delFmag = np.sqrt(delF[0]**2+delF[1]**2)
            stiff = delFmag/deflmag
            stiffdir = defl/deflmag
            
            stiffdir = np.delete(stiffdir,1)
           
            stiffness[j] = stiff*stiffdir
            
            j += 1
            
plt.plot(stiffness[:,0],stiffness[:,1])



x_data = stiffness[:,0]
y_data = stiffness[:,1]

def ellipse(x, y, alpha, a, b):
    x1 = x*np.cos(alpha)+y*np.sin(alpha)
    y1 = x*-np.sin(alpha) + y*np.cos(alpha)
    f = (x1 / a) ** 2 + (y1 / b) ** 2 - 1
    return f


def f_min(params, x, y):
    alpha, a, b = params
    return np.sum(ellipse(x, y, alpha, a, b)**2)


# Initial guess
p0 = [90, 1e12, 1e10]

# Optimize
res=scipy.optimize.minimize(f_min, p0, args=(x_data, y_data))

print(res.x)


u=0       #x-position of the center
v=0     #y-position of the center
a=res.x[1]       #radius on the x-axis
b=res.x[2]     #radius on the y-axis
t_rot=np.deg2rad(res.x[0]) #rotation angle
print(t_rot)

t = np.linspace(0, 2*np.pi, 100)
Ell = np.array([a*np.cos(t) , b*np.sin(t)])  
     #u,v removed to keep the same center location
R_rot = np.array([[np.cos(t_rot) , np.sin(t_rot)],[-np.sin(t_rot) , np.cos(t_rot)]])  
     #2-D rotation matrix

Ell_rot = np.zeros((2,Ell.shape[1]))
for i in range(Ell.shape[1]):
    Ell_rot[:,i] = np.dot(R_rot,Ell[:,i])

# plt.plot( u+Ell[0,:] , v+Ell[1,:] )     #initial ellipse
plt.plot( u+Ell_rot[0,:] , v+Ell_rot[1,:],'darkorange' )    #rotated ellipse
plt.grid(color='lightgray',linestyle='--')
plt.show()