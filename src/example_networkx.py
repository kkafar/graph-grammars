# import graphviz
#
# dot = graphviz.Digraph('round-table')
#
# dot.node('A', 'King Arthur')
# dot.node('B', 'Sir Bedevere the Wise')
# dot.node('L', 'Sir Lancelot the Brave')
#
# dot.edges(['AB', 'AL'])
# dot.edge('B', 'L', constraint='false')
import networkx as nx

G = nx.complete_graph(5)
A = nx.nx_agraph.to_agraph(G)  # convert to a graphviz graph
X1 = nx.nx_agraph.from_agraph(A)  # convert back to networkx (but as Graph)
X2 = nx.Graph(A)  # fancy way to do conversion
G1 = nx.Graph(X1)  # now make it a Graph

A.write("k5.dot")  # write to dot file
X3 = nx.nx_agraph.read_dot("k5.dot")  # read from dotfile

# You can also create .png directly with the AGraph.draw method
A.draw("k5.png", prog="neato")
