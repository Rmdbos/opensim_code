# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim


def do_stat_op(file,file_name):

    statop = osim.AnalyzeTool(file)
    statop.setCoordinatesFileName("../Stationary_kinematics"'\\' + file_name)
    statop.run()