# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Point python where to find the source code for the class 

import sys
sys.path.insert(0, "Functions")


# Import opensim and other used libraries
import opensim as osim
import numpy as np
import scipy.io
import matplotlib.pyplot as plt



data_path = 'Main/ExpData/'

 
###########################################################################
# define measurement time etc.
###########################################################################

# define time step
dt = 0.01

# define measurement time
t_meas = 40.96

# define total time
t_tot = 51.0

# define number of points in measurement time
n_points = t_meas/dt

# define number of points in total time
# n_data =  t_tot/dt+1;

# frequency primes
ndz  = [ 5, 11, 17, 23, 37, 59, 89, 131, 197, 293, 449, 673, 1009]
ndy  = [ 7, 13, 19, 29, 41, 61, 83, 127, 199, 307, 443, 677, 1013]
nn  = np.arange(n_points/2)


###########################################################################
# define conditions
########################################################################### 

# The first six runs are for ACFT, next SHIP, next CAR. -/+ alternate
# original condition names used by Daan
str_conds = {'ACFT', 'SHIP', 'CAR'}
         
# number of conditions               
n_conds = len(str_conds)

# participants
n_subjects = 39

# run numbers for each condition
n_runs = 6

# define the two screen directions we're interested in
str_axes = {'Y', 'Z'}
n_axes = len(str_axes)
             
###########################################################################
# logfile variables
########################################################################### 

# /ff -> FofuChannel
# /touch -> TouchChannel
# /mtouch -> MT_Interface_TouchEvent
# /leap -> LeapChannel
# /keypad -> KeypadTaskChannel
# /eci   -> ECIChannel
# /mcpva -> MotionCommandedPosVelAcc
# /imu   -> SimulatorCabMotionSensed

str_hdf5_fields = {'ff', 'leap', 'imu', 'touch', 'mcpva'}
n_hdf5_fields   = len(str_hdf5_fields)




###########################################################################
# define flags
###########################################################################

go_subjs = [1]#n_subjects;
go_runs  = np.arange(n_runs)
go_axes  = np.arange(n_axes)
cond     = 1 # 1 = ACFT, 2 = SHIP, 3 = CAR


SAV = 0
PLT = 1

###########################################################################
# START MAIN LOOP
###########################################################################

for subj in go_subjs:
    
    #######################################################################
    # load data (IDENTIFICATION)
    #######################################################################
    
    # load data
    mat = scipy.io.loadmat( data_path   + 'data_touchbdftdaan_subj' +  str(subj) +  '.mat') 
    
    
    # load data object
    mattest = mat["ACFT"]

    fdy = np.zeros((len(mattest[0][0][0][0][0][4][:,0]),1))
    fdz = np.zeros((len(mattest[0][0][0][0][0][5][:,0]),1))

    fdy = mattest[0][0][0][0][0][4][:,0]
    fdz = mattest[0][0][0][0][0][5][:,0]
    



thing = np.zeros((len(mattest[0][0][0][0][0][4][:,0])))



accvec = np.stack((thing,fdy,fdz))



model = osim.Model(r"Main\Set-up\Moblarms\MOBL_ARMS.osim")

state = model.initSystem()


mass_upp = model.get_BodySet().get("humerus").getMass()
mass_ulna = model.get_BodySet().get("ulna").getMass()
mass_radius = model.get_BodySet().get("radius").getMass()
mass_low = mass_ulna + mass_radius
mass_hand = model.get_BodySet().get("hand").getMass() 

force_upp = accvec*mass_upp
force_low = accvec*mass_low
force_hand = accvec*mass_hand


pos_shoulder = model.get_BodySet().get("humerus").getPositionInGround(state)

center_upp = model.get_BodySet().get("humerus").getMassCenter()
frame_upp = model.get_BodySet().get("humerus").findBaseFrame()
pos_upp = frame_upp.findStationLocationInGround(state,center_upp)

center_ulna = model.get_BodySet().get("ulna").getMassCenter()
center_radius = model.get_BodySet().get("radius").getMassCenter()
frame_ulna = model.get_BodySet().get("ulna").findBaseFrame()
frame_radius = model.get_BodySet().get("radius").findBaseFrame()
pos_ulna = frame_ulna.findStationLocationInGround(state,center_ulna)
pos_radius = frame_radius.findStationLocationInGround(state,center_radius)

pos_low = (pos_ulna.to_numpy()*mass_ulna+pos_radius.to_numpy()*mass_radius)/mass_low

center_hand = model.get_BodySet().get("hand").getMassCenter()
frame_hand = model.get_BodySet().get("hand").findBaseFrame()
pos_hand = frame_hand.findStationLocationInGround(state,center_hand)

posrel_upp = pos_upp.to_numpy() - pos_shoulder.to_numpy()
posrel_low = pos_low - pos_shoulder.to_numpy()
posrel_hand = pos_hand.to_numpy() - pos_shoulder.to_numpy()

moment_upp = np.cross(posrel_upp,force_upp,axisb=0)
moment_low = np.cross(posrel_low,force_low,axisb=0)

print(moment_low)
print(moment_upp)
print(force_hand)