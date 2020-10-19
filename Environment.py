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
        self.lobby_threshold = .33
        self.num_allow = 100
        self.decN = 3
        self.price = 10

        for i in range(self.num_agents):
            a = Company(i, self, self.strat(), self.tech(), self.market_cap)
            self.schedule.add(a)

    #Deterministic for Company Stochasticity
    def strat(self):
        return ["Auc_Strat", "Market_Strat", "Invest_Strat"]

    def tech(self):
        return normal(self.tech_level, .1, size= None)

    def market_cap(self):
        return normal(self.mean_size, 1 - self.size_h, size= None)
    
    def emit(self):
        en = []
        for i in self.schedule:
            en.append[i.produceE()]
        return sum(en)

    def getlobbying(self):
        l = []
        for i in self.schedule:
            l.append[i.lobby()]
        return l

    def decrement_allowances(self):
        l = self.getlobbying()
        if len(l) >= self.lobby_threshold:
            lobTotal = sum(l)(1 / self.num_agents - len(l)) #Dont forget to figure out how to scale this so that this value goes between 0 and self.decN
            dectempN = self.decN - lobTotal
            return 0 if dectempN < 0 else self.num_allow - dectempN
        else:
            return self.num_allow - self.decN
    
    def step(self):
        self.schedule.step()
