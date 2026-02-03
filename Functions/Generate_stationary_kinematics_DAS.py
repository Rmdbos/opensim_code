# Class that transforms generic coordinate to ones used by DAS3 and writes the stationary kinematics file


# Import used libraries
import numpy as np

class stat_kine_file:
    # abd_angle: the abduction angle of the shoulder in degrees. Type: double or numpy array
    # sh_flex_angle: the flexion angle of the shoulder in degrees. Type: double or numpy array
    # el_flex_angle: the flexion angle of the elbow in degrees. type: double or numpy array
    # setup_path: path to the relevant setup directory for both generated files. Type: string
    def __init__(self, setup_path, abd_angle = 0, sh_flex_angle =0, el_flex_angle = 0, GH_y = 0, GH_z = 0, GH_yy = 0, EL_x = 0):
        self.abd_angle = abd_angle
        self.sh_flex_angle = sh_flex_angle
        self.el_flex_angle = el_flex_angle
        self.setup_path = setup_path
        self.GH_y = GH_y
        self.GH_z = GH_z
        self.GH_yy = GH_yy
        self.EL_x = EL_x
        pass

    # Function takes three angles in degrees and returns the angles used by DAS3 in radians.
    # GH_y and GH_yy are limited to between -pi/2 to pi/2 due to the way they are calculated
    # GH_z is limited to between -30 and 84 degrees as that is the maximum input for the model
    # EL_X is limited to between 5 and 140 degrees as that is the maximum input for the model
    def coordinate_transformation(self):

        # add 0.001 degree to both angles to avoid numbers going to infinity and so np.sign doesn't return 0
        if self.abd_angle == 0:
            self.abd_angle = self.abd_angle + 0.001
        if self.sh_flex_angle == 0:
            self.sh_flex_angle = self.sh_flex_angle + 0.001

        # Calculate GH_y from the ratio betwen sh_flex_angle and abd_angle
        self.GH_y = np.arctan(self.sh_flex_angle/self.abd_angle)
        # Rotate arm back into place with GH_yy
        self.GH_yy = -self.GH_y
        # Get GH_z using pythagoras and ensure signs are correct
        GH_z = np.sqrt(np.square(self.abd_angle)+np.square(self.sh_flex_angle))*np.sign(self.abd_angle)*np.sign(self.sh_flex_angle)
        # Enforce limits for GH_z and convert to radians
        GH_z = np.where(GH_z > 84, 84, GH_z)
        GH_z = np.where(GH_z < -30, -30, GH_z)
        self.GH_z = GH_z/180*np.pi
        # Enforce limits for EL_x and convert to radians
        self.el_flex_angle = np.where(self.el_flex_angle > 140, 140, self.el_flex_angle)
        self.el_flex_angle = np.where(self.el_flex_angle < 5, 5, self.el_flex_angle)
        self.EL_x = self.el_flex_angle/180*np.pi



    # Function that generates a stationary kinematics file for the DAS3 model
    # GH_y angle used for DAS3 in radians. Type: double
    # GH_z angle used for DAS3 in radians. Type: double
    # GH_yy angle used for DAS3 in radians. Type: double
    # EL_x angle used for DAS3 in radians. Type: double
    def stat_kine_file(self):

        # Generate file name for stationary kinematics file
        file_name_kine = "DAS_static_kinematics_GH_y_" + str(round(self.GH_y*180/np.pi,1)) + "_GH_z_" + str(round(self.GH_z*180/np.pi,1)) + "_EL_x_" + str(round(self.EL_x*180/np.pi,1))

        # Get template file for stationaty kinematics file
        template = open(self.setup_path + r"\templates\Initial_cond_template_DAS.sto",'r')
        text_kine = template.readlines()
        template.close()

        # Generate timetrace
        time = np.arange(0,3.01,0.01)


        # Generate new header for stationary kinematics file
        text_kine[0] = file_name_kine + ".mot\t\t\t\t\t\t\t\t\t\n"
        text_kine[2] = 'nRows=' + str(len(time)) + '\t\t\t\t\t\t\t\t\t\n'
        text_kine[3] = 'nColumns=' + str(23) + '\t\t\t\t\t\t\t\t\t\n'
        
   
        # Write new header to the stationary kinematics directory
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot',"w")
        file.writelines(text_kine)
        file.close()

        # Append the rows of stationary kinematics data to this new file
        # file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot', "a")
        # for i in range(len(time)):
        #     trace = str(time[i]) + "\t" + str(-33.486/180*np.pi) + "\t" + str(0) + "\t" + str(5.002/180*np.pi) + "\t" + str(0) + "\t" + str(32.914/180*np.pi) + "\t" + str(0) + "\t" + str(45.571/180*np.pi) + "\t" + str(0) + "\t" + str(0.458/180*np.pi) + "\t" + str(0) + "\t" + str(-12.062/180*np.pi) + "\t" + str(0) + "\t" + str(self.GH_y) + "\t" + str(0) + "\t" + str(self.GH_z) + "\t" + str(0) + "\t" + str(self.GH_yy) + "\t" + str(0) + "\t" + str(self.EL_x) + "\t" + str(0) + "\t" + str(5/180*np.pi) + "\t" + str(0) + "\n"
        #     file.write(trace)
        # file.close()


        # Append the rows of stationary kinematics data to this new file
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot', "a")
        for i in range(len(time)):
            trace = str(time[i]) + "\t" + str(-33.486/180*np.pi) + "\t" + str(0) + "\t" + str(5.002/180*np.pi) + "\t" + str(0) + "\t" + str(32.914/180*np.pi) + "\t" + str(0) + "\t" + str(45.571/180*np.pi) + "\t" + str(0) + "\t" + str(0.458/180*np.pi) + "\t" + str(0) + "\t" + str(-12.062/180*np.pi) + "\t" + str(0) + "\t" + str(-1.433/180*np.pi) + "\t" + str(0) + "\t" + str(10.058/180*np.pi) + "\t" + str(0) + "\t" + str(1.414/180*np.pi) + "\t" + str(0) + "\t" + str(5/180*np.pi) + "\t" + str(0) + "\t" + str(5/180*np.pi) + "\t" + str(0) + "\n"
            file.write(trace)
        file.close()



    # Function that generates a stationary kinematics file for the DAS3 model for calculating the H matrix
    # GH_y angle used for DAS3 in radians. Type: double
    # GH_z angle used for DAS3 in radians. Type: double
    # GH_yy angle used for DAS3 in radians. Type: double
    # EL_x angle used for DAS3 in radians. Type: double
    def stat_kine_file_H(self):

        # Generate file name for stationary kinematics file
        file_name_kine = "DAS_static_kinematics_GH_y_" + str(round(self.GH_y*180/np.pi,1)) + "_GH_z_" + str(round(self.GH_z*180/np.pi,1)) + "_EL_x_" + str(round(self.EL_x*180/np.pi,1))

        # Get template file for stationaty kinematics file
        template = open(self.setup_path + r"\templates\Initial_cond_template_DAS_ID.sto",'r')
        text_kine = template.readlines()
        template.close()

        # Generate timetrace
        time = np.arange(0,3.01,0.01)


        # Generate new header for stationary kinematics file
        text_kine[0] = file_name_kine + ".mot\t\t\t\t\t\t\t\t\t\n"
        text_kine[2] = 'nRows=' + str(len(time)) + '\t\t\t\t\t\t\t\t\t\n'
        text_kine[3] = 'nColumns=' + str(12) + '\t\t\t\t\t\t\t\t\t\n'
        
   
        # Write new header to the stationary kinematics directory
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot',"w")
        file.writelines(text_kine)
        file.close()



        # Append the rows of stationary kinematics data to this new file
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot', "a")
        for i in range(len(time)):
            trace = str(time[i]) + "\t" + str(-33.486/180*np.pi) + str(5.002/180*np.pi) + str(32.914/180*np.pi) + str(45.571/180*np.pi) + str(0.458/180*np.pi) + str(-12.062/180*np.pi) + str(self.GH_y/180*np.pi) + str(self.GH_z/180*np.pi) + "\t" + str(self.GH_yy/180*np.pi) + "\t" + str(self.EL_x/180*np.pi) + "\t" + str(5/180*np.pi) + "\n"
            file.write(trace)
        file.close()
