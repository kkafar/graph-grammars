from typing import Dict

def reverse_dict_mapping(dictionary: Dict[int, int]) -> Dict[int, int]:
    return {v: k for k, v in dictionary.items()}
