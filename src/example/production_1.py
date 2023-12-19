from graph import Graph
import basic_graph
import matplotlib.pyplot as plt
from production.p1 import P1

def test_1():
    graph = Graph()
    graph = basic_graph.basic_square()

    graph.display()
    plt.show()

    P1()(graph)

#   graph.dump_node("test.adjlist")
