# Uses a class to generate an initial conditions file

# Tell python where to find the Functions
import sys
sys.path.insert(0, "Functions")

# Import used class
import Generate_initial_conditions as ic

# Initiate object with all necessary information
initcond_file = ic.generate_init_cond(r"Main\Set-up\Moblarms", r"Main\Set-up\Moblarms\Right_states.sto", "test")


# Generate the initial condition file
initcond_file.generate_init_cond()