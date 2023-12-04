# Graphviz + NetworkX

This function is especially interesting for us, as is finds given subgraph in our graph.

https://networkx.org/documentation/stable/reference/algorithms/isomorphism.vf2.html#subgraph-isomorphism
https://networkx.org/documentation/stable/reference/algorithms/isomorphism.html

How to use it:

https://stackoverflow.com/questions/23151289/check-whether-a-networkx-graph-is-a-subgraph-of-another-one

Some background paper, we don't need it most likely at all
https://www.sciencedirect.com/science/article/abs/pii/S0378437119307447

Pygraphviz docs
https://pygraphviz.github.io/documentation/latest/pygraphviz.pdf


Other useful links
https://www.graphviz.org/
https://graphviz.readthedocs.io/en/stable/manual.html
https://networkx.org/documentation/stable/tutorial.html#adding-attributes-to-graphs-nodes-and-edges

# Graph tool 

In case of performance issues we can use `graph-tool` implemented in C++ using boost graph libraries (the performance boost should be on turbo level)

It works great with graphviz, so we are safe on that front

https://git.skewed.de/count0/graph-tool/-/wikis/installation-instructions
https://graph-tool.skewed.de/static/doc/autosummary/graph_tool.topology.isomorphism.html
https://graph-tool.skewed.de/static/doc/autosummary/graph_tool.topology.subgraph_isomorphism.html
