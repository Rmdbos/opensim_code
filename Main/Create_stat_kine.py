# Uses initial_cond_file class to generate a file containing the initial conditions for a forward simulation and a stationary kinematics file



# Tell python where to find the source code for the class
import sys
sys.path.insert(0, "Functions")

# Import the class used
import Generate_stationary_kinematics_MOBL as sk


# Create object using the class, given angles for the joints and a path to the setup directory
position_file = sk.stat_kine_file(r'Main\Set-up\Moblarms',20,0,90,0,0,0,0)

position_file.coordinate_transformation()

position_file.find_related_coor()
# Write the initial position and stationary kinematics file
position_file.stat_kine_file_H()

