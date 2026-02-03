# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import matplotlib.pyplot as plt
import numpy as np



# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\DAS3\CMC\Results\DAS3_CMCed_controls.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\DAS3\DAS3_controls.sto')
# Process the file.
# Print the column labels.
print(tableTime1.getColumnLabels())


# Get columns we want to analyze, and the time column (independent column).
bic_l_CMC = tableTime1.getDependentColumn('bic_l')
delt_scap_9_CMC = tableTime1.getDependentColumn('delt_scap_9')
bic_l_forward_CMC = tableTime2.getDependentColumn('bic_l')
delt_scap_9_forward_CMC = tableTime2.getDependentColumn('delt_scap_9')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()



# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('input muscle activations')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, bic_l_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, bic_l_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('activation')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, delt_scap_9_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, delt_scap_9_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('activation')
axs[1].grid()
axs[1].legend()







# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\DAS3\CMC\Results\DAS3_CMCed_states.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\DAS3\DAS3_states.sto')
# Process the file.
# Print the column labels.
print(tableTime1.getColumnLabels())


# Get columns we want to analyze, and the time column (independent column).
bic_l_CMC = tableTime1.getDependentColumn('/forceset/bic_l/activation')
delt_scap_9_CMC = tableTime1.getDependentColumn('/forceset/delt_scap_9/activation')
bic_l_forward_CMC = tableTime2.getDependentColumn('/forceset/bic_l/activation')
delt_scap_9_forward_CMC = tableTime2.getDependentColumn('/forceset/delt_scap_9/activation')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()



# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('actual muscle excitations')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, bic_l_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, bic_l_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('activation')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, delt_scap_9_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, delt_scap_9_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('activation')
axs[1].grid()
axs[1].legend()

# # Set the spacing between subplots
plt.subplots_adjust(wspace=0.5, hspace=0.5)



# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\DAS3\CMC\Results\DAS3_CMCed_Actuation_force.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\DAS3\DAS3_Actuation_force.sto')
# Process the file.
# Print the column labels.
print(tableTime1.getColumnLabels())


# Get columns we want to analyze, and the time column (independent column).
bic_l_CMC = tableTime1.getDependentColumn('bic_l')
delt_scap_9_CMC = tableTime1.getDependentColumn('delt_scap_9')
bic_l_forward_CMC = tableTime2.getDependentColumn('bic_l')
delt_scap_9_forward_CMC = tableTime2.getDependentColumn('delt_scap_9')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()



# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('muscle forces')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, bic_l_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, bic_l_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('force')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, delt_scap_9_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, delt_scap_9_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('force')
axs[1].grid()
axs[1].legend()

# # Set the spacing between subplots
plt.subplots_adjust(wspace=0.5, hspace=0.5)
plt.show()

