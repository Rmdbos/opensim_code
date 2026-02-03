# Class for taking the states file from the CMC and turning it into an initial position file for the forward simulation



class generate_init_cond:
    # setup_path: path to the relevant setup directory. Type: string
    # CMC_results_path: path to the state file outputed by the CMC class. Type: string
    # file_name: name to give to the file that is generated. Type: string
    def __init__(self, setup_path, CMC_results_path, file_name):
        self.setup_path = setup_path
        self.CMC_results_path = CMC_results_path
        self.file_name = file_name
                


    def generate_init_cond(self):
        # Generate file name for the initial condition file
        file_name_init = self.file_name


        # Open and store CMC results file
        template = open(self.CMC_results_path,'r')
        text_init = template.readlines()
        template.close()

        # Generate new header for initial condition file
        text_init[0] = file_name_init + ".sto\t\t\t\t\t\t\t\t\t\n"
        text_init[2] = 'nRows=' + str(1) + '\t\t\t\t\t\t\t\t\t\n'
        
        # Write the header and the first line of the states to the initial condition file
        file = open(self.setup_path + r"\initial_position"'\\' + str(file_name_init) + '.sto',"w")
        for i in range(8):
            file.writelines(text_init[i])
        file.close()