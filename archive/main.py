#Tools used for the simulation and managing data
import numpy as np
import pandas as pd
import multiprocessing

#Tools Used for data analysis
import matplotlib.pyplot as plt

#Classes from this project
from Company import Company
from Allowance import Allowance
from Environment import Environment


def main():
   #Define default model parameters
   num_agents = 50
   auction_alloc = False
   mean_tech_level = 5
   strat_homogeneity = .5
   size_homogeneity = .5
   mean_size = .5
   i_cap_size = .2

   model = Environment(num_agents, i_cap_size, auction_alloc, strat_homogeneity, size_homogeneity, mean_size)
   model.setup()
   model.step()



if __name__ == '__main__':
    main()