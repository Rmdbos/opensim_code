# Uses a class to generate an initial conditions file

# Tell python where to find the Functions
import sys
sys.path.insert(0, "Functions")

# Import used class
import Generate_initial_conditions as ic

# Initiate object with all necessary information
initcond_file = ic.generate_init_cond(r"Main\Set-up\DAS3", r"Main\Set-up\DAS3\CMC\Results\DAS3_CMCed_states.sto", "testing_10_90")


# Generate the initial condition file
initcond_file.generate_init_cond()