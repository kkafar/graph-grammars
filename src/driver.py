from typing import Iterable, Callable, Optional
from production import Production
from graph import Graph
from model import NodeHandle
from pathlib import Path
import matplotlib.pyplot as plt


class InputProvider:
    """ This class is used by the `Driver` to get handle of hyperedge marked for breaking.
    """
    def __call__(self):
        raise NotImplementedError("__call__ must be implemented")


class FixedInput(InputProvider):
    """ Use this class to provide driver with fixed node handle to mark for breaking.
    """
    def __init__(self, hypernode_handle: NodeHandle) -> None:
        assert hypernode_handle is not None
        self.handle = hypernode_handle

    def __call__(self):
        return self.handle


class UserInput(InputProvider):
    """ Use this class to let user decide what node should be marked for breaking.
    """
    def __call__(self) -> NodeHandle:
        return int(input("NodeHandle> "))


class DriverDelegate:
    def on_production_success(self, prod: Production, graph: Graph):
        pass

    def on_production_failure(self, prod: Production, graph: Graph):
        pass

    def on_execution_start(self, graph: Graph, callables: Iterable[Production | InputProvider]):
        pass

    def on_execution_end(self, graph: Graph, callables: Iterable[Production | InputProvider]):
        pass

    def on_manual_input(self, graph: Graph, user_input: NodeHandle):
        pass


class DrawingDriverDelegate(DriverDelegate):
    def __init__(self, savedir: Optional[Path], newstyleplot: bool = True) -> None:
        self.savedir = savedir
        self.newstyle = newstyleplot
        self.counter = 0

    def on_execution_start(self, graph: Graph, callables: Iterable[Production | InputProvider]):
        fig, plot = plt.subplots(nrows=1, ncols=1)
        graph.display(newstyle=self.newstyle, ax=plot)
        plot.set(title='Graph before applying production sequence')
        if self.savedir is not None:
            savefile = self.savedir.joinpath('graph_before.png')
            fig.tight_layout()
            fig.savefig(savefile)
            plt.close(fig)


    def on_production_success(self, prod: Production, graph: Graph):
        print(f'Successfully applied {prod}')
        fig, plot = plt.subplots(nrows=1, ncols=1)
        graph.display(newstyle=self.newstyle, ax=plot)
        plot.set(title=f'Graph after {prod}')

        if self.savedir is not None:
            print(self.counter)
            savefile = self.savedir.joinpath(f'{self.counter}_graph_after_prod_{prod}.png')
            self.counter += 1
            fig.tight_layout()
            plt.savefig(savefile)
            plt.close(fig)


    def on_execution_end(self, graph: Graph, callables: Iterable[Production | InputProvider]):
        fig, plot = plt.subplots(nrows=1, ncols=1)
        graph.display(newstyle=self.newstyle, ax=plot)
        plot.set(title='Graph after applying production sequence')
        if self.savedir is not None:
            savefile = self.savedir.joinpath('graph_after.png')
            fig.tight_layout()
            fig.savefig(savefile)
            plt.close(fig)

    def on_manual_input(self, graph: Graph, user_input: NodeHandle):
        fig, plot = plt.subplots(nrows=1, ncols=1)
        graph.display(newstyle=self.newstyle, ax=plot)
        plot.set(title=f'Graph after user manually marked {user_input} to break')
        if self.savedir is not None:
            print(self.counter)
            savefile = self.savedir.joinpath(f'{self.counter}_graph_after_mi.png')
            self.counter += 1
            fig.tight_layout()
            fig.savefig(savefile)
            plt.close(fig)



class Driver:
    def __init__(self, delegate = DriverDelegate()) -> None:
        self.delegate = delegate

    def execute_production_sequence(self, graph: Graph, callables: Iterable[Production | InputProvider]):
        self.delegate.on_execution_start(graph, callables)
        for func in callables:
            if isinstance(func, Production):
                if func(graph):
                    self.delegate.on_production_success(func, graph)
                else:
                    self.delegate.on_production_failure(func, graph)
                    assert False, f"Production {func} failed"

            elif isinstance(func, InputProvider):
                user_input = func()
                graph.update_hyperedge_flag(user_input, True)
                self.delegate.on_manual_input(graph, user_input)
            else:
                raise RuntimeError("HEHE")

        self.delegate.on_execution_end(graph, callables)

