import numpy as np


x = 1
y = 0
z = 0


alpha = np.deg2rad(45)
beta = np.deg2rad(45)
gamma = np.deg2rad(45)

Rx = np.array([[1, 0, 0],[0 , np.cos(alpha), -np.sin(alpha)],[0, np.sin(alpha), np.cos(alpha)]]) 
Ry = np.array([[np.cos(beta), 0, np.sin(beta)],[0, 1, 0],[-np.sin(beta), 0, np.cos(beta)]])
Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],[np.sin(gamma) , np.cos(gamma),0],[0, 0, 1]])
xyz = np.array([x,y,z])

xyz1 = np.matmul(Rz,np.matmul(Ry,np.matmul(Rx,xyz)))

print(xyz1)