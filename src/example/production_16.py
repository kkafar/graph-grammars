import basic_graph
import matplotlib.pyplot as plt
from production import P16
from graph import Graph


def main():
    fig, plots = plt.subplots(nrows=1, ncols=2)

    graph, _ = basic_graph.basic_star5()

    graph.display(ax=plots[0])
    plots[0].set(title='Before')

    assert P16(5)(graph)

    graph.display(ax=plots[1])
    plots[1].set(title='After')

    fig.suptitle("Applying production 16")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

