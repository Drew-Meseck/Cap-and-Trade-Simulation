from Company import Company
from Allowance import Allowance
import random
from numpy.random import normal
import math

class Environment():

    def __init__(self, N, am, tl, stH, siH, mSize, pen):
        self.schedule = []
        self.num_agents = N
        self.auction = am
        self.tech_level = tl
        self.strat_h = stH
        self.size_h = siH
        self.strat_profs = {}
        self.mean_size = mSize
        self.lobby_threshold = .33
        self.num_allow = 100 # use a function of total initial emissions, cap by initial cap proportion, generate allowances.
        self.decN = 3
        self.price = 10
        self.max_allow = self.num_allow
        self.penalty = pen
        self.period = 1

        for i in range(self.num_agents):
            a = Company(i, self, self.strat(), self.tech(), self.market_cap())
            self.schedule.append(a)

    #Deterministic for Company Stochasticity
    def strat(self):
        return ["Auc_Strat", "Market_Strat", "Invest_Strat"]

    def tech(self):
        return random.randint(1, 4)

    def market_cap(self):
        return normal(self.mean_size, 1- self.size_h, size= None)
    
    def produce_emit(self):
        en = []
        for i in self.schedule:
            en.append(i.produce())
        return sum(en)

    def invest_step(self):
        for i in self.schedule:
            i.invest()

    def getlobbying(self):
        l = []
        for i in self.schedule:
            l.append(i.current_invest[0])
        return l

    def decrement_allowances(self): #Change this to reflect the scaled value for lobbying
        l = self.getlobbying()
        if len(l) >= self.lobby_threshold:
            lobTotal = sum(l) * (1 / self.num_agents - len(l)) #Dont forget to figure out how to scale this so that this value goes between 0 and self.decN
            dectempN = self.decN - lobTotal
            return 0 if dectempN < 0 else self.num_allow - dectempN
        else:
            return self.num_allow - self.decN

    def distribute_step(self):
        if self.auction:
            #This is where the auction each step takes place:
            #Generate Allowances:
            alls = []
            for i in range(self.num_allow):
                alls.append(Allowance(i, owner = None))
            #--------------------
            #Auction each allowance
            for allowance in alls:
                bidow = []
                for comp in self.schedule:
                    bidow.append(comp.submit_bid())
                owns, bids = zip(*bidow)
                win = max(bids)
                index = bids.index(win)
                owns[index].allowances_t.append(allowance)
                allowance.owner = owns[index]
            #------------------------------------------------
        else:
            pass
    
    def trade_step(self):
        pass

    def setup(self):
        for i in self.schedule:
            i.step()
    
    def step(self):
        self.distribute_step()
        self.trade_step()
        self.produce_emit()
        self.invest_step()
        self.decrement_allowances()
        self.period += 1
        for i in self.schedule:
            i.step()
            print("My Technology Level is: " + str(i.tech_level))