from graph import Graph
import basic_graph
import matplotlib.pyplot as plt
from production.production_9 import P9
from production.production_16 import P16

def test_16_9():

    graph = basic_graph.basic_pentagon()
    graph.display()
    plt.show()
    P16()(graph)
    P9()(graph)

