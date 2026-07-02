# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import Generate_force_files as fs


def do_stat_op(model,file_name):

    # forcefile = fs.force_setup_file([1,0,0],50, "Force_ID", r"Main\Set-up\test", "arm2", "model",[1,0,0],0)
    # forcefile.generate_force_file()
    # forcefile.generate_force_setup()


    # statop = osim.AnalyzeTool(file)
    # statop.setCoordinatesFileName("Stationary_kinematics"'\\' + file_name)
    # #statop.setExternalLoadsFileName("Forward_dynamics\model_forces.xml")
    # statop.run()
    
    ID = osim.InverseDynamicsTool()
    ID.set_results_directory(r"Main\Set-up\test\inverse_dynamics")
    ID.setCoordinatesFileName(r"Main\Set-up\test\Stationary_kinematics"'\\' + file_name)
    ID.setModel(model)
    muscles = osim.ArrayStr()
    muscles.append('Muscles')
    #ID.setExcludedForces(muscles)
    ID.setStartTime(0)
    ID.setEndTime(0.01)
    ID.setOutputGenForceFileName("Force_0.sto")
    ID.run()