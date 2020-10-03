from mesa import Agent




class Company(Agent):
    #Attributes of a company

    def __init__(self, unique_id, model, strats, tl, size):
        super().__init__(unique_id, model)
        self.strat_set = strats
        self.capacity = size
        self.tech_level = tl


    def step(self):
        print("I am agent " + str(self.unique_id) +".")
    

    #Actions a Company Can Take