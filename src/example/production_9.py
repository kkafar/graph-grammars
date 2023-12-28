from graph import Graph
import basic_graph
import matplotlib.pyplot as plt
from production import P9, P16


def main():
    fig, plot = plt.subplots(nrows=1, ncols=1)
    graph = basic_graph.basic_pentagon()

    assert P16()(graph)

    graph.display()
    plot.set(title='Before')
    fig.suptitle("Applying production 9")
    fig.tight_layout()
    plt.show()

    assert P9()(graph)

    fig, plot = plt.subplots(nrows=1, ncols=1)
    graph.display()
    plot.set(title='After')
    fig.suptitle("Applying production 9")
    fig.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()

