from mesa import Agent
import random
import math
from numpy.random import normal



class Company(Agent):
    #Attributes of a Company Agent

    def __init__(self, unique_id, model, strats, tl, size):
        super().__init__(unique_id, model)
        self.strat_set = strats
        self.s = size
        self.capacity = 100 * size #weighted by constant integer value to make it meaningful in math
        self.tech_level = tl
        self.ti_mem = [0]
        self.cash_on_hand = 0
        self.current_lobby = 0
        self.ti_prop = .5
        self.allowances_t = []
        self.inv_t = 0
        self.pi_t = 0
        self.prod_t = 0
        self.more_trades = True
    
    #Actions a Company Can Take
    def setup(self):
        print("I am agent " + str(self.unique_id) +".")
        print(" I Have Technology Level: " + str(self.tech_level) + " And Size: " + str(self.capacity))
        print()
    
    def step(self):
        pass

    
    def update_tech(self): #perhaps tech is in descrete integer levels and advance if past investment meets some threshold (not all past investment is kept!)
        val = 0
        thresh = 0
        for index, value in enumerate(self.ti_mem):
            mult = 0
            #peacewise function that describes inflection curve, peaking at period 2, effect ending at period 5
            if index <= 2:
                mult =  math.sqrt(index/2)
            else:
                mult = -1 * (math.sqrt(index - 1) + 2)
                if mult < 0:
                    mult = 0
            #threshold value is greater than the average produced tech level, increased by the tech level but reduced by capacity (size of company)
            thresh += mult * (sum(self.ti_mem[:4]) / 5 ) + ((2 ** self.tech_level) * (1/self.capacity))
            mult = normal(mult, .1, size= None)
            val += mult * self.ti_mem[index]
        if val >= thresh:
            self.tech_level += 1
        
    #Produce base on "Cobb-Douglass" approximation using size and ln(technology)
    def produce(self):
        A = math.log(self.tech_level + 1)
        cap = self.capacity
        prod = int(A * cap)
        r = random.uniform(.1, 2)
        emit = int(prod / ( r * self.tech_level))
        alls = len(self.allowances_t)
        #Handle how much is emitted based on production (also affected by technology level)
        if len(self.allowances_t) < emit:
            prod = alls * (r * self.tech_level)
            emit = int(prod / (r * self.tech_level))
        self.pi_t = prod * self.model.price
        self.cash_on_hand += self.pi_t
        #Must use allowances in relation to production (all goods emit 1 ton / good)
        for a in range(emit):
            self.allowances_t.pop()
        self.prod_t = prod        
        return emit

    def produce_initial(self):
        prod = math.log(self.tech_level + 1) * self.capacity
        self.prod_t = prod
        self.cash_on_hand += self.model.price * prod
        return prod * (1/ (random.uniform(.1, 2) * self.tech_level))


    #Invest using investment strategy 
    def invest(self):
        lob, tech, inv = self.get_invest_props()
        i = self.pi_t * inv
        self.inv_t = i * tech
        self.ti_mem.insert(0, self.inv_t)
        self.current_lobby = i * lob
        self.cash_on_hand -= i
        
    
    #determines the amount invested of profit each period and the distribution of that investment
    def get_invest_props(self):

        expec_l = (1 - self.model.lobby_threshold) * (sum(self.model.t_1_lobby_mem) / len(self.model.schedule.agents))
        expec_t = sum(self.ti_mem) / len(self.ti_mem) * (self.model.lobby_threshold) + self.capacity

        total_expec = expec_l + expec_t
        prop_l = expec_l / total_expec
        prop_t = expec_t / total_expec

        prop_i = random.uniform(.1, .4) 

        #If the period is 0, size is the only information they have about the past, and how effective tech investment is.
        if self.model.period == 0:
            prop_t = self.s
            prop_l = 1 - prop_t
        return (prop_l, prop_t, prop_i)

    def valuate(self):
        #first estimate their total emissions for the current period
        est_prod = math.log(self.tech_level + 1) * self.capacity
        est_emit = est_prod / (random.uniform(.1, 2) * self.tech_level)
        #the estimated emissions is the needed total allowances to produce at max capacity
        #Now, they are constrained by their budget, so their valuation will be a ratio of these values
        return self.cash_on_hand / est_emit

    #Chooses amount of bid. (0 is the bid if not submitted or affordable)
    def submit_bid(self):
        #optimial bid in first price sealed bid auction is half of agent valuation.
        bid = self.valuate() / 2
        if self.cash_on_hand < bid:
            bid = 0 
        return (self, bid)

    def get_buy_sell(self):
        est_prod = math.log(self.tech_level + 1) * self.capacity
        est_emit = est_prod / (random.uniform(.1, 2) * self.tech_level)
        stat = len(self.allowances_t) == est_emit
        return True if stat else False


    def sell_allowance(self):
        est_prod = math.log(self.tech_level + 1) * self.capacity
        est_emit = est_prod / (random.uniform(.1, 2) * self.tech_level)
        diff = abs(len(self.allowances_t) - int(est_emit))
        price = self.cash_on_hand / est_emit
        return price * diff



    def update_trading(self):
        est_prod = math.log(self.tech_level + 1) * self.capacity
        est_emit = est_prod / (random.uniform(.1, 2) * self.tech_level)
        stat = len(self.allowances_t) == est_emit
        if stat:
            self.more_trades = False
        else:
            self.more_trades = True


            




class Allowance():
    #Attributes of an Allowance


    def __init__(self, id, o):
        self.uid = id
        self.owner = o

    #Functions inherent to the behavior of an allowance