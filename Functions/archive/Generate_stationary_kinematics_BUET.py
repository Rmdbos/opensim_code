# Class that transforms generic coordinate to ones used by DAS3 and writes the stationary kinematics file


# Import used libraries
import numpy as np

class stat_kine_file:
    # add_angle: the adduction angle of the shoulder in degrees. Type: double or numpy array
    # sh_flex_angle: the flexion angle of the shoulder in degrees. Type: double or numpy array
    # el_flex_angle: the flexion angle of the elbow in degrees. type: double or numpy array
    # setup_path: path to the relevant setup directory for both generated files. Type: string
    def __init__(self, add_angle, sh_flex_angle, el_flex_angle, setup_path):
        self.add_angle = add_angle
        self.sh_flex_angle = sh_flex_angle
        self.el_flex_angle = el_flex_angle
        self.setup_path = setup_path
        pass

    # Function takes three angles in degrees and returns the angles used by BUET in radians.
    # arm_flex_r is limited to between -90 and 180 as that is the maximum input for the model
    # arm_add_r is limited to between -120 and 90 degrees as that is the maximum input for the model
    # elbow_flex_r is limited to between 0 and 150 degrees as that is the maximum input for the model
    def coordinate_transformation(self):



        # Set range for arm_flex_r and caculate angle in radians
        self.sh_flex_angle = np.where(self.sh_flex_angle > 180, 180, self.sh_flex_angle)
        self.sh_flex_angle = np.where(self.sh_flex_angle < -90, -90, self.sh_flex_angle)
        self.arm_flex_r = self.sh_flex_angle/180*np.pi
        # set arm rotation to 0
        self.arm_rot_r = 0
        # Set range for arm_add_r and caculate angle in radians
        self.add_angle  = np.where(self.add_angle > 90, 90, self.add_angle)
        self.add_angle = np.where(self.add_angle < -120, -120, self.add_angle)
        self.arm_add_r = self.add_angle/180*np.pi
        # Set range for elbow_flex_r and caculate angle in radians
        self.el_flex_angle = np.where(self.el_flex_angle > 150, 150, self.el_flex_angle)
        self.el_flex_angle = np.where(self.el_flex_angle < 0, 0, self.el_flex_angle)
        self.elbow_flex_r = self.el_flex_angle/180*np.pi



    # Function that generates a stationary kinematics file for the DAS3 model
    # GH_y angle used for DAS3 in radians. Type: double
    # GH_z angle used for DAS3 in radians. Type: double
    # GH_yy angle used for DAS3 in radians. Type: double
    # EL_x angle used for DAS3 in radians. Type: double
    def stat_kine_file(self):

        # Generate file name for stationary kinematics file
        file_name_kine = "BUET_static_kinematics_GH_y_" + str(round(self.arm_flex_r*180/np.pi,1)) + "_arm_add_" + str(round(self.arm_add_r*180/np.pi,1)) + "_elbow_" + str(round(self.elbow_flex_r*180/np.pi,1))

        # Get template file for stationaty kinematics file
        template = open(self.setup_path + r"\templates\Initial_cond_template_BUET.sto",'r')
        text_kine = template.readlines()
        template.close()

        # Generate timetrace
        time = np.arange(0,3.01,0.01)


        # Generate new header for stationary kinematics file
        text_kine[0] = file_name_kine + ".mot\t\t\t\t\t\t\t\t\t\n"
        text_kine[2] = 'nRows=' + str(len(time)) + '\t\t\t\t\t\t\t\t\t\n'
        text_kine[3] = 'nColumns=' + str(17) + '\t\t\t\t\t\t\t\t\t\n'
        
   
        # Write new header to the stationary kinematics directory
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot',"w")
        file.writelines(text_kine)
        file.close()

        # Append the rows of stationary kinematics data to this new file
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot', "a")
        for i in range(len(time)):
            trace = str(time[i]) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(self.arm_flex_r) + "\t" + str(0) + "\t" + str(self.arm_add_r) + "\t" + str(0) + "\t" + str(self.arm_rot_r) + "\t" + str(0) + "\t" + str(self.elbow_flex_r) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\n"
            file.write(trace)
        file.close()
