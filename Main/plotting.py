import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D axes

stiffness = np.array([[-126.08933555, -134.45104301,  -49.1347177 ],
 [ 150.69972603,  162.68795396,   51.78931061],
 [ 325.09657248,  -24.27045666, -409.70797147],
 [-121.75138932,   13.56399784,  153.50801851],
 [ -27.1909966,    98.26355253,  198.380993  ],
 [  21.1016238,   -91.75264082, -188.55229033],
 [ -22.34897312, -153.5791499,    84.46397589],
 [  26.73622417,  224.84702847, -123.61140814],
 [-146.83408953,  -63.01469588,   75.21897809],
 [ 360.64736324,  156.86608124, -196.27546002],
 [-186.12733854,  -20.80273578, -195.79131576],
 [ 165.57956968,   12.87548458,  173.09265243],
 [ 193.45745633,  101.29459022, -112.20408316],
 [-170.67735006,  -82.95238395,  100.56092811],
 [-115.59538058,  179.21591365,   79.67654717],
 [ 232.04262222, -377.29936235, -162.99943156],
 [  76.73266482,  -93.62433152, -254.96638402],
 [ -41.49272217,   53.24468677,  135.73935795],
 [  40.21836522,  163.68280615, -233.42447444],
 [ -33.3858396,  -122.55239591,  168.20923363],
 [-202.5967149,    -9.7753037,   -24.43574662],
 [ 386.27111768,   -6.13820345,   27.32161745],
 [ -92.35481126,    4.84816671,  117.33422839],
 [ 236.50986264,  -8.48931303, -308.80222743],
 [ -95.11875846,  269.62913528,   21.08166187],
 [  71.55645744, -195.87610863,  -23.89483753],
 [ 246.21482139, -374.93417186, -181.83113484],
 [-110.37702343,  182.25851469,   71.53128184],
 [-202.59670926,   -9.77530318,  -24.43574599],
 [ 386.27103837,   -6.13820205,   27.32160851]])


deflections = np.array([[-0.00480018, -0.00511851, -0.00187054],
 [ 0.00482543,  0.0052093,   0.0016583 ],
 [ 0.00386211, -0.00028833, -0.00486729],
 [-0.00385756,  0.00042976,  0.00486374],
 [-0.00088702,  0.00320553,  0.00647153],
 [ 0.00072854, -0.00316777, -0.00650979],
 [-0.00091066, -0.00625791,  0.00344167],
 [ 0.00074617,  0.00627517, -0.00344982],
 [-0.00527488, -0.00226375,  0.00270217],
 [ 0.00540412,  0.00235056, -0.00294109],
 [-0.00415197, -0.00046405, -0.00436755],
 [ 0.0042138,   0.00032767,  0.004405  ],
 [ 0.00539382,  0.00282421, -0.00312838],
 [-0.00546676, -0.00265695,  0.00322095],
 [-0.00323128,  0.00500969,  0.00222723],
 [ 0.00322645, -0.00524618, -0.00226643],
 [ 0.00199311, -0.00243187, -0.00662269],
 [-0.0020935,   0.00268644,  0.00684869],
 [ 0.00085167,  0.00346615, -0.004943  ],
 [-0.00101183, -0.0037142,   0.00509792],
 [-0.00713869, -0.00034444, -0.00086102],
 [ 0.00709378, -0.00011273,  0.00050175],
 [-0.00435892,  0.00022882,  0.00553788],
 [ 0.00444867, -0.00015968, -0.00580846],
 [-0.00215984,  0.00612241,  0.0004787 ],
 [ 0.00222673, -0.00609537, -0.00074357],
 [ 0.00326441, -0.00497101, -0.00241078],
 [-0.00319724,  0.0052794,   0.00207201],
 [-0.00713869, -0.00034444, -0.00086102],
 [ 0.00709378, -0.00011273,  0.00050175]])



fig = plt.figure()
ax = plt.axes(projection='3d')

ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)

ax.scatter(deflections[:,0], deflections[:,1], deflections[:,2])
ax.set_title('3D Scatter Plot')
plt.show()





fig = plt.figure()
ax = plt.axes(projection='3d')





ax.scatter(stiffness[:,0], stiffness[:,1], stiffness[:,2])
ax.set_title('3D Scatter Plot')


