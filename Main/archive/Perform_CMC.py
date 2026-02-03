# Uses several functions to perform CMC on the opensim model

# Tell python where to find the Functions
import sys
sys.path.insert(0, "Functions")

# Import used class
import CMC_generator_test as CMC


# Setup the generator
CMC_test = CMC.CMC_generator(r"Main\Set-up\test\test_simple.osim", r'Main\Set-up\test\CMC\Results', r'../Stationary_kinematics\test_static_kinematics_angle_30.mot', r"Main\Set-up\test\CMC")

# Make the task file
CMC_test.make_task_file()

# Make the setup file
CMC_test.make_setup_file()

# Run the CMC
#CMC_test.run_CMC()



