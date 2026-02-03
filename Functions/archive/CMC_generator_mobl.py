# Class that generates a setup file for the CMC and then executes the CMC

# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import xml.etree.ElementTree as ET


class CMC_generator:
    # path_osim_model: the relative path to the OpenSim model. Type: string
    # path_results: the path where the results should be stored. Type: string
    # path_kinematics: the path to the stationary kinematics file. type: string
    # path_task: the path where the task file needs to be stored. Type: string
    def __init__(self, path_osim_model,path_results, path_kinematics, path_task):
        self.Osim_model = osim.Model(path_osim_model)
        self.setup_path = path_osim_model.replace(self.Osim_model.getName() + ".osim","")
        self.path_results = path_results
        self.path_kinematics = path_kinematics
        self.path_task = path_task


    # Function used to create the task file that is used by the CMC function
    def make_task_file(self):
        # Initialize a taskset that is used
        taskset =  osim.CMC_TaskSet()

        # Get all coordinates in the model
        for coordinate in self.Osim_model.getCoordinateSet():
            # Select all the coordinates that need to be tracked for the task
            if coordinate.getName() == "elv_angle" or coordinate.getName() == "shoulder_elv" or coordinate.getName() == "shoulder_rot" or coordinate.getName() == "elbow_flexion":
                # Initialize joint task and give it the required name and set to active
                task = osim.CMC_Joint()
                task.setName(coordinate.getName())
                task.setCoordinateName(coordinate.getName())
                task.setActive(True)
                task.setKP(100)
                task.setKV(20)
                # Add task to taskset
                taskset.cloneAndAppend(task)

        # Print the taskset to an XML file
        taskset.printToXML(self.path_task + r"\taskset.xml")


    # Function that creates the setup file for the CMC
    def make_setup_file(self):
        # Initiate CMC tool
        CMC_tool = osim.CMCTool()
        # Get the name from the model
        name = self.Osim_model.getName()
        # Use inbuild functionalities to give the CMCtool a name, path to the kinematics, path to the taskset. Store it in an xml file
        CMC_tool.setName(str(name) + "_CMCed")
        CMC_tool.setDesiredKinematicsFileName(self.path_kinematics)
        CMC_tool.setTaskSetFileName(r"taskset.xml")
        CMC_tool.printToXML(self.path_task + "\CMC.xml")

        # Get the XML file and store as root
        tree = ET.parse(self.path_task + "\CMC.xml")
        root = tree.getroot()

        # Add model to use for CMC
        root[0][0].text = '../' + self.Osim_model.getName() + ".osim"
        # Add where to store the results
        root[0][3].text = "./Results"
        # Set integrator and optimiser settings
        root[0][4].text = "20"
        root[0][8].text = "300000000"
        root[0][10].text = "0.0001"
        root[0][11].text = "0.0005"
        root[0][27].text = "2000"
        root[0][29].text = "true"
        # Set model to not use fast optimisation target
        root[0][23].text = "false"
        

        # Write changes to xml file
        final_file = ET.tostring(root)
        with open(self.path_task + "\CMC.xml", "wb") as f:
            f.write(final_file)







    # Function used to perform the CMC
    def run_CMC(self):
        # Initiate CMC tool and run it
        CMC_tool = osim.CMCTool(self.path_task + '\CMC.xml')
        CMC_tool.run()