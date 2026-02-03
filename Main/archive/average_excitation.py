# Class that generates a setup file for the CMC and then executes the CMC

# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import csv
import numpy as np


def average_excitation(states_table, model,t_begin,t_end):

    file_path = r"Main\Set-up\Moblarms\Initial_position\testing_10_90.sto"
    with open(file_path,newline='') as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            row = row

    controls = osim.ControlSet()

    i =42
    for muscle in model.getMuscles():
        
        excitation = states_table.getDependentColumn('/forceset/' + muscle.getName() + '/activation')
        average_exci = np.mean(excitation.to_numpy()[50:])
        row[i] = average_exci
        control = osim.ControlLinear()
        control.setName(muscle.getName() + ".excitation")
        control.setControlValue(t_begin, average_exci)
        control.setControlValue(t_end, average_exci)

        controls.cloneAndAppend(control)
        i +=2

    
    controls.printToXML("Main\Set-up\Moblarms" + "\controls.xml")
    delim = "\t"

    template = open(r"Main\Set-up\Moblarms\Initial_position\testing_10_90.sto",'r')
    text_kine = template.readlines()
    template.close()
    # Generate new header for stationary kinematics file
    text_kine[0] = "testing_init" + ".mot\t\t\t\t\t\t\t\t\t\n"
    text_kine.pop()
    
    text = delim.join(map(str,row))

   
    # Write new header to the stationary kinematics directory
    file = open(r"Main\Set-up\Moblarms\Initial_position\testing_init.sto","w")
    file.writelines(text_kine)
    file.close()
    file = open(r"Main\Set-up\Moblarms\Initial_position\testing_init.sto", "a")
    file.write(text)
    file.close()


model = osim.Model('Main\Set-up\Moblarms\MOBL_ARMS.osim')
state = osim.TimeSeriesTable("Main\Set-up\Moblarms\CMC\Results\MOBL_ARMS_CMCed_states.sto")
    
    
average_excitation(state, model, 0.03, 3)
    