from mesa import Agent




class Company(Agent):
    #Attributes of a company

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        print("I am agent " + str(self.unique_id) +".")
    

    #Actions a Company Can Take