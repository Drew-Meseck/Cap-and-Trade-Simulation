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
        self.period = 0

        #Reporters
        self.mean_tech_level = 0
        self.current_lobby = 0
        self.current_prod = 0
        self.t_1_lobby_mem = [0 for i in range(self.num_agents)]
        self.mean_cash_on_hand = 0
        self.emissions_t = 0


        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            {"mean_tech": "mean_tech_level", 
            "total_lobby": "current_lobby", 
            "n_allow": "num_allow",
            "mean_prod": "current_prod",
            "emissions": "emissions_t"}
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
        self.emissions_t = sum(en)

    def invest_step(self):
        for i in self.schedule.agents:
            i.invest()
            i.update_tech()
        self.getlobbying()

    def getlobbying(self):
        l = []
        for i in self.schedule.agents:
            l.append(i.current_lobby)
        self.t_1_lobby_mem = l

    def decrement_allowances(self): #Change this to reflect the scaled value for lobbying
        self.num_allow -= self.decN

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
                bid_high = (0, 0)
                for comp in self.schedule.agents:
                    o, bid = comp.submit_bid()
                    if bid > bid_high[1]:
                        bid_high = (o, bid)
                bid_high[0].cash_on_hand -= bid_high[1]
                allowance.owner = bid_high[0]
                bid_high[0].allowances_t.append(allowance)
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
        market = []
        for company in self.schedule.agents:
            company.more_trades = True
        trading = True
        count = 0
        while(trading and count < 10):
            m_len_i = len(market)
            for i in self.schedule.agents:
                if i.more_trades:
                    dec = i.get_buy_sell()
                    if dec: #They want to buy
                        target = i.valuate()
                        for a in market:
                            if a[1] <= target:
                                seller = a[0]
                                buyer = i
                                seller.cash_on_hand += a[1]
                                buyer.cash_on_hand -= a[1]
                                buyer.allowances_t.append(seller.allowances_t.pop())
                                break
                    else: #They want to sell
                        market.append(i.sell_allowance())
                #Update the trading status of the emitter
                i.update_trading()
            if len(market) == 0 or len(market):
                            trading = False
            
            agent_trades = [x.more_trades for x in self.schedule.agents]

            if not any(agent_trades):
                trading = False
            
            count += 1

                
    #REPORTERS=================================================================
    def update_reporters(self):
        #get mean tech level
        sum_tech = 0
        sum_prod = 0
        for i in self.schedule.agents:
            sum_tech += i.tech_level
            sum_prod += i.prod_t
        self.mean_tech_level = sum_tech / len(self.schedule.agents)
        self.current_prod = sum_prod / len(self.schedule.agents)
        self.current_lobby = sum(self.t_1_lobby_mem)


    def step(self):
        #DO INITIAL EMISSIONS TO DETERMINE ENVIRONMENT VARIABLES============================
        if self.period == 0:
            initial_emissions = []
            prod = []
            for i in self.schedule.agents:
                initial_emissions.append(i.produce_initial())
                prod.append(i.prod_t)
                i.setup()

            self.emissions_t = sum(initial_emissions)
            print("Total Production Prior to Cap: " + str(sum(prod)))
            print("Emissions Prior to Cap: " + str(self.emissions_t))
            self.num_allow = int((1 - self.initial_cap) * self.emissions_t)
            self.max_allow = self.num_allow
            print("Number of allowances under cap: " + str(self.num_allow))
            self.update_reporters()
            self.datacollector.collect(self)
            self.period += 1
            
        #====================================================================================

        #STEP================================================================================
        else:
            self.update_reporters()
            self.datacollector.collect(self)
            self.distribute_step()
            self.trade_step()
            self.produce_emit()
            self.invest_step()
            self.decrement_allowances()
            #for i in self.schedule.agents:
                #i.setup()
            self.update_reporters()
            self.datacollector.collect(self)
            self.period += 1
            if self.period == 50 + 1:
                self.running = False
        #====================================================================================