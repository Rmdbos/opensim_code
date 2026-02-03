# Class related to the scaling of OpenSim models
# make_setup_file creates the xml file that can be used in a scaletool to scale an OpenSim model
# scale_model takes an xml setup file and than runs the scaletool to scale the model


# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Import opensim and other used libraries
import opensim as osim
import xml.etree.ElementTree as ET

class model_scaler:
    # Function takes paths to both the OpenSim model and Human Library model and uses that to fill in the properties.
    # Type: string for both
    # Model: this is the model to be scaled Type: OpenSim model
    # IMPORTANT the name of the OpenSim model needs to be the same as the name of the .osim file
    # mass: the mass of the subject, this mass will be distrubuted over the bodies in the same ratios as the original model Type: double
    # height: the height of the subject, is not actually used in scaling just copied into the xml file Type: double
    # scales: A list with two columns. in the left column the names of the bodies in strings, in the right column their scaling factors. 
    # Example: scales = [["bone",1.1],["bone2",1.1]]. Type: python list.
    def __init__(self, path_osim_model, path_Human_library_model, scale_test, mass_test, Height_test):
        self.Osim_model = osim.Model(path_osim_model)
        self.HL_model = path_Human_library_model
        self.setup_path = path_osim_model.replace(self.Osim_model.getName() + ".osim","")
        self.scales = scale_test
        self.mass = mass_test
        self.height = Height_test


    
    

    # Function used to create an xml file that can be used in scaling of OpenSim models
    def make_setup_file(self):
        # Initiate scale tool
        scale_tool = osim.ScaleTool()
        # Get the name from the model
        name = self.Osim_model.getName()
        # Use inbuild functionalities to give the scaletool a name, mass, height and age. Store it in an xml file
        scale_tool.setName(str(name) + "_scaled")
        scale_tool.setSubjectMass(self.mass)
        scale_tool.setSubjectHeight(self.height)
        scale_tool.setSubjectAge(22)
        scale_tool.printToXML(self.setup_path + str(name) + "_Setup_Scale.xml")
        # Open that xml file using elementtree
        tree = ET.parse(self.setup_path + str(name) + "_Setup_Scale.xml")
        root = tree.getroot()
        # Use elementtree to edit the file using some basic information and which model to scale
        root[0][3].text = "setup file for scaling " + str(name)
        root[0][4][0].text = str(name) + ".osim"
        root[0][4].remove(root[0][4][1])
        root[0][5][1].text = "manualScale"
        root[0][5].remove(root[0][5][2])
        # Loop over scales to add each body and their scaling factor to the file
        for i in range(len(self.scales)):
            scale = ET.SubElement(root[0][5][2][0],'Scale')
            scaled = ET.SubElement(scale,'scales')
            scaled.text = str(self.scales[i][1]) + "    " + str(self.scales[i][1]) + "    " + str(self.scales[i][1])
            segment = ET.SubElement(scale, 'segment')
            segment.text = self.scales[i][0]
            apply = ET.SubElement(scale, 'apply')
            apply.text = 'true'
        # Remove several unused blocks
        root[0][5].remove(root[0][5][3])
        root[0][5].remove(root[0][5][3])
        # Set preserve mass distribution to true
        root[0][5][3].text = "true"
        # Specify in which file to store the new model and where to store the applied scaling factors
        root[0][5][4].text = str(name) + "_scaled.osim"
        root[0][5][5].text = r"Scale_files"'\\' + str(name) + "_scaleSet_applied.xml"
        root[0].remove(root[0][6])


        # Write changes to xml file
        final_file = ET.tostring(root)
        with open(self.setup_path + str(name) + "_Setup_Scale.xml", "wb") as f:
            f.write(final_file)






    # Function used to scale opensim models
    def scale_model(self):
        # Get model name
        name = self.Osim_model.getName()
        print(name)
        # Initiate scale tool and run it
        scale_tool = osim.ScaleTool(self.setup_path + str(name) + "_Setup_Scale.xml")
        scale_tool.run()