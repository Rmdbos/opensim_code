# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Point python where to find the source code for the class 

import sys
sys.path.insert(0, "Functions")


# Import opensim and other used libraries
import opensim as osim



# Initialise model and state and set coordinate angle
model = osim.Model(r"Weird_inverse_dyn\test_simple_dependent.osim")

# initialise system and store state
state = model.initSystem()

# Check state
print(state.getY())

# # If you call equilibrate muscles before the inverse dynamics tool the muscle forces are always incorrect
# for muscle in model.getMuscles():
#     muscle.setActivation(state,0.5)
# model.equilibrateMuscles(state)


# Run the inverse dynamics tool for the model in its default position
# Muscles are excluded as for some models including the muscles leads to the wrong results
ID = osim.InverseDynamicsTool()
ID.set_results_directory(r"Weird_inverse_dyn")
ID.setCoordinatesFileName(r"Weird_inverse_dyn\test_static_kinematics_ID_angle_0.mot")
ID.setModel(model)
muscles = osim.ArrayStr()
muscles.append('Muscles')
ID.setExcludedForces(muscles) #commenting this line out results in the code returning the correct results
ID.setStartTime(0)
ID.setEndTime(0.01)
ID.setOutputGenForceFileName("results_invdyn")
ID.run()

# Check state
print(state.getY())

# Equilibrating the muscles is needed after the inverse dynamics tool
for muscle in model.getMuscles():
    muscle.setActivation(state,0.5)
model.equilibrateMuscles(state)



# Loop over all coordinates
for coordinate in model.getCoordinateSet():   
    name = coordinate.getName()
    # only take the coordinates that we are interested in 
    if name == "rot_coord_0":     
        for muscle in model.getMuscles():
            # Print muscle name
            print("Muscle name: " + str(muscle.getName()))
            # Calculate maximum active fiber force at given fiber length
            force_active = muscle.getActiveFiberForce(state)
            print("Muscle active force: " + str(force_active))
            # Calculate passive fiber force at given length
            force_passive = muscle.getPassiveFiberForce(state)
            print("Muscle passive force: " + str(force_passive))
            # Add one to i
            

# Correct output:                                           incorrect output:

# Muscle name: muscle1					                    Muscle name: muscle1
# Muscle active force: 225.45634006568682					Muscle active force: -7.61368255264883e-29
# Muscle passive force: 14.046425700396918					Muscle passive force: 32595.767468863603
# Muscle name: muscle2					                    Muscle name: muscle2
# Muscle active force: 225.45634006568682					Muscle active force: -7.61368255264883e-29
# Muscle passive force: 14.046425700396918					Muscle passive force: 32595.767468863603
# Muscle name: muscle3					                    Muscle name: muscle3
# Muscle active force: 249.99887568629634					Muscle active force: 0.0
# Muscle passive force: 1.5580423778744662e-08				Muscle passive force: 31010.969387755067
# Muscle name: muscle4					                    Muscle name: muscle4
# Muscle active force: 249.99887568629634					Muscle active force: 0.0
# Muscle passive force: 1.5580423778744662e-08				Muscle passive force: 31010.969387755067
