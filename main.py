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
   model = Environment(10)
   model.step()



if __name__ == '__main__':
    main()