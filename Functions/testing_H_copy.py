# Python file with function that calculates the H matrix for the testing model


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
import Generate_stationary_kinematics_test_ID as sk




# Initialise model
model = osim.Model(r"Main\Set-up\test\test_simple.osim")

# Initialise state and equilibrate muscles
s = model.initSystem()
model.equilibrateMuscles(s)


# Fuction that calculates the H matrix for the testing model
# model: the model for which to calculate the H matrix. Type: OpenSim model
# state: state of the model for which the H matrix needs to be calculated. Type: OpenSim state
def calc_H_test(model,state):
    

    # Initialise a solver that finds the muscle moment arms
    solver = osim.MomentArmSolver(model)


    gravity = model.getGravity()
    # print(gravity)
    gravnew = osim.Vec3([0,0,0])
    model.setGravity(gravnew)

    # Get the number of muscles and number of coordinates in the model
    num_musc = model.getNumMuscleStates()/2
    num_coord = model.getNumCoordinates()

    # Initialise empty Fmax and M matrices
    Fmax = np.zeros((int(num_musc),int(num_musc+1)))
    M = np.empty((num_coord,int(num_musc)))
    print(M)
    
    # Initialise i to 0 and loop over all coordinates
    i = 0
    for coordinate in model.getCoordinateSet():
        # Initialise j to 0 and loop over all muscles
        j = 0
        for muscle in model.getMuscles():
            print(muscle.getName())
            cospen = muscle.getCosPennationAngle(state)
            # Calculate maximum active fiber force at given fiber length
            force_active = muscle.getActiveFiberForce(state)/muscle.getActivation(state)*cospen
            # Calculate passive fiber force at given length
            force_passive = muscle.getPassiveFiberForce(state)*cospen
            # Calculate muscle moment arm relative to coordinate
            path = muscle.getGeometryPath()
            arm = solver.solve(state,coordinate,path)
            print(arm)
            # Add forces and moment arm to Fmax and M matrices
            Fmax[j,j+1] = force_active
            Fmax[j,0] = force_passive
            M[i,j] = arm
            print(M)
            # Add one to both i and j
            j += 1
        i += 1
    print(M)
    # Calculate coordinate angles in degrees
    angle_degrees = round(state.getY()[0]*180/np.pi,1)
    # Create object using the create static kinematics file class, given angles for the joints and a path to the setup directory
    position_file = sk.stat_kine_file(angle_degrees,r'Main\Set-up\test')

    
    # Write the initial position and stationary kinematics file
    position_file.stat_kine_file()

    # Perform inverse dynamics without muscle forces for 0 force condition
    ID = osim.InverseDynamicsTool()
    ID.set_results_directory(r"Main\Set-up\test\inverse_dynamics")
    ID.setCoordinatesFileName(r"Main\Set-up\test\Stationary_kinematics\test_static_kinematics_ID_angle_" + str(angle_degrees) + ".mot")
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
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\test", "arm2", "model",[1,0,0],0)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()

        ID = osim.InverseDynamicsTool()
        ID.set_results_directory(r"Main\Set-up\test\inverse_dynamics")
        ID.setCoordinatesFileName(r"Main\Set-up\test\Stationary_kinematics\test_static_kinematics_ID_angle_" + str(angle_degrees) + ".mot")
        ID.setExternalLoadsFileName(r"Main\Set-up\test\Forward_dynamics\model_forces.xml")
        ID.setModel(model)
        muscles = osim.ArrayStr()
        muscles.append('Muscles')
        ID.setExcludedForces(muscles)
        ID.setStartTime(0)
        ID.setEndTime(0.01)
        ID.setOutputGenForceFileName("Force_x_" + str(magnitude) +".sto")
        ID.run()


    # Loop over all force magnitudes and apply them to the model in and inverse dynamics simulation in the z direction
    for i in range(6):
        direction = [0,0,1]
        magnitude = mag[i]

        # Use force setup class to create a forcefile for the inverse dynamics
        forcefile = fs.force_setup_file(direction, magnitude, "Force_ID", r"Main\Set-up\test", "arm2", "model", [1,0,0],0)
        forcefile.generate_force_file()
        forcefile.generate_force_setup()

        ID = osim.InverseDynamicsTool()
        ID.set_results_directory(r"Main\Set-up\test\inverse_dynamics")
        ID.setCoordinatesFileName(r"Main\Set-up\test\Stationary_kinematics\test_static_kinematics_ID_angle_" + str(angle_degrees) + ".mot")
        ID.setExternalLoadsFileName(r"Main\Set-up\test\Forward_dynamics\model_forces.xml")
        ID.setModel(model)
        muscles = osim.ArrayStr()
        muscles.append('Muscles')
        ID.setExcludedForces(muscles)
        ID.setStartTime(0)
        ID.setEndTime(0.01)
        ID.setOutputGenForceFileName("Force_z_" + str(magnitude) +".sto")
        ID.run()


    # Initialise matrix with forces for linear regression
    forces = np.zeros((13,2))

    # Assign the forces applied in the inverse dynamics to the force matrix
    for i in range(2):
        for j in range(6):
            k = 1 + j + 6*i
            forces[k,i] = -mag[j]
    

    # Initialise empty matrix with the moments for linear regression
    moments = np.zeros((13,num_coord))

    # Loop over matrix columns and assign correct moment to each
    j = 0
    for coordinate in model.getCoordinateSet():
        # Get coordinate name
        name = coordinate.getName()
        for i in range(13):
            if i == 0:
                tableTime = osim.TimeSeriesTable(r'Main\Set-up\test\inverse_dynamics\Force_0.sto')
                moment = tableTime.getDependentColumn(name + "_moment")
                moments[i,j] = moment.to_numpy()[1]
            if i > 0 and i <=6:
                tableTime = osim.TimeSeriesTable(r'Main\Set-up\test\inverse_dynamics\Force_x_' + str(mag[i-1]) + '.sto')
                moment = tableTime.getDependentColumn(name + "_moment")
                moments[i,j] = moment.to_numpy()[1]
            if i > 6:
                tableTime = osim.TimeSeriesTable(r'Main\Set-up\test\inverse_dynamics\Force_z_' + str(mag[i-7]) + '.sto')
                moment = tableTime.getDependentColumn(name + "_moment")
                moments[i,j] = moment.to_numpy()[1]
        j += 1
  

    # Initialise linear regression and fit to find J
    model2 = LinearRegression(fit_intercept=False)
    model2.fit(forces, moments)

    # Get J from the linear regression
    J = model2.coef_

    # Take the pseudoinverse of J
    J_inv = np.linalg.pinv(J)
    print(J)
    print(J_inv)
    # Calculate H by multiplying J, M, and Fmax
    H = np.matmul(J_inv,np.matmul(M,Fmax))
    test = np.matmul(M,Fmax)

    model.setGravity(gravity)
    # Return H
    return H, test

# # Calculate H for position 1
# H1 = calc_H_test(model,s)


# # Create deflected position
# model2 = osim.Model(r"Main\Set-up\test\test_simple.osim")

# s2 = model2.initSystem()

# coord = model2.getCoordinateSet()
# coor = coord.get(0)

# coor.setValue(s2,1/180*np.pi)
# model2.equilibrateMuscles(s2)

# # Calculate H for deflected position
# H2 = calc_H_test(model2,s2)

# print(s.getY())
# print(s2.getY())
# print(H1)
# print(H2)

# # Initialise the activation vector
# activations = np.array([1,0,0])
# print(activations)

# # Get forces for both positions
# forces1 = np.matmul(H1,activations)
# forces2 = np.matmul(H2,activations)

# # Calculate deflection
# deflection = -1/180*np.pi * -0.5



# print(forces1)
# print(forces2)

# # Calculate stiffness
# stiffness = -(forces2-forces1)[0]/deflection
# print(stiffness)