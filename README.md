# Cap-and-Trade-Simulation
Drew H. Meseck
Economics Capstone Fall 2020

# To Run this Model:
1) Clone or download this repository

2) Install the requirements from the requirements.txt folder either onto your machine or in a virtual environment contained within the main project directory.

3) Navigate to the main directory, (ensuring your virtual environment is active if you used one)

4) type "mesa runserver" into the command line in the project folder, this will call the run.py script which launches the specified server GUI from the server.py folder. A new browser window should open on a locally hosted port.

5) Drag input sliders to desired values, and select the auction status, and select "Start" this should run the model!

# Note about Experiments:

If you would like to run the experiments, the batchrunner used is the MASTER version of BatchRunnerMP rather than the STABLE version. This file is the batchrunner.py file that exists here: https://github.com/projectmesa/mesa/blob/master/mesa/batchrunner.py
so if need be replace the version of the batchrunner you have with this file as it is not the one that comes with the pip install of mesa.

This is necessary as the multiprocessing is very useful for running the experiments in a reasonable time! All experiments are contained within the jupyter notebook Experiments.ipynb.


