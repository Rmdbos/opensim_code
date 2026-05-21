# Uses the force_setup_file class to generate a file containing time traces of the forces and a file with the setup for those forces



# Point python where to find the source code for the class 
import sys
sys.path.insert(0, "Functions")

# Import the class
import Generate_force_files as fs

# Generate unit vector detailing the direction of the force
direction = [1,0,0]

# Call class using the direction, a magnitude for the force, a name for the force file, where the setup files are located, the body we are interested in, and the name of the model
forcefile = fs.force_setup_file(direction, 0.04175847, "test", r"Main\Set-up\test", "arm", "model")

# Generate the force file in .mot format
forcefile.generate_force_file()

# Generate the xml setup file
forcefile.generate_force_setup()


