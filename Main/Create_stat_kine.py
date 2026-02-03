# Uses initial_cond_file class to generate a file containing the initial conditions for a forward simulation and a stationary kinematics file



# Tell python where to find the source code for the class
import sys
sys.path.insert(0, "Functions")

# Import the class used
import Generate_stationary_kinematics_test as sk


# Create object using the class, given angles for the joints and a path to the setup directory
position_file = sk.stat_kine_file(30,r'Main\Set-up\test')


# Write the initial position and stationary kinematics file
position_file.stat_kine_file()

