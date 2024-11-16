from random import shuffle
from tictactoegame import Game 
from abc import ABC, abstractmethod

class Policy(ABC):
    @abstractmethod
    def predict(self, game: Game, checkvalue: str) -> int:
        pass

class Random(Policy):
    def __init__(self) -> None:
        super().__init__()
        
    def predict(self, game: Game, checkvalue: str) -> int:
        free_states = game.free_states(checkvalue)
        shuffle(free_states)
        return free_states[0]
             

        



class Greedy(Policy):
    def __init__(self) -> None:
        super().__init__()
        self._init_valuefunc()

    def _init_valuefunc(self):
        valuefunc = {}
        for i in range(3**9):
            b = Game(i)
            if b._islegal():
                if b.wins("x"):
                    valuefunc[i] = 1
                else:
                    valuefunc[i] = 0

    def update(self):
        pass

    @abstractmethod
    def predict(self, game: Game, mark: str) -> int:
        pass

class Agent:
    def __init__(self, policy: Policy, mark: str):
        assert mark in ["x",  "o"]
        self.mark = mark

        if self.mark == "x":
            self.myturns = 0
        else:
            self.myturns = 1
        self.policy = policy

class Match:
    def __init__(self, agent_1: Agent, agent_2: Agent):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, game: Game):
        won = False
        turn = 0
        while won is False:
            moving_agent = [self.agent_1, self.agent_2][turn % 2]
            x_or_o = ["x", "o"][turn % 2]
            game.update_state(moving_agent.predict(game, x_or_o))
            game.draw()
            turn += 1
            if game.wins("x") or game.wins("o"):
                won = True
                game.draw()

