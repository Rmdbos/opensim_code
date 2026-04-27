# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import matplotlib.pyplot as plt
import numpy as np




# Use the TableProcessor to read the motion file.
tableTime41 = osim.TimeSeriesTable(r'testing_4.1_4.5\gravity_4.1_fixed_oldSUP\Right_states_degrees.mot')
tableTime45 = osim.TimeSeriesTable(r'testing_4.1_4.5\gravity_4.1_fixed_newSUP\Right_states_degrees.mot')



x_time41 = tableTime41.getIndependentColumn()
x_time45 = tableTime45.getIndependentColumn()



for column in tableTime41.getColumnLabels():
    data41 = tableTime41.getDependentColumn(column)
    data45 = tableTime45.getDependentColumn(column)
    

    columnclean = column.replace('/','')

    
    

    plt.plot(x_time41, data41.to_numpy(), label='simulation in 4.1 with old supinator')
    plt.plot(x_time45, data45.to_numpy(), label='simulation in 4.1 with new supinator')
    plt.title(column)
    plt.xlabel('Time')
    plt.ylabel('see title')
    plt.grid()
    plt.legend()
    plt.savefig(r"testing_4.1_4.5/comparison_plots_4.1_oldnew/plot" +  columnclean + ".png")
    plt.clf()
