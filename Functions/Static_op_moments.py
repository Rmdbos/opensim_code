# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim

# Function that calculates the moments at each independent joint needed to calculate the muscle activations
def do_stat_op(file,file_name):
    # Load instructions for static optimisation tool from file
    statop = osim.AnalyzeTool(file)
    # Specify stationary kinematics file from which to use coordinates
    statop.setCoordinatesFileName("../Stationary_kinematics"'\\' + file_name)
    statop.run()