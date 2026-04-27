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
import Generate_stationary_kinematics_DAS as sk
np.set_printoptions(threshold=sys.maxsize)






# Fuction that calculates the H matrix for the Das3 model
# model: the model for which to calculate the H matrix. Type: OpenSim model
# state: state of the model for which the H matrix needs to be calculated. Type: OpenSim state
def calc_H_das(model,state):

    # Initialise a solver that finds the muscle moment arms
    solver = osim.MomentArmSolver(model)

    # Get the number of muscles and number of coordinates in the model
    num_musc = model.getNumMuscleStates()/2
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
            # Ensure muscle activation is not 0 and calculate fiber length for this activation
            muscle.setActivation(state,0.01)
            model.equilibrateMuscles(state)
            # Calculate maximum active fiber force at given fiber length
            force_active = muscle.getActiveFiberForce(state)/muscle.getActivation(state)
            # Calculate passive fiber force at given length
            force_passive = muscle.getPassiveFiberForce(state)
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
        
   
  

    # Calculate coordinate angles in both radians and degrees
    GH_y_degrees = round(state.getY()[6]*180/np.pi,1)
    GH_z_degrees = round(state.getY()[7]*180/np.pi,1)
    GH_yy_degrees = round(state.getY()[8]*180/np.pi,1)
    EL_x_degrees = round(state.getY()[9]*180/np.pi,1)
    GH_y_rad = state.getY()[6]
    GH_z_rad = state.getY()[7]
    GH_yy_rad = state.getY()[8]
    EL_x_rad = state.getY()[9]

    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(r'Main\Set-up\DAS3', 0,0,0,GH_y_rad,GH_z_rad,GH_yy_rad,EL_x_rad)

    
    # Write the initial position and stationary kinematics file
    position_file.stat_kine_file_H()

    # Perform inverse dynamics without muscle forces for 0 force condition
    ID = osim.InverseDynamicsTool()
    ID.set_results_directory(r"Main\Set-up\DAS3\inverse_dynamics")
    ID.setCoordinatesFileName("Main\Set-up\DAS3\Stationary_kinematics\DAS_static_kinematics_GH_y_" + str(GH_y_degrees) + "_GH_z_" + str(GH_z_degrees) + "_EL_x_" + str(EL_x_degrees) + ".mot")
    ID.setModel(model)
    muscles = osim.ArrayStr()
    muscles.append('Muscles')
    ID.setExcludedForces(muscles)
    ID.setStartTime(0)
    ID.setEndTime(0.01)
    ID.setOutputGenForceFileName("Force_0.sto")
    ID.run()

    # Initialise list with different force magnitudes
    mag = [-0.3,-0.2,-0.1,0.1,0.2,0.3]

    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the x direction
    for i in range(6):
        direction = [1,0,0]
        magnitude = mag[i]
        
        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\DAS3", "hand_r", "das3")
        forcefile.generate_force_file()
        forcefile.generate_force_setup()

        ID = osim.InverseDynamicsTool()
        ID.set_results_directory(r"Main\Set-up\DAS3\inverse_dynamics")
        ID.setCoordinatesFileName("Main\Set-up\DAS3\Stationary_kinematics\DAS_static_kinematics_GH_y_" + str(GH_y_degrees) + "_GH_z_" + str(GH_z_degrees) + "_EL_x_" + str(EL_x_degrees) + ".mot")
        ID.setExternalLoadsFileName(r"Main\Set-up\DAS3\Forward_dynamics\das3_forces.xml")
        ID.setModel(model)
        muscles = osim.ArrayStr()
        muscles.append('Muscles')
        ID.setExcludedForces(muscles)
        ID.setStartTime(0)
        ID.setEndTime(0.01)
        ID.setOutputGenForceFileName("Force_x_" + str(magnitude) +".sto")
        ID.run()


    
    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the y direction
    for i in range(6):
        direction = [0,1,0]
        magnitude = mag[i]

        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\DAS3", "hand_r", "das3")
        forcefile.generate_force_file()
        forcefile.generate_force_setup()

        ID = osim.InverseDynamicsTool()
        ID.set_results_directory(r"Main\Set-up\DAS3\inverse_dynamics")
        ID.setCoordinatesFileName("Main\Set-up\DAS3\Stationary_kinematics\DAS_static_kinematics_GH_y_" + str(GH_y_degrees) + "_GH_z_" + str(GH_z_degrees) + "_EL_x_" + str(EL_x_degrees) + ".mot")
        ID.setExternalLoadsFileName(r"Main\Set-up\DAS3\Forward_dynamics\das3_forces.xml")
        ID.setModel(model)
        muscles = osim.ArrayStr()
        muscles.append('Muscles')
        ID.setExcludedForces(muscles)
        ID.setStartTime(0)
        ID.setEndTime(0.01)
        ID.setOutputGenForceFileName("Force_y_" + str(magnitude) +".sto")
        ID.run()

    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the z direction
    for i in range(6):
        direction = [0,0,1]
        magnitude = mag[i]

        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\DAS3", "hand_r", "das3")
        forcefile.generate_force_file()
        forcefile.generate_force_setup()

        ID = osim.InverseDynamicsTool()
        ID.set_results_directory(r"Main\Set-up\DAS3\inverse_dynamics")
        ID.setCoordinatesFileName("Main\Set-up\DAS3\Stationary_kinematics\DAS_static_kinematics_GH_y_" + str(GH_y_degrees) + "_GH_z_" + str(GH_z_degrees) + "_EL_x_" + str(EL_x_degrees) + ".mot")
        ID.setExternalLoadsFileName(r"Main\Set-up\DAS3\Forward_dynamics\das3_forces.xml")
        ID.setModel(model)
        muscles = osim.ArrayStr()
        muscles.append('Muscles')
        ID.setExcludedForces(muscles)
        ID.setStartTime(0)
        ID.setEndTime(0.01)
        ID.setOutputGenForceFileName("Force_z_" + str(magnitude) +".sto")
        ID.run()


    # Initialise matrix with forces for linear regression
    forces = np.zeros((19,3))

    # Assign the forces applied in the inverse dynamics to the force matrix
    for i in range(3):
        for j in range(6):
            k = 1 + j + 6*i
            forces[k,i] = -mag[j]
   
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
                tableTime = osim.TimeSeriesTable(r'Main\Set-up\das3\inverse_dynamics\Force_0.sto')
                moment = tableTime.getDependentColumn(name + "_moment")
                moments[i,j] = moment.to_numpy()[1]
            if i > 0 and i <=6:
                tableTime = osim.TimeSeriesTable(r'Main\Set-up\das3\inverse_dynamics\Force_x_' + str(mag[i-1]) + '.sto')
                moment = tableTime.getDependentColumn(name + "_moment")
                moments[i,j] = moment.to_numpy()[1]
            if i > 6 and i <= 12:
                tableTime = osim.TimeSeriesTable(r'Main\Set-up\das3\inverse_dynamics\Force_y_' + str(mag[i-7]) + '.sto')
                moment = tableTime.getDependentColumn(name + "_moment")
                moments[i,j] = moment.to_numpy()[1]
            if i > 12:
                tableTime = osim.TimeSeriesTable(r'Main\Set-up\das3\inverse_dynamics\Force_z_' + str(mag[i-13]) + '.sto')
                moment = tableTime.getDependentColumn(name + "_moment")
                moments[i,j] = moment.to_numpy()[1]
        # Add one to j
        j += 1
        
    
    # Initialise linear regression and fit to find J
    Jmodel = LinearRegression(fit_intercept=False)
    Jmodel.fit(forces, moments)

    # Get J from the linear regression
    J = Jmodel.coef_

    # Take the pseudoinverse of J
    J_inv = np.linalg.pinv(J)

    # Calculate H by multiplying J, M, and Fmax
    H = np.matmul(J_inv,np.matmul(M,Fmax))

    
    # Return H
    return H


model = osim.Model(r"Main\Set-up\DAS3\das3.osim")

s = model.initSystem()
model.equilibrateMuscles(s)

H1 = calc_H_das(model,s)

print(H1)

# Find point of body in cartesian coordinates
body_interest = model.get_BodySet().get("hand_r")
point = body_interest.getPositionInGround(s)
print(point)
