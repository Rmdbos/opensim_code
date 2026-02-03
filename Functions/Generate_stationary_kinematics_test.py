# Class takes angle for the simpel model and writes the stationary kinematics file


# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")


# Import used libraries
import numpy as np



class stat_kine_file:
    # angle: angle to be given to the coordinate of the simpel model. Type: double
    # setup_path: path to the relevant setup directory for both generated files. Type: string
    def __init__(self, angle, setup_path):
        self.angle = angle
        self.setup_path = setup_path
        pass






    # Function that generates a stationary kinematics file for the simpel model
    # angle angle used for simpel model in radians. Type: double
    def stat_kine_file(self):

        # Generate file name for stationary kinematics file
        file_name_kine = "test_static_kinematics_angle_" + str(round(self.angle,1))

        # Get template file for stationaty kinematics file
        template = open(self.setup_path + r"\templates\Initial_cond_template_test.sto",'r')
        text_kine = template.readlines()
        template.close()

        # Generate timetrace
        time = np.arange(0,10.01,0.01)


        # Generate new header for stationary kinematics file
        text_kine[0] = file_name_kine + ".mot\t\t\t\t\t\t\t\t\t\n"
        text_kine[2] = 'nRows=' + str(len(time)) + '\t\t\t\t\t\t\t\t\t\n'
        text_kine[3] = 'nColumns=' + str(3) + '\t\t\t\t\t\t\t\t\t\n'
        
   
        # Write new header to the stationary kinematics directory
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot',"w")
        file.writelines(text_kine)
        file.close()

        # Append the rows of stationary kinematics data to this new file
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot', "a")
        for i in range(len(time)):
            trace = str(time[i]) + "\t" + str(self.angle/180*np.pi) + "\t" + str(0) + "\n"
            file.write(trace)
        file.close()


        