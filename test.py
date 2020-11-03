from model import Environment


model = Environment(25, .4, True, .5, 3, 5)

for i in range(50):
    model.step()