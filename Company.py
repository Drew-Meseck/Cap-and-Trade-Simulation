from mesa import Agent
import random



class Company(Agent):
    #Attributes of a company

    def __init__(self, unique_id, model, strats, tl, size):
        super().__init__(unique_id, model)
        self.strat_set = strats
        self.capacity = size
        self.tech_level = tl
        self.ti_mem = []
        self.cash_on_hand = 0
        
        


    def step(self):
        print("I am agent " + str(self.unique_id) +".")

    
    def update_tech(self): #perhaps tech is in descrete integer levels and advance if past investment meets some threshold (not all past investment is kept!)
        pass

    def produce(self):
        pass

    def produceE(self):
        return self.produce * (1 / (random.randrange(.1, 3, .1) * self.tech_level - 3)) # has some random and asymptotic affect on emissions.

    def lobby(self):
        pass


    #Actions a Company Can Take