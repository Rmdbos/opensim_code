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
def calc_H_Mobl(model,state):

    # Initialise a solver that finds the muscle moment arms
    solver = osim.MomentArmSolver(model)

    # Get the number of muscles and number of coordinates in the model
    num_musc = round(model.getNumMuscleStates()/2)
    num_coord = model.getNumCoordinates()

    # Initialise empty Fmax and M matrices
    Fmax = np.zeros((int(num_musc),int(num_musc+1)))
    M = np.empty((num_coord,int(num_musc)))
    

    # Initialise i to 0 and loop over all coordinates
    i = 0
    for coordinate in model.getCoordinateSet():
        # Initialise j to 0 and loop over all muscles
        j = 0
        for muscle in model.getMuscles():
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

            M[i,j] = arm
            # Add one to both i and j
            j += 1
        i += 1
        
    
  
    elv_angle_deg = round(state.getY()[10]*180/np.pi,1)
    shoulder_elv_deg = round(state.getY()[11]*180/np.pi,1)
    shoulder_rot_deg = round(state.getY()[13]*180/np.pi,1)
    elbow_flexion_deg = round(state.getY()[14]*180/np.pi,1)
    elv_angle_rad = state.getY()[10]
    shoulder_elv_rad = state.getY()[11]
    shoulder_rot_rad = state.getY()[13]
    elbow_flexion_rad = state.getY()[14]
    
    
    # Perform inverse dynamics without muscle forces for 0 force condition
    statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
    statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
    statop.setResultsDir("Statop_2\Force_0")
    statop.run()

    # Initialise list with different force magnitudes
    mag = [-0.3,-0.2,-0.1,0.1,0.2,0.3]

    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the x direction
    for i in range(6):
        direction = [1,0,0]
        magnitude = mag[i]
        
        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right", [1, 0, 0],0)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()


        statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
        statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
        statop.setResultsDir("Statop_2\Force_x_" + str(magnitude))
        statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
        statop.run()
        

    
    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the y direction
    for i in range(6):
        direction = [0,1,0]
        magnitude = mag[i]

        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right", [1, 0, 0],0)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()


        statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
        statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
        statop.setResultsDir("Statop_2\Force_y_" + str(magnitude))
        statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
        statop.run()
        

    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the z direction
    for i in range(6):
        direction = [0,0,1]
        magnitude = mag[i]

        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right", [1, 0, 0],0)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()


        statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
        statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
        statop.setResultsDir("Statop_2\Force_z_" + str(magnitude))
        statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
        statop.run()
    

   

    # Initialise list with different force magnitudes
    magT = [-0.3,-0.2,-0.1,0.1,0.2,0.3]

    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the x direction
    for i in range(6):
        directionT = [1,0,0]
        magnitudeT = magT[i]
        print(type(directionT))
        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file( [1, 0, 0],0, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right", directionT, magnitudeT)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()


        statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
        statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
        statop.setResultsDir(r"Statop_2\torque_x_" + str(magnitudeT))
        statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
        statop.run()
        

    
    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the y direction
    for i in range(6):
        directionT = [0,1,0]
        magnitudeT = magT[i]

        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file([1, 0, 0],0, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right",directionT,magnitudeT)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()


        statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
        statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
        statop.setResultsDir(r"Statop_2\torque_y_" + str(magnitudeT))
        statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
        statop.run()
        

    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the z direction
    for i in range(6):
        directionT = [0,0,1]
        magnitudeT = magT[i]

        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file([1, 0, 0],0, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right",directionT,magnitudeT)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()


        statop = osim.AnalyzeTool("Main\Set-up\Moblarms\stat_op_setup.xml")
        statop.setCoordinatesFileName("Stationary_kinematics"'\\' + "Mobl_static_kinematics_elv_angle_" + str(elv_angle_deg) + "_shoulder_elv_" + str(shoulder_elv_deg) + "_elbow_flexion_" + str(elbow_flexion_deg) + ".mot")
        statop.setResultsDir(r"Statop_2\torque_z_" + str(magnitudeT))
        statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
        
        statop.run()

    # Initialise matrix with forces for linear regression
    forces_torques = np.zeros((19,3))

    # Assign the forces applied in the inverse dynamics to the force matrix
    for i in range(3):
        for j in range(6):
            k = 1 + j + 6*i
            forces_torques[k,i] = -mag[j]
            

    print(forces_torques)
   
    # Initialise empty matrix with the moments for linear regression
    moments = np.zeros((19,num_coord))

    # Set j to 0 and loop over all coordinates
    j = 0
    for coordinate in model.getCoordinateSet():
        # Get coordinate name
        name = coordinate.getName()
        # Loop over matrix columns and assign correct moment to each
        for i in range(19):
            if i == 0:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_0\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                moments[i,j] = moment
            if i > 0 and i <=6:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_x_" + str(mag[i-1]) + "\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                    
                moments[i,j] = moment
            if i > 6 and i <= 12:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_y_" + str(mag[i-7]) + "\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                moments[i,j] = moment
            if i > 12:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_z_" + str(mag[i-13]) + "\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                moments[i,j] = moment
                
        # Add one to j
        j += 1


    moments2 = np.zeros((19,num_coord))

    # Set j to 0 and loop over all coordinates
    j = 0
    for coordinate in model.getCoordinateSet():
        # Get coordinate name
        name = coordinate.getName()
        # Loop over matrix columns and assign correct moment to each
        for i in range(19):
            if i == 0:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\Force_0\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                moments2[i,j] = moment
            if i > 0 and i <= 6:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\torque_x_" + str(magT[i-1]) + "\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                moments2[i,j] = moment
            if i > 6 and i <= 12:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\torque_y_" + str(magT[i-7]) + "\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                moments2[i,j] = moment
            if i > 12:
                set = osim.ControlSet(r"Main\Set-up\Moblarms\Statop_2\torque_z_" + str(magT[i-13]) + "\Right_StaticOptimization_controls.xml")

                control = set.get(name + "_reserve")
                moment = control.getControlValue() * 10
                moments2[i,j] = moment
        # Add one to j
        j += 1
    # print(moments)
    
    
    # Initialise linear regression and fit to find J
    Jmodel = LinearRegression(fit_intercept=False)
    Jmodel.fit(forces_torques, moments)

    # Get J from the linear regression
    J = Jmodel.coef_
    

    # Take the pseudoinverse of J
    J_inv = np.linalg.pinv(J)

    # Initialise linear regression and fit to find J
    Jmodel2 = LinearRegression(fit_intercept=False)
    Jmodel2.fit(forces_torques, moments2)

    # Get J from the linear regression
    J2 = Jmodel2.coef_
    
    
    # Take the pseudoinverse of J
    J_inv2 = np.linalg.pinv(J2)

    # Calculate H by multiplying J, M, and Fmax
    H = np.matmul(J_inv,np.matmul(M,Fmax))
    H2 = np.matmul(J_inv2,np.matmul(M,Fmax))
    # H = np.matmul(M,Fmax)
    
    # Return H
    return H, H2


# model = osim.Model(r"Main\Set-up\Moblarms\MOBL_ARMS.osim")

# s = model.initSystem()
# model.equilibrateMuscles(s)

# H1 = calc_H_Mobl(model,s)

# print(H1)

# # Find point of body in cartesian coordinates
# body_interest = model.get_BodySet().get("hand")
# point = body_interest.getPositionInGround(s)
# print(point)
