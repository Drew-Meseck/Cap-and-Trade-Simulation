#Distribution method experiment

import pandas as pd
import numpy as np
from multiprocessing import Pool
from model import Environment
from os import cpu_count
from CustomBR import DrewBatchRunner
    

def main():
    cores = cpu_count()

    #Experiment 1 Variables 
    fixed_params = {
    "N": 25,
    "cap_size": .35,
    "mSize":  .5,
    "lobby": .33,
    "dec": .005  
    }

    variable_params = {
        "am": [False, True]
    }


    experiment1 = BatchRunnerMP(Environment,
        nr_processes= None,
        variable_parameters = variable_params, 
        fixed_parameters = fixed_params,
        iterations = 5,
        max_steps = 200)
    
    experiment1.run_all()
    


if __name__ == "__main__":
    main()