from production.production_1 import P1
import basic_graph
import matplotlib.pyplot as plt
from production.production_9 import P9
from production.production_10 import P10
from production.production_16 import P16
from graph import Graph

def test_16():
    graph, _ = basic_graph.basic_star5()
    graph.display()
    plt.show()
    
    P16(5)(graph)
    graph.display()
    plt.show()

