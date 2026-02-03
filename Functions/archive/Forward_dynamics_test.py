# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import xml.etree.ElementTree as ET




class forward_sim_generator:
    # path_osim_model: the relative path to the OpenSim model. Type: string
    # path_results: the path where the results should be stored. Type: string
    # path_kinematics: the path to the stationary kinematics file. type: string
    # path_task: the path where the task file needs to be stored. Type: string
    def __init__(self, path_osim_model, path_forward):
        self.Osim_model = osim.Model(path_osim_model)
        self.path_forward = path_forward


    # Function to run forward simulation on a model and which controllers to use
    def create_forward_file(self):

        forward_tool = osim.ForwardTool()
        forward_tool.setControlsFileName("../CMC\Results\model_CMCed_controls.xml")
        forward_tool.setStatesFileName("../CMC\Results\model_CMCed_states.sto")
        forward_tool.setInitialTime(0.03)
        forward_tool.setFinalTime(9.99)
        forward_tool.setModelFilename("../test_simple.osim")
        forward_tool.setResultsDir(r"\results")
        forward_tool.setSolveForEquilibrium(False)
        forward_tool.setUseSpecifiedDt(True)

        forward_tool.printToXML(self.path_forward + r"\forward_setup.xml")


        # # Setup xml file
        # tree = ET.parse('ToyLanding_Forward_Setup.xml')
        
        # root = tree.getroot()
        # root[0][0].text = str(Model.getName())+ ".osim"

        # final_file = ET.tostring(root)
        # with open("ToyLanding_Forward_Setup.xml", "wb") as f:
        #     f.write(final_file)

        




    # Function used to perform the forward simulation
    def run_forward(self):
        # Initiate forward tool and run it
        forward_tool = osim.ForwardTool(self.path_forward + r"\forward_setup.xml")
        forward_tool.run()

