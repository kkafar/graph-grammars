from graph import Graph
import basic_graph
import matplotlib.pyplot as plt
from production.production_10 import P10
from production.production_16 import P16

def test_10():

    graph = basic_graph.basic_pentagon()
    graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)

    graph.display()
    plt.show()

    P16()(graph)

    P10()(graph)

