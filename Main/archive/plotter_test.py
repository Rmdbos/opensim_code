# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import matplotlib.pyplot as plt
import numpy as np



# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_controls.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_controls.sto')
# Process the file.



# Get columns we want to analyze, and the time column (independent column).
muscle1_CMC = tableTime1.getDependentColumn('muscle1')
muscle2_CMC = tableTime1.getDependentColumn('muscle2')
muscle1_forward_CMC = tableTime2.getDependentColumn('muscle1')
muscle2_forward_CMC = tableTime2.getDependentColumn('muscle2')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()

print(np.mean(muscle2_CMC.to_numpy()))

# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('input muscle activations')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, muscle1_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, muscle1_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('activation')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, muscle2_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, muscle2_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('activation')
axs[1].grid()
axs[1].legend()










# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_states.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_states.sto')
# Process the file.



# Get columns we want to analyze, and the time column (independent column).
muscle1_CMC = tableTime1.getDependentColumn('/forceset/muscle1/activation')
muscle2_CMC = tableTime1.getDependentColumn('/forceset/muscle2/activation')
muscle1_forward_CMC = tableTime2.getDependentColumn('/forceset/muscle1/activation')
muscle2_forward_CMC = tableTime2.getDependentColumn('/forceset/muscle2/activation')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()

print(np.mean(muscle2_CMC.to_numpy()))

# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('actual muscle excitations')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, muscle1_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, muscle1_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('excitation')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, muscle2_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, muscle2_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('excitation')
axs[1].grid()
axs[1].legend()

# # Set the spacing between subplots
plt.subplots_adjust(wspace=0.5, hspace=0.5)










# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_states.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_states.sto')
# Process the file.


# Get columns we want to analyze, and the time column (independent column).
muscle1_CMC = tableTime1.getDependentColumn('/forceset/muscle1/fiber_length')
muscle2_CMC = tableTime1.getDependentColumn('/forceset/muscle2/fiber_length')
muscle1_forward_CMC = tableTime2.getDependentColumn('/forceset/muscle1/fiber_length')
muscle2_forward_CMC = tableTime2.getDependentColumn('/forceset/muscle2/fiber_length')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()



# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('muscle fibre fiber_length')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, muscle1_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, muscle1_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('fiber_length')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, muscle2_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, muscle2_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('fiber_length')
axs[1].grid()
axs[1].legend()

# # Set the spacing between subplots
plt.subplots_adjust(wspace=0.5, hspace=0.5)







# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_Actuation_speed.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_Actuation_speed.sto')
# Process the file.



# Get columns we want to analyze, and the time column (independent column).
muscle1_CMC = tableTime1.getDependentColumn('muscle1')
muscle2_CMC = tableTime1.getDependentColumn('muscle2')
muscle1_forward_CMC = tableTime2.getDependentColumn('muscle1')
muscle2_forward_CMC = tableTime2.getDependentColumn('muscle2')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()



# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('muscle speeds')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, muscle1_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, muscle1_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('speed')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, muscle2_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, muscle2_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('speed')
axs[1].grid()
axs[1].legend()

# # Set the spacing between subplots
plt.subplots_adjust(wspace=0.5, hspace=0.5)









# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_Actuation_force.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_Actuation_force.sto')
# Process the file.



# Get columns we want to analyze, and the time column (independent column).
muscle1_CMC = tableTime1.getDependentColumn('muscle1')
muscle2_CMC = tableTime1.getDependentColumn('muscle2')
muscle1_forward_CMC = tableTime2.getDependentColumn('muscle1')
muscle2_forward_CMC = tableTime2.getDependentColumn('muscle2')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()



# Create six subplots, with 2 rows and 3 columns.
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('muscle forces')

# Plot muscle 1 activations on the first subplot.
axs[0].plot(x_time1, muscle1_CMC.to_numpy(), label='CMC result')
axs[0].plot(x_time2, muscle1_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs[0].set_title('Muscle 1')
axs[0].set_xlabel('Time')
axs[0].set_ylabel('force')
axs[0].grid()
axs[0].legend()

# Plot the muscle 2 activations on the second subplot.
axs[1].plot(x_time1, muscle2_CMC.to_numpy(), label='CMC result')
axs[1].plot(x_time2, muscle2_forward_CMC.to_numpy(), label='Forward with CMC controls')
axs[1].set_title('Muscle 2')
axs[1].set_xlabel('Time')
axs[1].set_ylabel('force')
axs[1].grid()
axs[1].legend()

# # Set the spacing between subplots
plt.subplots_adjust(wspace=0.5, hspace=0.5)








# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_Kinematics_dudt.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_Kinematics_dudt.sto')
# Process the file.



# Get columns we want to analyze, and the time column (independent column).
rot_coord_0_CMC = tableTime1.getDependentColumn('rot_coord_0')
rot_coord_0_forward_CMC = tableTime2.getDependentColumn('rot_coord_0')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()




fig, axs = plt.subplots(1, 1, figsize=(10, 10))
fig.suptitle('rotational accelerations')
# Plot muscle 1 activations on the first subplot.
axs.plot(x_time1, rot_coord_0_CMC.to_numpy(), label='CMC result')
axs.plot(x_time2, rot_coord_0_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs.set_title('rotation du/dt')
axs.set_xlabel('Time')
axs.set_ylabel('acceleration')
axs.grid()
axs.legend()







# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_Kinematics_u.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_Kinematics_u.sto')
# Process the file.



# Get columns we want to analyze, and the time column (independent column).
rot_coord_0_CMC = tableTime1.getDependentColumn('rot_coord_0')
rot_coord_0_forward_CMC = tableTime2.getDependentColumn('rot_coord_0')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()




fig, axs = plt.subplots(1, 1, figsize=(10, 10))
fig.suptitle('rotational speeds')
# Plot muscle 1 activations on the first subplot.
axs.plot(x_time1, rot_coord_0_CMC.to_numpy(), label='CMC result')
axs.plot(x_time2, rot_coord_0_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs.set_title('rotation u')
axs.set_xlabel('Time')
axs.set_ylabel('speed')
axs.grid()
axs.legend()





# Use the TableProcessor to read the motion file.
tableTime1 = osim.TimeSeriesTable(r'Main\Set-up\test\CMC\Results\model_CMCed_Kinematics_q.sto')
tableTime2 = osim.TimeSeriesTable(r'Main\Set-up\test\Forward_dynamics\results\model_Kinematics_q.sto')
# Process the file.



# Get columns we want to analyze, and the time column (independent column).
rot_coord_0_CMC = tableTime1.getDependentColumn('rot_coord_0')
rot_coord_0_forward_CMC = tableTime2.getDependentColumn('rot_coord_0')
# bicep_b2 = tableTime.getDependentColumn('/forceset/bic_b_2/activation')
# deltoid = tableTime.getDependentColumn('/forceset/lat_dorsi_1/activation')
x_time1 = tableTime1.getIndependentColumn()
x_time2 = tableTime2.getIndependentColumn()




fig, axs = plt.subplots(1, 1, figsize=(10, 10))
fig.suptitle('angles')
# Plot muscle 1 activations on the first subplot.
axs.plot(x_time1, rot_coord_0_CMC.to_numpy(), label='CMC result')
axs.plot(x_time2, rot_coord_0_forward_CMC.to_numpy(), label='Forward with CMC controls')
#axs[0].plot(x_time, bicep_b2.to_numpy(), label='bicep b2')
axs.set_title('angles q')
axs.set_xlabel('Time')
axs.set_ylabel('angle')
axs.grid()
axs.legend()



plt.show()

