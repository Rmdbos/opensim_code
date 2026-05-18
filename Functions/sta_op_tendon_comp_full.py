# Function that gets the activations needed to maintain a certain position for the test model

# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Point python where to find the source code for the class 
import sys
sys.path.insert(0, "Functions")


# Import opensim and other used libraries
import opensim as osim
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import cvxpy as cp






# Function that gets the activations needed to maintain a certain position for the test model
# model: the model for which to calculate the activations. Type: OpenSim model
# state: state of the model for which the activations needs to be calculated. Type: OpenSim state
def find_activations(model,state):

    # Initialise a solver that finds the muscle moment arms
    solverarm = osim.MomentArmSolver(model)

    # Initialise activation list and append number of CP variables to it equal to number of muscles
    activation = []
    for muscle in model.getMuscles():
        act = cp.Variable()
        activation.append(act)

    # Initialise empty contraint matrix
    constraint = []
    set = osim.ControlSet(r"Main\Set-up\test\statop\stat_op_moments_StaticOptimization_controls.xml")
    # Initialise j to 0 and loop over all coordinates
    j = 0
    for coordinate in model.getCoordinateSet():
        # Get the moment on the coordinate
        name = coordinate.getName()

        control = set.get(name + "_reserve")
            
        moment = control.getControlValue() * 10
        # Initialise i and the moment due to the muscle to 0 and loop over all muscles
        print(name)
            
        moment_musc = 0
        i = 0
        for muscle in model.getMuscles():
            print(muscle.getName())
            # Calculate cosine of the penation angle
            cospen = muscle.getCosPennationAngle(state)
            # Calculate maximum active fiber force at given fiber length
            force_active = muscle.getActiveFiberForce(state)/muscle.getActivation(state)
            # Calculate passive fiber force at given length
            force_passive = muscle.getPassiveFiberForce(state)
            # Calculate muscle moment arm relative to coordinate
            path = muscle.getGeometryPath()
            arm = solverarm.solve(state,coordinate,path)
            # Get the force and the moment on the coordinate due to the muscle
            force = (force_active*activation[i]+force_passive)*cospen
            moment_musc += arm*force
            print(arm)
            # Add one to i
              
            i += 1
            # Add new constrain that equalises the moment found using ID to the moments in the muscle
        constraint.append(moment == moment_musc)
        # for p in range(2):
        #     if p == 0:
        #         constraint.append(moment+(abs(moment*1)) >= moment_musc)
        #     if p == 1:
        #         constraint.append(moment-(abs(moment*1)) <= moment_musc)
        
        
        # Add one to j
        j += 1

    # Add constraints for minumum and maximum activation
    for i in range(len(activation)):
        constraint.append(activation[i] >= 0.02)
        constraint.append(activation[i] <= 1)


    # Create objective function from squares off all activations summed
    objective = 0
    for i in range(len(activation)):
        objective += activation[i]**2
    objective = cp.Minimize(objective)

    # # Define cvxpy problem
    prob = cp.Problem(objective, constraint)

    # # Solve the problem
    result = prob.solve(warm_start = False,verbose = False)

    # Return the found activations
    return activation

        






def loop_fibre_length(model,state):
    # Set all muscle activations to the same and equilibrate muscles
    for muscle in model.getMuscles():
        muscle.setActivation(state,0.5)
    model.equilibrateMuscles(state)

    # Initialise diff to 1 and j to 0
    diff = 1
    j = 0
    # Loop while diff is above the threshold and j below the max number of iterations
    while diff >= 1e-12 and j < 30:
        # Set diff to 0
        diff = 0
        # Get number of muscles
        num_muscles = round(model.getNumMuscleStates()/2)
        # Use the optimiser to find the activations for current fiber lengths
        activation = find_activations(model,state)
        # Set i to 0 and loop over all muscles
        i = 0
        for muscle in model.getMuscles():
            # Get old fiber length
            old = muscle.getFiberLength(state)
            # Update activation and fiber length based on findings from find_activations
            muscle.setActivation(state,float(activation[i].value))
            model.equilibrateMuscles(state)
            # Get new fiber lenght
            new = muscle.getFiberLength(state)
            # Calculate root mean square of differences
            diff += (old-new)**2
            i += 1
        diff = np.sqrt(diff/num_muscles)

        
        # Add one to j
        j += 1
        # Print exit statement if j goes over max number of iterations
        if j >= 30:
            print("maximum number of iterations exceeded, stopping solver")
    return(activation)


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



