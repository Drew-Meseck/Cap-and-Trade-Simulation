from mesa import Agent
import random
import math
from numpy.random import normal



class Company(Agent):
    #Attributes of a Company Agent

    def __init__(self, unique_id, model, strats, tl, size):
        super().__init__(unique_id, model)
        self.strat_set = strats
        self.capacity = 100 * size #weighted by constant integer value to make it meaningful in math
        self.tech_level = tl
        self.ti_mem = [0]
        self.cash_on_hand = 0
        self.current_invest = (0,0)
        self.ti_prop = .5
        self.allowances_t = []
        self.inv_t = 0
        self.pi_t = 0
        self.prod_t = 0
    
    #Actions a Company Can Take
    def setup(self):
        print("I am agent " + str(self.unique_id) +".")
        print(" I Have Technology Level: " + str(self.tech_level) + " And Size: " + str(self.capacity))
        print()

    
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
            thresh += mult * (sum(self.ti_mem[:4]) / 5 ) + (self.tech_level * (1/self.capacity))
            mult = normal(mult, .1, size= None)
            val += mult * self.ti_mem[index]
        if val >= thresh:
            self.tech_level += 1
        
    #Produce base on "Cobb-Douglass" approximation using size and ln(technology)
    def produce(self):
        A = math.log(self.tech_level)
        cap = self.capacity 
        prod = int(A * cap)
        if len(self.allowances_t) < prod:
            prod = len(self.allowances_t)
        self.pi_t = prod * self.model.price
        self.cash_on_hand += self.pi_t
        #Must use allowances in relation to production (all goods emit 1 ton / good)
        for a in range(prod):
            if len(self.allowances_t) == 0:
                break
            else:
                self.allowances_t.pop()
        self.prod_t = prod
        #Handle how much is emitted based on production (also affected by technology level)
        emit = prod * (1/ (random.uniform(.1, 2) * self.tech_level))
        return emit

    def produce_initial(self):
        prod = math.log(self.tech_level) * self.capacity
        self.prod_t = prod
        self.cash_on_hand += self.model.price * prod
        return prod * (1/ (random.uniform(.1, 2) * self.tech_level))


    #Invest using investment strategy 
    def invest(self):
        self.ti_prop, inv_prop_t = self.strat_get_ti_prop()
        self.inv_t = inv_prop_t * self.pi_t
        self.cash_on_hand -= self.inv_t 
        #return a tuple of (Tech_invest at t)
        invest_now = (self.ti_prop * self.inv_t, (1-self.ti_prop) * self.inv_t)
        self.ti_mem.insert(0, invest_now[0])
        self.current_invest =  invest_now
    
    #determines the amount invested of profit each period and the distribution of that investment
    def strat_get_ti_prop(self):
        return (.2, .5)


    def bid_decision(self):
        strat = self.strat_set[0] # get auction strategy profile
        if strat == "bidder":
            return True
        elif strat == "market":
            return False
        elif strat == "balanced":
            if len(self.allowances_t) < self.prod_t:
                return True
            else:
                return False
        return True

    #Chooses amount of bid. (0 is the bid if not submitted)
    def submit_bid(self):
        dec = self.bid_decision()
        bid = 0
        if dec:
            pass # this is where the strategy set determines the level of the bid
        return (self, bid)




class Allowance():
    #Attributes of an Allowance


    def __init__(self, id, o):
        self.uid = id
        self.owner = o

    #Functions inherent to the behavior of an allowance