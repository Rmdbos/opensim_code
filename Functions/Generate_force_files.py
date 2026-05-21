# Class that generates a file with the timetraces of a force applied to a body between 0.4 and 0.7 seconds during an OpenSim simulation and the xml file to be given to the forward simulation

# Import used libraries
import numpy as np
import xml.etree.ElementTree as ET


# direction: a unit vector that describes the direction in which the force is applied on the body. Type: 3 long list or numpy array
# magnitude: magnitude of the force applied to the body in Newton. Type: double
# force_file_name: the name to be given to the file where the timetrace is to be stored. Type: string
# setup_path: path to the relevant setup directory for the model. Here the used templates can be found and the new files are stored Type: string
# body_of_interest: name of the body that the force is applied to. Type: string
# model_name: name of the model the force is applied to. Used to generate the filename. Type: string
class force_setup_file:
    def __init__(self, direction, magnitude, force_file_name, setup_path, body_of_interest, model_name):
            self.direction = direction
            self.magnitude = magnitude
            self.file_name = force_file_name
            self.setup_path = setup_path
            self.body_of_interest = body_of_interest
            self.model_name = model_name
            




    # Function generates a file with timetraces of a force and torque applied to a point on the body
    def generate_force_file(self):
        # Generate the first column with the timestamps
        time = np.arange(0,3.001,0.001)

        # Make sure the direction vector is unit length and create a block function describing each force scaled by magnitude and direction
        direction = self.direction/(np.sqrt(self.direction[0]**2+self.direction[1]**2+self.direction[2]**2))
        force_vx = np.heaviside(time,1) * self.magnitude * direction[0]
        force_vy = np.heaviside(time,1) * self.magnitude * direction[1]
        force_vz = np.heaviside(time,1) * self.magnitude * direction[2]

        # Give force application point as body center
        force_px = np.zeros(len(time))
        force_py = np.zeros(len(time))
        force_pz = np.zeros(len(time))


   

        # # Give torque in all directions as zero
        torque_x = np.zeros(len(time))
        torque_y = np.zeros(len(time))
        torque_z = np.zeros(len(time))

        # Open and store template file
        template = open(self.setup_path + r"\templates\Force_file_template.mot",'r')
        text = template.readlines()
        template.close()

        # Generate new header
        text[0] = self.file_name + ".mot\t\t\t\t\t\t\t\t\t\n"
        text[2] = 'nRows=' + str(len(time)) + '\t\t\t\t\t\t\t\t\t\n'
        text[3] = 'nColumns=' + str(10) + '\t\t\t\t\t\t\t\t\t\n'
        
        # Get path to folder containing the setup force files and write new header there
        file = open(self.setup_path + r"\Forward_dynamics\Force_files""\\" + str(self.file_name) + '.mot',"w")
        file.writelines(text)
        file.close()

        # Append the rows of data to this new file
        file = open(self.setup_path + r"\Forward_dynamics\Force_files""\\" + str(self.file_name) + '.mot', "a")
        for i in range(len(time)):
            trace = str(time[i]) + "\t" + str(force_vx[i]) + "\t" + str(force_vy[i]) + "\t" + str(force_vz[i]) + "\t" + str(force_px[i]) + "\t" + str(force_py[i]) + "\t" + str(force_pz[i]) + "\t" + str(torque_x[i]) + "\t" + str(torque_y[i]) + "\t" + str(torque_z[i]) + "\n"
            file.write(trace)
        file.close()

    # Function that generates the .xml file used to setup the force by the forward dynamics tool
    def generate_force_setup(self):
        # Open template file for the .xml
        tree = ET.parse(self.setup_path + r"\templates\template_forces.xml")
        root = tree.getroot()

        # Change the body the force is applied to and the name of the file containing the forces
        root[0][0][0][1].text = self.body_of_interest
        root[0][0][0][3].text = self.body_of_interest
        root[0][2].text = r"Force_files""\\" + str(self.file_name) + '.mot'

        # Write the new file to the forward dynamics setup folder
        file = ET.tostring(root)
        with open(self.setup_path + r"\Forward_dynamics"'\\' + self.model_name + "_forces.xml", "wb") as f:
            f.write(file)

