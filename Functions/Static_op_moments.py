# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import Generate_force_files as fs

# Function that calculates the moments at each independent joint needed to calculate the muscle activations
def do_stat_op(file,file_name):

    # Use force setup class to create a forcefile for the inverse dynamics
    forcefile = fs.force_setup_file([0,0,1], 20, "Force_ID", r"Main\Set-up\Moblarms", "hand", "Right")
    forcefile.generate_force_file()
    forcefile.generate_force_setup()


    # Load instructions for static optimisation tool from file
    statop = osim.AnalyzeTool(file)
    # Specify stationary kinematics file from which to use coordinates
    statop.setCoordinatesFileName("Stationary_kinematics"'\\' + file_name)
    statop.setExternalLoadsFileName("Forward_dynamics\Right_forces.xml")
    statop.run()