from graph import Graph
import basic_graph
import matplotlib.pyplot as plt
from production import P10, P16

def main():
    graph = basic_graph.basic_pentagon()
    graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)

    graph.display()
    plt.show()

    P16()(graph)
    P10()(graph)


if __name__ == "__main__":
    main()
