import basic_graph
import matplotlib.pyplot as plt
from production import P16
from graph import Graph


def main():
    graph, _ = basic_graph.basic_star5()
    graph.display()
    plt.show()
    P16(5)(graph)


if __name__ == "__main__":
    main()

