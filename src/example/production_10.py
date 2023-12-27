from graph import Graph
import basic_graph
import matplotlib.pyplot as plt
from production import P10, P16

def main():
    fig, plot = plt.subplots(nrows=1, ncols=1)

    graph = basic_graph.basic_pentagon()
    graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)

    assert P16()(graph)

    graph.display()
    plot.set(title='Before')
    fig.suptitle("Applying production 10")
    fig.tight_layout()
    plt.show()

<<<<<<< HEAD
    P10()(graph)
    graph.display()
=======
    assert P10()(graph)

    fig, plot = plt.subplots(nrows=1, ncols=1)
    graph.display()
    plot.set(title='After')
    fig.suptitle("Applying production 10")
    fig.tight_layout()
>>>>>>> origin/main
    plt.show()



if __name__ == "__main__":
    main()
