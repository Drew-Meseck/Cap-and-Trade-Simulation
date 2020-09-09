from mesa import Model
from mesa.time import RandomActivation
from Company import Company

class Environment(Model):

    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)

        for i in range(self.num_agents):
            a = Company(i, self)
            self.schedule.add(a)

    def step(self):
        self.schedule.step()
