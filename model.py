from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agents import Company, Allowance
import random
from numpy.random import normal
import math

class Environment(Model):
    #Constructor for the Environment model class
    def __init__(self, N, cap_size, am, mSize, lobby, dec):
        #The number of agents
        self.num_agents = N
        #Boolean to determine distribution method
        self.auction = am
        #Average size of the agents
        self.mean_size = mSize
        #The level of cooperation needed for lobbying to be effective
        self.lobby_threshold = lobby
        #number of allowances, determined by the initial cap size
        self.num_allow = 0
        #The initial number of allowance
        self.max_allow = 0
        #The decrement level expressed as a percentage of total allowances
        self.decN = dec
        #the price of goods in the market
        self.price = 10
        #the initial cap size expressed as a percentage of initial emissions
        self.initial_cap = cap_size
        #the time step of the model
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
            "emissions": "emissions_t",
            "mean_cash": "mean_cash_on_hand"}
        )

        #SETUP CODE===================================================================
        #This loop creates all of the agents in the model
        for i in range(self.num_agents):
            a = Company(i, self, self.tech(), self.market_cap())
            self.schedule.add(a)

        #Sets the status of the model
        self.running = True
        #=============================================================================

    
    #Deterimes Starting Technology levels for agents
    def tech(self):
        return random.choice([1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 6, 7, 8, 9, 10])
    #Returns a random triangular distribution (for integers) for initial technology levels
    def market_cap(self):
        return random.triangular(0, 1, self.mean_size)
    
    #Tells all the agents to produce and emit for the step
    def produce_emit(self):
        en = []
        for i in self.schedule.agents:
            en.append(i.produce())
        self.emissions_t = sum(en)
    #Tells all the agents to perform their period investment
    def invest_step(self):
        for i in self.schedule.agents:
            i.invest()
            i.update_tech()
        self.getlobbying()

    #Sets the lobbying memory from last step to inform behavior in the next step
    def getlobbying(self):
        l = []
        for i in self.schedule.agents:
            l.append(i.current_lobby)
        self.t_1_lobby_mem = l

    #Decrements the allowances based on the lobbying for the current period.
    def decrement_allowances(self): #Change this to reflect the scaled value for lobbying
        lt = len(self.t_1_lobby_mem) * self.lobby_threshold
        lob = [i for i in self.t_1_lobby_mem if i != 0]
        dec = int(self.decN * self.num_allow)
        if len(lob) >= lt:
            #If the lobbying threshold is met, create the decrement ratio and scale the decrement percentage accordingly
            modifier = sum(lob) / sum(self.t_1_lobby_mem) * random.uniform(.1, 1.5) #Random effectiveness of lobbying
            dec = dec * modifier if dec * modifier <= dec else dec
        else:
            dec = 0
        
        self.num_allow -= dec

    #Distributes the alowances based on the distribution method
    def distribute_step(self):
        if self.auction:
            #This is where the auction each step takes place:
            #Generate new Allowances:
            alls = []
            for i in range(int(self.num_allow)):
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
                #create a ratio based on the production level of this firm relative to the whole market
                ratio = prod[c] / total_prod
                #allocate allowances based on their production level
                na = int(ratio * self.num_allow)
                for a in range(na):
                    self.schedule.agents[c].allowances_t.append(Allowance(a, self.schedule.agents[c]))
                total_all += na
            
            remain = int(self.num_allow - total_all)
            #print("Remaining " + str(remain))
            for a in range(remain):
                x = random.choice(self.schedule.agents)
                x.allowances_t.append(Allowance(879, x))
            remain -= remain
            
            
            #Some Testing Output used in previous versions

            #print("DISTRIBUTE STEP:")
            #print(str(total_all) + ' ' + str(self.num_allow))
            #print("Remaining: " + str(remain))
            #for i in self.schedule.agents:
               #print(len(i.allowances_t))

    #Defines the framework with which trading takes place
    def trade_step(self):
        market = []
        for company in self.schedule.agents:
            company.more_trades = True
        trading = True
        count = 0
        #If there are more trades, or the trading period has more time left, continue trading
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
                                market.remove(a)
                                break
                    elif not dec: #They want to sell
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
        sum_cash = 0
        for i in self.schedule.agents:
            sum_tech += i.tech_level
            sum_prod += i.prod_t
            sum_cash += i.cash_on_hand
        self.mean_tech_level = sum_tech / len(self.schedule.agents)
        self.current_prod = sum_prod / len(self.schedule.agents)
        self.mean_cash_on_hand = sum_cash / len(self.schedule.agents)
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
            self.max_allow = int(self.num_allow)
            print("Number of allowances under cap: " + str(self.num_allow))
            self.update_reporters()
            self.datacollector.collect(self)
            self.period += 1
            
        #====================================================================================

        #STEP================================================================================
        else:
            #Distribute allowances
            self.distribute_step()
            #Trade allowances
            self.trade_step()
            #Produce goods and emit pollutants (Carbon)
            self.produce_emit()
            #Invest in technological advancement and lobbying
            self.invest_step()
            #Decrement the number of allowances for next step
            self.decrement_allowances()
            #Collect Data-----------------------------------
            self.update_reporters()
            self.datacollector.collect(self)
            #-----------------------------------------------
            self.period += 1
            if self.period == 500 + 1 or self.num_allow <= 10:
                self.running = False
        #====================================================================================