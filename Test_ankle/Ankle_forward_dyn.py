#import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

#import opensim and other used libraries
import opensim as osim

import matplotlib.pyplot as plt

import xml.etree.ElementTree as ET
import numpy as np



#load opensim model
toylanding = osim.Model("ToyLandingModel.osim")

#scale model using preprepard scaling file
def scale_model():
    scale_tool = osim.ScaleTool("ToyLanding_Setup_Scale.xml")
    scale_tool.run()

#function to run forward simulation on a model and which controllers to use
def run_sim(Model, reflexes, cocontraction):

    #determine which controllers need to be turned on and which off
    for controller in Model.getControllerSet():
        if controller.getName() == "Reflexes":
            controller.set_enabled(reflexes)
            
        if controller.getName() == "R-inverter-controls" or controller.getName() == "R-everter-controls":
            controller.set_enabled(cocontraction)
    Model.printToXML(str(Model.getName()) + ".osim")

    #setup xml file
    tree = ET.parse('ToyLanding_Forward_Setup.xml')
    
    root = tree.getroot()
    root[0][0].text = str(Model.getName())+ ".osim"

    final_file = ET.tostring(root)
    with open("ToyLanding_Forward_Setup.xml", "wb") as f:
        f.write(final_file)

  

    #Make a manager that does the simulation
    manager = osim.ForwardTool("ToyLanding_Forward_Setup.xml")
    manager.run()

    #get data found in python simulation
    Table_python = osim.TimeSeriesTable('ResultsForward\ToyLandingModel_states_degrees.mot')

    #get reference data from simulation performed in OpenSimGUI
    #select the right one based on which controllers are activated
    if reflexes == False:
        if cocontraction == False:
            Table_simref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Simulate_no_controller.mot')
            Table_Forwardref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Forward_dynamics_no_controller.mot')
        else:
            Table_simref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Simulate_cocontraction.mot')
            Table_Forwardref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Forward_dynamics_cocontraction.mot')
    else:
        if cocontraction == False:
            Table_simref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Simulate_reflexes.mot')
            Table_Forwardref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Forward_dynamics_reflexes.mot')
        else:
            Table_simref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Simulate_all_controllers.mot')
            Table_Forwardref = osim.TimeSeriesTable('Simulate_VS_Forward_dynamics\Forward_dynamics_all_controllers.mot')
            

    # Get columns we want to analyze, and the time column (independent column).
    simref_subtalar_angle_r = Table_simref.getDependentColumn('/jointset/subtalar_r/subtalar_angle_r/value')
    Forwardref_subtalar_angle_r = Table_Forwardref.getDependentColumn('/jointset/subtalar_r/subtalar_angle_r/value')
    Python_subtalar_angle_r = Table_python.getDependentColumn('/jointset/subtalar_r/subtalar_angle_r/value')
    time1 = Table_simref.getIndependentColumn()
    time2 = Table_Forwardref.getIndependentColumn()
    time3 = Table_python.getIndependentColumn()


    # Plot the knee angles on the first subplot.
    plt.plot(time1, simref_subtalar_angle_r.to_numpy(), label='Simulation button')
    plt.plot(time2, Forwardref_subtalar_angle_r.to_numpy(), label='Forward dynamics')
    plt.plot(time3, Python_subtalar_angle_r.to_numpy(), label='Python')
    plt.title('subtalar angles, reflexes enabled: ' + str(reflexes) + ' cocontraction enabled: ' + str(cocontraction))
    plt.xlabel('Time')
    plt.ylabel('subtalar angle')
    plt.grid()
    plt.legend()
    plt.show()

scale_model()

#load opensim model
toylanding_scaled = osim.Model("ToyLandingModel_scaled.osim")
    
#call function for different combinations of controllers
run_sim(toylanding_scaled,False,False)
run_sim(toylanding_scaled,True,False)
run_sim(toylanding_scaled,False,True)
run_sim(toylanding_scaled,True,True)


#select body to get position from
calcn_r = toylanding.get_BodySet().get("calcn_r")

#retreive data from states file
storage = osim.Storage("ResultsForward\ToyLandingModel_states.sto")
state = toylanding.initSystem()
state_names = storage.getColumnLabels()
n_states = state_names.getSize()
sto_state = osim.ArrayDouble()
sto_state.setSize(n_states)
IK = osim.TimeSeriesTable('ResultsForward\ToyLandingModel_states.sto')
#initialise states list
position = []
#loop over all times in states file
for t in range(IK.getNumRows()):
    #retreive data at that time
    time = IK.getIndependentColumn()[t]
    storage.getDataAtTime(time,n_states,sto_state)
    #loop over all states at time t
    for i in range((state_names.getSize()-1)):
        #skip time column
        if state_names.getitem(i) == "time":
            continue
        #get values from each column
        else:
            sto_idx = storage.getStateIndex(state_names.getitem(i))
            state_value = sto_state.getitem(sto_idx)
            toylanding.setStateVariableValue(state,state_names.getitem(i),state_value)
    #assemble the state
    state.setTime(time)
    toylanding.assemble(state)
    #get postion in ground frame and store to position variable
    point = calcn_r.getPositionInGround(state)
    position.append(point.to_numpy().tolist())


#get time and turn position into numpy array
time = IK.getIndependentColumn()
position = np.array(position)

#plot coordinates
plt.plot(time, position[:,0], label='x coordinate')
plt.plot(time, position[:,1], label='y coordinate')
plt.plot(time, position[:,2], label='z coordinate')
plt.title('Position of the calcaneus')
plt.xlabel('Time')
plt.ylabel('coordinates')
plt.grid()
plt.legend()
plt.show()