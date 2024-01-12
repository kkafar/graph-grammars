from example import (
    graph_creation,
    monomorphism,
    production_1,
    production_2,
    production_5,
    production_6,
    production_9,
    production_10,
    production_11,
    production_12,
    production_13,
    production_16,
    production_17,
    derivation_1,
)

__all__ = (
    graph_creation,
    monomorphism,
    production_1,
    production_2,
    production_5,
    production_6,
    production_9,
    production_10,
    production_11,
    production_12,
    production_13,
    production_16,
    production_17,
    derivation_1
)


def main():
    for module in __all__:
        module.main()


if __name__ == "__main__":
    main()

