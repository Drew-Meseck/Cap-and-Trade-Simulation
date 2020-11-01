from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import Company, Allowance
import random
from numpy.random import normal
import math

class Environment(Model):
    
    def __init__(self, N, cap_size, am, mSize, mTech, dec):
        self.num_agents = N
        self.auction = am
        self.mean_size = mSize
        self.lobby_threshold = .33
        self.num_allow = 0
        self.max_allow = 0
        self.decN = dec
        self.price = 10
        self.mean_tech_level = 0
        self.initial_cap = cap_size
        self.mean_tech_level = 0
        self.period = 0
        self.current_lobby = 0

        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            {"mean_tech": "mean_tech_level", 
            "total_lobby": "current_lobby", 
            "n_allow": "num_allow"}
        )

        #SETUP CODE===================================================================
        for i in range(self.num_agents):
            a = Company(i, self, self.strat(), self.tech(), self.market_cap())
            self.schedule.add(a)


        self.running = True
        #===========================================================================

    def strat(self):
        return ["Auc_Strat", "Market_Strat", "Invest_Strat"]

    def tech(self):
        return random.randint(1, 4)

    def market_cap(self):
        return random.triangular(0, 1, self.mean_size)
    
    def produce_emit(self):
        en = []
        for i in self.schedule.agents:
            en.append(i.produce())
        return sum(en)

    def invest_step(self):
        for i in self.schedule.agents:
            i.invest()
            i.update_tech()

    def getlobbying(self):
        l = []
        for i in self.schedule.agents:
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
                alls.append(Allowance(i, o = None))
            #--------------------
            #Auction each allowance
            for allowance in alls:
                bidow = []
                for comp in self.schedule.agents:
                    bidow.append(comp.submit_bid())
                owns, bids = zip(*bidow)
                win = max(bids)
                index = bids.index(win)
                owns[index].allowances_t.append(allowance)
                allowance.owner = owns[index]
            #------------------------------------------------
        #Output based allocation
        else:
            prod = []
            total_all = 0
            for c in self.schedule.agents:
                prod.append(c.prod_t)
            total_prod = sum(prod)
            for c in range(len(self.schedule.agents)):
                ratio = prod[c] / total_prod
                na = int(ratio * self.num_allow)
                for a in range(na):
                    self.schedule.agents[c].allowances_t.append(Allowance(a, self.schedule.agents[c]))
                total_all += na
            
            remain = self.num_allow - total_all
            print("Remaining " + str(remain))
            for a in range(remain):
                x = random.choice(self.schedule.agents)
                x.allowances_t.append(Allowance(879, x))
            remain -= remain

            print("DISTRIBUTE STEP:")
            print(str(total_all) + ' ' + str(self.num_allow))
            print("Remaining: " + str(remain))
            for i in self.schedule.agents:
                print(len(i.allowances_t))


    def trade_step(self):
        pass

    #REPORTERS=================================================================
    def update_reporters(self):
        #get mean tech level
        sum_tech = 0
        for i in self.schedule.agents:
            sum_tech += i.tech_level
        self.mean_tech_level = sum_tech / len(self.schedule.agents)

        self.current_lobby = sum(self.getlobbying())        

    def step(self):
        #DO INITIAL EMISSIONS TO DETERMINE ENVIRONMENT VARIABLES============================
        if self.period == 0:
            initial_emissions = []
            prod = []
            for i in self.schedule.agents:
                initial_emissions.append(i.produce_initial())
                prod.append(i.prod_t)
                i.setup()

            emissions = sum(initial_emissions)
            print("Total Production Prior to Cap: " + str(sum(prod)))
            print("Emissions Prior to Cap: " + str(emissions))
            self.num_allow = int((1 - self.initial_cap) * emissions)
            self.max_allow = self.num_allow
            print("Number of allowances under cap: " + str(self.num_allow))
        #====================================================================================

        #STEP================================================================================
        
        self.distribute_step()
        #self.trade_step()
        self.produce_emit()
        self.invest_step()
        self.decrement_allowances()
        #for i in self.schedule.agents:
            #i.setup()
        self.update_reporters()
        self.datacollector.collect(self)
        self.period += 1
        if self.period == 50:
            self.running = False
        #====================================================================================