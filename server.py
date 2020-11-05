from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Environment

tech_chart = ChartModule([{"Label": "mean_tech", "Color": "Black"}])
prod_chart = ChartModule([{"Label": "mean_prod", "Color": "Blue"}])
emit_chart = ChartModule([{"Label": "emissions", "Color" : "Red"}])
cash_chart = ChartModule([{"Label": "n_allow", "Color": "Green"}])

model_params = {
    "N": UserSettableParameter("slider", "Number of Agents", 100, 10, 200, 10),
    "cap_size": UserSettableParameter("slider", "Initial Cap Size (%) ", .4, .01, .99, .01),
    "am": UserSettableParameter("checkbox", "Auction Distribution?", False),
    "mSize": UserSettableParameter("slider", "Mean Size Level", .5, .1, 1, .1),
    "mTech": UserSettableParameter("slider", "Mean Technology Level", 3, 1, 10, 1),
    "dec": UserSettableParameter("slider", "Allowance Decrement Percentage Per Period", .05, .001, .1, .001)
}

server = ModularServer(
    Environment, [tech_chart, prod_chart, emit_chart, cash_chart], "Cap and Trade", model_params
)
