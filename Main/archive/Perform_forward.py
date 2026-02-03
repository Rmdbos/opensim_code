# Uses several functions to perform CMC on the opensim model

# Tell python where to find the Functions
import sys
sys.path.insert(0, "Functions")

# Import used class
import Forward_dynamics_test as FD


# Setup the generator
forward = FD.forward_sim_generator(r"Main\Set-up\test\test_simple.osim", r'Main\Set-up\test\Forward_dynamics')

# Make the task file
forward.create_forward_file()

forward.run_forward()