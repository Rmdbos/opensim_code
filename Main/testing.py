# Import needed to get the right files to use opensim
import os
os.add_dll_directory("C:/OpenSim 4.5/bin")

# Point python where to find the source code for the class 

import sys
sys.path.insert(0, "Functions")


# Import opensim and other used libraries
import opensim as osim
import numpy as np
from sklearn.linear_model import LinearRegression
import Generate_force_files as fs
import Generate_stationary_kinematics_MOBL as sk
import sta_op_tendon_comp as so
import Static_op_moments as st
import stiffness_MoBL_ARMS_copy2 as ma
np.set_printoptions(threshold=sys.maxsize)

model = osim.Model(r"Main\Set-up\test\test_simple_dependent.osim")
# model = osim.Model(r"Main\Set-up\Moblarms\MOBL_ARMS.osim")

s = model.initSystem()
ground = model.getGround()

# sto = osim.Storage(r"Main\Set-up\test\Stationary_kinematics\test_static_kinematics_ID_angle_0.mot")
# tool = osim.ForwardTool()

# tool.createExternalLoads(r"Main\Set-up\test\Forward_dynamics\model_forces.xml",model)

# externalloads = tool.getExternalLoads()

# externalloads.transformPointsExpressedInGroundToAppliedBodies(sto,0,1)



joint = model.getJointSet().get("pin2")
body = model.getBodySet().get("arm2")

# for joint in model.getJointSet():
#     print(joint)
# joint = model.getJointSet().get("elbow")
# print(joint)
# print(osim.CustomJoint())

# print(model)
# print(dir(model.getMultibodySystem()))


# joint = model.getJointSet().get("wrist_hand")
# body = model.getBodySet().get("hand")

# print(s.getZ())
# print(s.getY())
# print(s.getQ())
# print(s.getU())


print(joint.getChildFrame().getRotationInGround(s).get(1))

# position1 = joint.getChildFrame().getPositionInGround(s)
# position2 = joint.getParentFrame().getPositionInGround(s)
# position3 = body.getPositionInGround(s)
# position4 = body.getMassCenter()
# position5 = body.findStationLocationInAnotherFrame(s,position4,ground)
# print(position1)
# print(position2)
# print(position3)
# print(position4)
# print(position5)