x_data = stiffness[:,0]
y_data = stiffness[:,1]
z_data = stiffness[:,2]

def ellipsoid(x, y, z, alpha, beta, gamma, a, b, c):
    Rx = np.array([[1, 0, 0],[0 , np.cos(alpha), -np.sin(alpha)],[0, np.sin(alpha), np.cos(alpha)]]) 
    Ry = np.array([[np.cos(beta), 0, np.sin(beta)],[0, 1, 0],[-np.sin(beta), 0, np.cos(beta)]])
    Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],[np.sin(gamma) , np.cos(gamma),0],[0, 0, 1]])
    xyz = np.array([x,y,z])
    xyz1 = np.matmul(Rz,np.matmul(Ry,np.matmul(Rx,xyz)))
    x1 = xyz1[0]
    y1 = xyz1[1]
    z1 = xyz1[2]
    f = (x1 / a) ** 2 + (y1 / b) ** 2 + (z1 / c) **2 - 1
    return f


def f_min(params, x, y, z):
    alpha, beta, gamma , a, b, c = params
    return np.sum(ellipsoid(x, y, z, alpha, beta, gamma, a, b, c)**2)


# Initial guess
p0 = [0, 0 , 0, 200, 500, 300]

# Optimize
res=scipy.optimize.minimize(f_min, p0, args=(x_data, y_data, z_data))

print(res)


a = res.x[3]
b = res.x[4]
c = res.x[5]  # Semi-axes (adjust these for different ellipsoids)
num_samples = 100  # Number of points per angle (θ and φ)



theta = np.linspace(0, np.pi, num_samples)  # Polar angle: 0 to π
phi = np.linspace(0, 2 * np.pi, num_samples)  # Azimuthal angle: 0 to 2π
 
# Create meshgrid: θ_grid[i,j] = θ[j], φ_grid[i,j] = φ[i]
theta_grid, phi_grid = np.meshgrid(theta, phi)


x = a * np.sin(theta_grid) * np.cos(phi_grid)
y = b * np.sin(theta_grid) * np.sin(phi_grid)
z = c * np.cos(theta_grid)


alpha = res.x[0]
beta = res.x[1]
gamma = res.x[2]

Rx = np.array([[1, 0, 0],[0 , np.cos(alpha), -np.sin(alpha)],[0, np.sin(alpha), np.cos(alpha)]]) 
Ry = np.array([[np.cos(beta), 0, np.sin(beta)],[0, 1, 0],[-np.sin(beta), 0, np.cos(beta)]])
Rz = np.array([[np.cos(gamma), -np.sin(gamma), 0],[np.sin(gamma) , np.cos(gamma),0],[0, 0, 1]])



x1 = x
y1 = y*np.cos(alpha)-z*np.sin(alpha)
z1 = y*np.sin(alpha)+z*np.cos(alpha)

x2 = x1*np.cos(beta) + z1*np.sin(beta)
y2 = y1
z2 = x1*-np.sin(beta)+z1*np.cos(beta)

x3 = x2*np.cos(gamma)-y2*np.sin(gamma)
y3 = x2*np.sin(gamma) + y2*np.cos(gamma)
z3 = z2

 
# Plot the ellipsoid surface
ellipsoid = ax.plot_wireframe(
    x3, y3, z3,
    cmap='viridis',  # Color map
    alpha=0.8,       # Transparency
    edgecolor='k',   # Edge color for wireframe
    linewidth=0.2    # Edge line width
)
 
# # Add labels and title
ax.set_xlabel('X-axis', fontsize=12)
ax.set_ylabel('Y-axis', fontsize=12)
ax.set_zlabel('Z-axis', fontsize=12)
ax.set_title(f'Ellipsoid with Semi-axes (a={a}, b={b}, c={c})', fontsize=14)
 
# Add color bar (optional)
cbar = fig.colorbar(ellipsoid, ax=ax, shrink=0.7, aspect=10)
cbar.set_label('Z-Value', rotation=270, labelpad=15)
 
# Adjust view angle for better visibility
ax.view_init(elev=30, azim=45)  # Elevation and azimuth angles
 
plt.tight_layout()
plt.show()

