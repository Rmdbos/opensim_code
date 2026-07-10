import scipy.io
import numpy as np
import matplotlib.pyplot as plt



#constants




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
    

    for ax in go_axes:
        u = np.zeros((len(mattest[0][0][1][0][0][1][:,0]),6))
        fd = np.zeros((len(mattest[0][0][0][0][0][4][:,0]),6))
        # retrieve signals
        for rn in go_runs:
            if ax == 0: # Y
                # Y
                # u  = dat.DYN_ux_pix(end-n_points+1:end,:)*pixel2mm; 
                
                u[:,rn] = mattest[0][0][1][0][0][1][:,rn]
                
                fd[:,rn] = mattest[0][0][0][0][0][4][:,rn]
                
                
                # eval(['u(:,rn)  =  dat.leap.x(:,rn);'])
                # eval(['fd(:,rn) = -dat.ff.fdy(:,rn);'])
                nd = ndy
            elif ax == 1: # Z
                # Z
                
                u[:,rn] = mattest[0][0][1][0][0][2][:,rn]
                fd[:,rn] = mattest[0][0][0][0][0][5][:,rn]
                # eval(['u(:,rn)  =  dat.leap.y(:,rn);'])
                # eval(['fd(:,rn) =  dat.ff.fdz(:,rn);'])
                nd = ndz
                # u = dat.DYN_uy_pix(end-n_points+1:end,:)*pixel2mm; 
                # fd = dat.fdz(end-n_points+1:end,:);
            else:
                print('Should not be here (ax = 1 or 2)!')

    #     end # rn
        t = mattest[0][0][0][0][0][1][:,1]
                
        ###################################################################
        # plot time/spectrum data
        ###################################################################
    
        if PLT:
            plt.figure
            # plt.set(gcf, 'Position', [1, 1, 1855, 1003])
            # plot time signals for each run
            for rn in range(n_runs):
                plt.subplot(3, n_runs, rn+1)        
                plt.plot(t, fd[:,rn])
                # plt.hold
                plt.plot(t, u[:,rn])
                plt.xlim([t[1], t[-1]])
                plt.title(['Run #' +  str(rn)])
            
            # plt.legend('fd', 'u')
            plt.show()
 