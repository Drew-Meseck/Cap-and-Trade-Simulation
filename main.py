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
   num_agents = 100
   auction_alloc = True
   mean_tech_level = .5
   strat_homogeneity = .5
   size_homogeneity = .5
   mean_size = .5

   model = Environment(num_agents, auction_alloc, mean_tech_level, strat_homogeneity, size_homogeneity, mean_size)
   model.step()



if __name__ == '__main__':
    main()