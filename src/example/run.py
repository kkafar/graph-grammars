import networkx as nx
import graphviz
import itertools as it
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
from graph import Graph
from example.production_1 import test_1
from example.production_9 import test_16_9
from example.production_10 import test_10
from example.production_16 import test_16

def main():
    plt.rcParams['figure.figsize'] = (16, 9)
    if len(sys.argv) < 2:
        print("please provide one of the arguments: 1, 16, 169, 10")
        exit()
    arg = sys.argv[1]
    if arg == '1':
        print("hello")
        test_1()
    elif arg == '16':
        test_16()
    elif arg == '169':
        test_16_9()
    elif arg == '10':
        test_10()

if __name__ == "__main__":
    main()
