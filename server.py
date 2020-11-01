from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Environment

model_params = {
    "N": UserSettableParameter("slider", "Number of Agents", 100, 10, 200, 10),
    "cap_size": UserSettableParameter("slider", "Initial Cap Size (%) ", .4, .01, .99, .01),
    "am": UserSettableParameter("checkbox", "Auction Distribution?", True),
    "mSize": UserSettableParameter("slider", "Mean Size Level", .5, .1, 1, .1),
    "mTech": UserSettableParameter("slider", "Mean Technology Level", 3, 1, 10, 1),
    "dec": UserSettableParameter("slider", "Allowance Decrement Per Period", 5, 1, 10, 1)
}

server = ModularServer(
    Environment, [], "Cap and Trade", model_params
)
