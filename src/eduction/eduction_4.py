from production.production_7 import P7
from ..util import reverse_dict_mapping

p7 = P7()

graph = p7.get_lhs()

mappings = graph.generate_subgraphs_isomorphic_with(p7.get_lhs())

highest_y = 0
highest_y_id = -1
for mapping in mappings:
    rev_mapping = reverse_dict_mapping(mapping)
    print(rev_mapping)
