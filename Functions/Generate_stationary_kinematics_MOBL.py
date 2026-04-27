# Class that transforms generic coordinate to ones used by DAS3 and writes the stationary kinematics file


# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")


# Import used libraries
import numpy as np
import opensim as osim

class stat_kine_file:
    # abd_angle: the abduction angle of the shoulder in degrees. Type: double or numpy array
    # sh_flex_angle: the flexion angle of the shoulder in degrees. Type: double or numpy array
    # el_flex_angle: the flexion angle of the elbow in degrees. type: double or numpy array
    # setup_path: path to the relevant setup directory for both generated files. Type: string
    def __init__(self, setup_path, abd_angle = 0, sh_flex_angle =0, el_flex_angle = 0, elv_angle = 0, shoulder_rot = 0, shoulder_elv = 0, elbow_flexion = 0):
        self.abd_angle = abd_angle
        self.sh_flex_angle = sh_flex_angle
        self.el_flex_angle = el_flex_angle
        self.elv_angle = elv_angle
        self.shoulder_rot = shoulder_rot
        self.shoulder_elv = shoulder_elv
        self.elbow_flexion = elbow_flexion
        self.setup_path = setup_path
        pass

    # Function takes three angles in degrees and returns the angles used by DAS3 in radians.
    # elv_angle and elv_angley are limited to between -pi/2 to pi/2 due to the way they are calculated
    # shoulder_elv is limited to between 0 and 84 degrees as that is the maximum input for the model
    # elbow_flexion is limited to between 0 and 130 degrees as that is the maximum input for the model
    def coordinate_transformation(self):

        # add 0.001 degree to both angles to avoid numbers going to infinity and so np.sign doesn't return 0
        if self.abd_angle == 0:
            self.abd_angle = self.abd_angle + 0.001
        if self.sh_flex_angle == 0:
            self.sh_flex_angle = self.sh_flex_angle + 0.001

        # Calculate elv_angle from the ratio betwen sh_flex_angle and abd_angle
        self.elv_angle = np.arctan(self.sh_flex_angle/self.abd_angle)
        # Rotate arm back into place with elv_angley
        self.shoulder_rot = 0
        # Get shoulder_elv using pythagoras and ensure signs are correct
        shoulder_elv = np.sqrt(np.square(self.abd_angle)+np.square(self.sh_flex_angle))*np.sign(self.abd_angle)*np.sign(self.sh_flex_angle)
        # Enforce limits for shoulder_elv and convert to radians
        shoulder_elv = np.where(shoulder_elv > 180, 180, shoulder_elv)
        shoulder_elv = np.where(shoulder_elv < 0, 0, shoulder_elv)
        self.shoulder_elv = shoulder_elv/180*np.pi
        # Enforce limits for elbow_flexion and convert to radians
        self.el_flex_angle = np.where(self.el_flex_angle > 130, 130, self.el_flex_angle)
        self.el_flex_angle = np.where(self.el_flex_angle < 0, 0, self.el_flex_angle)
        self.elbow_flexion = self.el_flex_angle/180*np.pi


    def find_related_coor(self):
        # Set related values using simmspline
        sternoclav_r2_con = osim.SimmSpline()
        sternoclav_r2_con.addPoint(0,0)
        sternoclav_r2_con.addPoint(2.61799,-0.633555)
        self.sternoclavi_r2 = sternoclav_r2_con.calcValue(osim.Vector(1,self.shoulder_elv))

        sternoclav_r3_con = osim.SimmSpline()
        sternoclav_r3_con.addPoint(0,0)
        sternoclav_r3_con.addPoint(3.14159,0.322013)
        self.sternoclavi_r3 = sternoclav_r3_con.calcValue(osim.Vector(1,self.shoulder_elv))

        unrotscap_r2_con = osim.SimmSpline()
        unrotscap_r2_con.addPoint(0,0)
        unrotscap_r2_con.addPoint(2.61799,0.633555)
        self.unrotscap_r2 = unrotscap_r2_con.calcValue(osim.Vector(1,self.shoulder_elv))

        unrotscap_r3_con = osim.SimmSpline()
        unrotscap_r3_con.addPoint(0,0)
        unrotscap_r3_con.addPoint(3.14159,-0.322013)
        self.unrotscap_r3 = unrotscap_r3_con.calcValue(osim.Vector(1,self.shoulder_elv))

        acrimonclav_r1_con = osim.SimmSpline()
        acrimonclav_r1_con.addPoint(0,0)
        acrimonclav_r1_con.addPoint(2.61799,0.466003)
        self.acrimonclav_r1 = acrimonclav_r1_con.calcValue(osim.Vector(1,self.shoulder_elv))

        acrimonclav_r2_con = osim.SimmSpline()
        acrimonclav_r2_con.addPoint(0,0)
        acrimonclav_r2_con.addPoint(2.61799,-0.128282)
        self.acrimonclav_r2 = acrimonclav_r2_con.calcValue(osim.Vector(1,self.shoulder_elv))

        acrimonclav_r3_con = osim.SimmSpline()
        acrimonclav_r3_con.addPoint(0,0)
        acrimonclav_r3_con.addPoint(2.61799,1.03673)
        self.acrimonclav_r3 = acrimonclav_r3_con.calcValue(osim.Vector(1,self.shoulder_elv))

        unrothum_r1_con = osim.SimmSpline()
        unrothum_r1_con.addPoint(0,0)
        unrothum_r1_con.addPoint(2.61799,-0.466003)
        self.unrothum_r1 = unrothum_r1_con.calcValue(osim.Vector(1,self.shoulder_elv))

        unrothum_r2_con = osim.SimmSpline()
        unrothum_r2_con.addPoint(0,0)
        unrothum_r2_con.addPoint(2.61799,0.128282)
        self.unrothum_r2 = unrothum_r2_con.calcValue(osim.Vector(1,self.shoulder_elv))

        unrothum_r3_con = osim.SimmSpline()
        unrothum_r3_con.addPoint(0,0)
        unrothum_r3_con.addPoint(2.61799,-1.03673)
        self.unrothum_r3 = unrothum_r3_con.calcValue(osim.Vector(1,self.shoulder_elv))

        shoulder1_r2_con = osim.SimmSpline()
        shoulder1_r2_con.addPoint(-1.5708,1.5708)
        shoulder1_r2_con.addPoint(3.14159,-3.14159)
        self.shoulder1_r2 = shoulder1_r2_con.calcValue(osim.Vector(1,self.elv_angle))

        wrist_hand_r1_con = osim.SimmSpline()
        wrist_hand_r1_con.addPoint(-0.174533,-0.261799)
        wrist_hand_r1_con.addPoint(0,0)
        wrist_hand_r1_con.addPoint(0.436332,0.436332)
        self.wrist_hand_r1 = wrist_hand_r1_con.calcValue(osim.Vector(1,0))

        wrist_hand_r3_con = osim.SimmSpline()
        wrist_hand_r3_con.addPoint(-1.22173,1.22173)
        wrist_hand_r3_con.addPoint(-0.610865,0.610865)
        self.wrist_hand_r3 = wrist_hand_r3_con.calcValue(osim.Vector(1,0))
        





    # Function that generates a stationary kinematics file for the DAS3 model
    # elv_angle angle used for Mobl_ARMS in radians. Type: double
    # shoulder_elv angle used for Mobl_ARMS in radians. Type: double
    # shoulder_rot angle used for Mobl_ARMS in radians. Type: double
    # elbow_flexion angle used for Mobl_ARMS in radians. Type: double
    def stat_kine_file(self):

        # Generate file name for stationary kinematics file
        file_name_kine = "Mobl_static_kinematics_elv_angle_" + str(round(self.elv_angle*180/np.pi,1)) + "_shoulder_elv_" + str(round(self.shoulder_elv*180/np.pi,1)) + "_elbow_flexion_" + str(round(self.elbow_flexion*180/np.pi,1))

        # Get template file for stationaty kinematics file
        template = open(self.setup_path + r"\templates\Initial_cond_template_MOBL.sto",'r')
        text_kine = template.readlines()
        template.close()

        # Generate timetrace
        time = np.arange(0,3.01,0.01)


        # Generate new header for stationary kinematics file
        text_kine[0] = file_name_kine + ".mot\t\t\t\t\t\t\t\t\t\n"
        text_kine[2] = 'nRows=' + str(len(time)) + '\t\t\t\t\t\t\t\t\t\n'
        text_kine[3] = 'nColumns=' + str(43) + '\t\t\t\t\t\t\t\t\t\n'
        
   
        # Write new header to the stationary kinematics directory
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot',"w")
        file.writelines(text_kine)
        file.close()

        # Append the rows of stationary kinematics data to this new file
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot', "a")
        for i in range(len(time)):
            trace = str(time[i]) + "\t" + str(10/180*np.pi) + "\t" + str(0) + "\t" + str(self.sternoclavi_r2) + "\t" + str(0) + "\t" + str(self.sternoclavi_r3) + "\t" + str(0) + "\t" + str(self.unrotscap_r3) + "\t" + str(0) + "\t" + str(self.unrotscap_r2) + "\t" + str(0) + "\t" + str(self.acrimonclav_r2) + "\t" + str(0) + "\t" + str(self.acrimonclav_r3) + "\t" + str(0) + "\t" + str(self.acrimonclav_r1) + "\t" + str(0) + "\t" + str(self.unrothum_r1) + "\t" + str(0) + "\t" + str(self.unrothum_r3) + "\t" + str(0) + "\t" + str(self.unrothum_r2) + "\t" + str(0) + "\t" + str(self.elv_angle) + "\t" + str(0) + "\t" + str(self.shoulder_elv) + "\t" + str(0) + "\t" + str(self.shoulder1_r2) + "\t" + str(0) + "\t" + str(self.shoulder_rot) + "\t" + str(0) + "\t" + str(self.elbow_flexion) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(0) + "\t" + str(self.wrist_hand_r1) + "\t" + str(0) + "\t" + str(self.wrist_hand_r3) + "\t" + str(0) + "\n"
            file.write(trace)
        file.close()


    # Function that generates a stationary kinematics file for the DAS3 model
    # elv_angle angle used for Mobl_ARMS in radians. Type: double
    # shoulder_elv angle used for Mobl_ARMS in radians. Type: double
    # shoulder_rot angle used for Mobl_ARMS in radians. Type: double
    # elbow_flexion angle used for Mobl_ARMS in radians. Type: double
    def stat_kine_file_H(self):

        # Generate file name for stationary kinematics file
        file_name_kine = "Mobl_static_kinematics_elv_angle_" + str(round(self.elv_angle*180/np.pi,1)) + "_shoulder_elv_" + str(round(self.shoulder_elv*180/np.pi,1)) + "_elbow_flexion_" + str(round(self.elbow_flexion*180/np.pi,1))

        # Get template file for stationaty kinematics file
        template = open(self.setup_path + r"\templates\Initial_cond_template_MOBL_ID.sto",'r')
        text_kine = template.readlines()
        template.close()

        # Generate timetrace
        time = np.arange(0,3.01,0.01)


        # Generate new header for stationary kinematics file
        text_kine[0] = file_name_kine + ".mot\t\t\t\t\t\t\t\t\t\n"
        text_kine[2] = 'nRows=' + str(len(time)) + '\t\t\t\t\t\t\t\t\t\n'
        text_kine[3] = 'nColumns=' + str(22) + '\t\t\t\t\t\t\t\t\t\n'
        
   
        # Write new header to the stationary kinematics directory
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot',"w")
        file.writelines(text_kine)
        file.close()



        # Append the rows of stationary kinematics data to this new file
        file = open(self.setup_path + r"\Stationary_kinematics"'\\' + str(file_name_kine) + '.mot', "a")
        for i in range(len(time)):
            trace = str(time[i]) + "\t" + str(10/180*np.pi)  + "\t" + str(self.sternoclavi_r2)  + "\t" + str(self.sternoclavi_r3)  + "\t" + str(self.unrotscap_r3)  + "\t" + str(self.unrotscap_r2)  + "\t" + str(self.acrimonclav_r2)  + "\t" + str(self.acrimonclav_r3)  + "\t" + str(self.acrimonclav_r1)  + "\t" + str(self.unrothum_r1)  + "\t" + str(self.unrothum_r3)  + "\t" + str(self.unrothum_r2)  + "\t" + str(self.elv_angle)  + "\t" + str(self.shoulder_elv)  + "\t" + str(self.shoulder1_r2)  + "\t" + str(self.shoulder_rot)  + "\t" + str(self.elbow_flexion)  + "\t" + str(0)  + "\t" + str(0)  + "\t" + str(0) + "\t"  + str(self.wrist_hand_r1)  + "\t" + str(self.wrist_hand_r3) + "\n"
            file.write(trace)
        file.close()
        return  str(file_name_kine) + '.mot'
        