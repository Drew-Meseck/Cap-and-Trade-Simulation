from model import Environment


model = Environment(25, .4, True, .5, .33, 30)

for i in range(50):
    model.step()