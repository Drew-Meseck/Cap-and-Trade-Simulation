from mesa import Model
from mesa.time import RandomActivation
from Company import Company
import random
from numpy.random import normal

class Environment(Model):

    def __init__(self, N, am, tl, stH, siH, mSize):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        self.auction = am
        self.tech_level = tl
        self.strat_h = stH
        self.size_h = siH
        self.strat_profs = {}
        self.mean_size = mSize

        for i in range(self.num_agents):
            a = Company(i, self, strat(), tech(), market_cap)
            self.schedule.add(a)

    #Deterministic for Company Stochasticity
    def strat(self):
        return ["Auc_Strat", "Market_Strat", "Invest_Strat"]

    def tech(self):
        return normal(self.tech_level, .1, size= None)

    def market_cap(self):
        return normal(self.mean_size, 1 - self.size_h, size= None)
    
    def step(self):
        self.schedule.step()
