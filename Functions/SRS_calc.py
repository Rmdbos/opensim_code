# Python file with function that calculates the H matrix for the das3 model


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
np.set_printoptions(threshold=sys.maxsize)



def calc_srs(model,state,activations):
    


    # Get the number of muscles and number of coordinates in the model
    num_musc = round(model.getNumMuscleStates()/2)

    # Initialise empty Fmax and M matrices
    Fmax = np.zeros((int(num_musc),int(num_musc+1)))
    l_0 = np.zeros(int(num_musc))
    K_t= np.zeros(int(num_musc))
    

    

    # Initialise i to 0 and loop over all coordinates
 
    j = 0
    for muscle in model.getMuscles():

        
        # Calculate cosine of the pennation angle
        cospen = muscle.getCosPennationAngle(state)
        # Calculate maximum active fiber force at given fiber length
        force_active = muscle.getActiveFiberForce(state)/muscle.getActivation(state)*cospen
        # Calculate passive fiber force at given length
        force_passive = muscle.getPassiveFiberForce(state)*cospen
        # Add forces and moment arm to Fmax and M matrices
        Fmax[j,j+1] = force_active
        
        Fmax[j,0] = force_passive
        l_0[j] = muscle.getOptimalFiberLength()
        Kt = muscle.getTendonStiffness(state)
        if np.isposinf(Kt):
            K_t[j] = 10**6
        else:
            K_t[j] = muscle.getTendonStiffness(state)
        
        
        # Add one to both i and j
        j += 1
    gamma = 23.4
    forces = np.matmul(Fmax,activations)
    K_m = (gamma*forces)/l_0
    K = (K_m*K_t)/(K_m+K_t)
    print(K)
   