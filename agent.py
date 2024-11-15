from tictactoegame import game 
from abc import ABC, abstractmethod

class Policy(ABC):
    @abstractmethod
    def predict(self):
        pass

class Greedy(Policy):
    def __init__(self) -> None:
        super().__init__()

        self._init_valuefunc()

    def _init_valuefunc(self):
        valuefunc = {}
        for i in range(3**9):
            b = game(i)
            if b._islegal():
                if b.wins("x"):
                    valuefunc[i] = 1
                else:
                    valuefunc[i] = 0
    def update(self):
        pass
    def predict(self):
        pass
class agent:
    def __init__(self, policy: Policy):
        self.policy = policy
