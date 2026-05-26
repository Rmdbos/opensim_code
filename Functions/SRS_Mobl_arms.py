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






# Fuction that calculates the H matrix for the MoBL_ARMS model
# model: the model for which to calculate the H matrix. Type: OpenSim model
# state: state of the model for which the H matrix needs to be calculated. Type: OpenSim state
def calc_H_Mobl(model,state,activations):

    # Initialise a solver that finds the muscle moment arms
    solver = osim.MomentArmSolver(model)

    # Get the number of muscles and number of coordinates in the model
    num_musc = round(model.getNumMuscleStates()/2)
    num_coord = model.getNumCoordinates()

    # Initialise empty Fmax and M matrices
    Fmax = np.zeros((int(num_musc),int(num_musc+1)))
    M = np.empty((num_coord,int(num_musc)))
    l_0 = np.zeros(int(num_musc))
    K_t= np.zeros(int(num_musc))
    

    # Initialise i to 0 and loop over all coordinates
    i = 0
    for coordinate in model.getCoordinateSet():
        # Initialise j to 0 and loop over all muscles
        j = 0
        for muscle in model.getMuscles():
            # Calculate cosine of the pennation angle
            cospen = muscle.getCosPennationAngle(state)
            # Calculate maximum active fiber force at given fiber length
            force_active = muscle.getActiveFiberForce(state)/muscle.getActivation(state)*cospen
            # Calculate passive fiber force at given length
            force_passive = muscle.getPassiveFiberForce(state)*cospen
            # Calculate muscle moment arm relative to coordinate
            path = muscle.getGeometryPath()
            arm = solver.solve(state,coordinate,path)
            # Add forces and moment arm to Fmax and M matrices
            Fmax[j,j+1] = force_active
        
            Fmax[j,0] = force_passive
            l_0[j] = muscle.getOptimalFiberLength()
            Kt = muscle.getTendonStiffness(state)
            if np.isposinf(Kt):
                K_t[j] = 10**6
            else:
                K_t[j] = muscle.getTendonStiffness(state)

            M[i,j] = arm
            # Add one to both i and j
            j += 1
        i += 1

    gamma = 23.4
    forces = np.matmul(Fmax,activations)
    K_m = (gamma*forces)/l_0
    K = np.zeros((int(num_musc),int(num_musc)))

    for i in range(int(num_musc)):
        K[i,i] = (K_m[i]*K_t[i])/(K_m[i]+K_t[i])
    

    Mderiv = np.zeros((num_coord,num_coord,int(num_musc)))
    for coordinatei in model.getCoordinateSet():
        i = 0
        coordangle = coordinatei.getValue(state)
        Mpm = np.zeros((3,num_coord,int(num_musc)))
        for coordinatej in model.getCoordinateSet():
            # Initialise j to 0 and loop over all muscles
            j = 0
            for muscle in model.getMuscles():
                # Calculate muscle moment arm relative to coordinate
                path = muscle.getGeometryPath()
                Mpm[0] = M
                for p in range(2):
                    angle = coordangle+((-1**p)*0.01)
                    coordinatei.setValue(state,angle)
                    arm = solver.solve(state,coordinatej,path)
                
                    Mpm[p+1,i,j] = arm
        
                # Add one to both i and j
                coordinatei.setValue(state,coordangle)
                j += 1
            i += 1
        print(Mpm)

   
    Mt = np.transpose(M)
  

    K_j = np.matmul(M,np.matmul(K,Mt))
        
    
    # # Retrieve all relevant states
    # elv_angle_deg = round(state.getY()[10]*180/np.pi,1)
    # shoulder_elv_deg = round(state.getY()[11]*180/np.pi,1)
    # shoulder_rot_deg = round(state.getY()[13]*180/np.pi,1)
    # elbow_flexion_deg = round(state.getY()[14]*180/np.pi,1)
    # elv_angle_rad = state.getY()[10]
    # shoulder_elv_rad = state.getY()[11]
    # shoulder_rot_rad = state.getY()[13]
    # elbow_flexion_rad = state.getY()[14]
    
    
    # # Perform inverse dynamics without muscle forces for 0 force condition
    # statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
    # statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
    # statop.setResultsDir("Statop_2\Force_0")
    # statop.run()

    # # Initialise list with different force magnitudes
    # mag = [-0.3,-0.2,-0.1,0.1,0.2,0.3]

    # # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the x direction
    # for i in range(6):
    #     direction = [1,0,0]
    #     magnitude = mag[i]
        
    #     # Use force setup class to create a forcefile for the inverse dynamics
    #     forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right")
    #     forcefile.generate_force_file()
    #     forcefile.generate_force_setup()

    #     # Load static optimisation instructions from file and calculate moments at independent joints
    #     statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
    #     statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
    #     statop.setResultsDir("Statop_2\Force_x_" + str(magnitude))
    #     statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
    #     statop.run()
        

    
    # # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the y direction
    # for i in range(6):
    #     direction = [0,1,0]
    #     magnitude = mag[i]

    #     # Use force setup class to create a forcefile for the inverse dynamics
    #     forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right")
    #     forcefile.generate_force_file()
    #     forcefile.generate_force_setup()

    #     # Load static optimisation instructions from file and calculate moments at independent joints
    #     statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
    #     statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
    #     statop.setResultsDir("Statop_2\Force_y_" + str(magnitude))
    #     statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
    #     statop.run()
        

    # # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the z direction
    # for i in range(6):
    #     direction = [0,0,1]
    #     magnitude = mag[i]

    #     # Use force setup class to create a forcefile for the inverse dynamics
    #     forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right")
    #     forcefile.generate_force_file()
    #     forcefile.generate_force_setup()

    #     # Load static optimisation instructions from file and calculate moments at independent joints
    #     statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
    #     statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
    #     statop.setResultsDir("Statop_2\Force_z_" + str(magnitude))
    #     statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
    #     statop.run()
    

    

    # # Initialise matrix with forces for linear regression
    # forces = np.zeros((19,3))

    # # Assign the forces applied in the inverse dynamics to the force matrix
    # for i in range(3):
    #     for j in range(6):
    #         k = 1 + j + 6*i
    #         forces[k,i] = -mag[j]
   
    # # Initialise empty matrix with the moments for linear regression
    # moments = np.zeros((19,num_coord))

    # # Set j to 0 and loop over all coordinates
    # j = 0
    # for coordinate in model.getCoordinateSet():
    #     # Get coordinate name
    #     name = coordinate.getName()
    #     # Only use indepentent coordinates
    #     if name == "elv_angle" or name == "shoulder_elv" or name == "shoulder_rot" or name == "elbow_flexion" or name == "pro_sup" or name == "deviation" or name == "flexion":
    #         # Loop over matrix columns and assign correct moment to each
    #         for i in range(19):
    #             if i == 0:
    #                 set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_0\Right_StaticOptimization_controls.xml")

    #                 control = set.get(name + "_reserve")
    #                 moment = control.getControlValue() * 10
    #                 moments[i,j] = moment
    #             if i > 0 and i <=6:
    #                 set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_x_" + str(mag[i-1]) + "\Right_StaticOptimization_controls.xml")

    #                 control = set.get(name + "_reserve")
    #                 moment = control.getControlValue() * 10
                    
    #                 moments[i,j] = moment
    #             if i > 6 and i <= 12:
    #                 set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_y_" + str(mag[i-7]) + "\Right_StaticOptimization_controls.xml")

    #                 control = set.get(name + "_reserve")
    #                 moment = control.getControlValue() * 10
    #                 moments[i,j] = moment
    #             if i > 12:
    #                 set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_z_" + str(mag[i-13]) + "\Right_StaticOptimization_controls.xml")

    #                 control = set.get(name + "_reserve")
    #                 moment = control.getControlValue() * 10
    #                 moments[i,j] = moment
    #     # Add one to j
    #     j += 1
    
    
    # # Initialise linear regression and fit to find J
    # Jmodel = LinearRegression(fit_intercept=False)
    # Jmodel.fit(forces, moments)

    # # Get J from the linear regression
    # J = Jmodel.coef_

    # # Take the pseudoinverse of J
    # J_inv = np.linalg.pinv(J)

    # # Calculate H by multiplying J, M, and Fmax
    # H = np.matmul(J_inv,np.matmul(M,Fmax))
    # # H = np.matmul(M,Fmax)
    
    # # Return H
    return Fmax, M, H


