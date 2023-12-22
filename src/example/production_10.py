from graph import Graph
import basic_graph
import matplotlib.pyplot as plt
from production import P10

def main():
    fig, plots = plt.subplots(nrows=1, ncols=2)

    graph = basic_graph.basic_pentagon()
    graph.split_edge_with_vnode(edge=(0, 1), node_flag=True)

    graph.display(ax=plots[0])
    plots[0].set(title='Before')

    assert P10()(graph)

    graph.display(ax=plots[1])
    plots[1].set(title='After')

    fig.suptitle("Applying production 10")
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
