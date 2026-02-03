# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import numpy as np


# Function used to find the position of a body in the ground reference frame
# Model: this is the model used in the forward simulation to be analysed Type: OpenSim model
# IMPORTANT the name of the OpenSim model needs to be the same as the name of the .osim file
# body: the name of the body from the model that is investigated Type: string
# state_file: path to the state file created in the forward simulation Type: string
def position_in_ground(Model, body, state_file):
    # Get the body that needs to be analysed
    body_intrest = Model.get_BodySet().get(body)

    # Retreive data from states file
    storage = osim.Storage(state_file)
    state = Model.initSystem()
    state_names = storage.getColumnLabels()
    n_states = state_names.getSize()
    sto_state = osim.ArrayDouble()
    sto_state.setSize(n_states)
    IK = osim.TimeSeriesTable(state_file)
    # Initialise states list
    position = []

    # Loop over all times in states file
    for t in range(IK.getNumRows()):
        # Retreive data at that time
        time = IK.getIndependentColumn()[t]
        storage.getDataAtTime(time,n_states,sto_state)
        # Loop over all states at time t
        for i in range((state_names.getSize()-1)):
            # Skip time column
            if state_names.getitem(i) == "time":
                continue
            # Get values from each column
            else:
                sto_idx = storage.getStateIndex(state_names.getitem(i))
                state_value = sto_state.getitem(sto_idx)
                Model.setStateVariableValue(state,state_names.getitem(i),state_value)
        # Assemble the state
        state.setTime(time)
        Model.assemble(state)
        # Get postion in ground frame and store to position variable
        point = body_intrest.getPositionInGround(state)
        position.append(point.to_numpy().tolist())

    # Turn position into numpy array
    position = np.array(position)
    return position