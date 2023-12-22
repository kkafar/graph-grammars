import example.graph_creation
import example.production_1
import example.production_2
import example.production_9
import example.production_10
import example.production_16


__all__ = (
    graph_creation,
    production_1,
    production_2,
    production_9,
    production_10,
    production_16,
)


def main():
    for module in __all__:
        module.main()


if __name__ == "__main__":
    main()

