from ast import Load
from random import shuffle, random
import pickle
from tictactoegame import Game 
from abc import ABC, abstractmethod

class Policy(ABC):
    @abstractmethod
    def predict(self, game: Game, checkvalue: str) -> int:
        pass

class RandomPolicy(Policy):
    def __init__(self) -> None:
        super().__init__()
        
    def predict(self, game: Game, checkvalue: str) -> int:
        free_states = game.free_states(checkvalue)
        shuffle(free_states)
        return free_states[0]

class TDPolicy(Policy):
    def __init__(self, step_size_parameter: float, exploration_parameter: float, pickle_path: str|None, mark:str) -> None:
        super().__init__()
        self.mark = mark
        self.step_size_parameter = step_size_parameter
        self.exploration_parameter = exploration_parameter
        
        if pickle_path is None:
            self.valuefunc = self._init_valuefunc()
        else: 
            self.valuefunc = self.load_valuefunc(pickle_path)

    def _init_valuefunc(self) -> dict:
        valuefunc = {}
        if self.mark == "x":
            other_mark = "o"
        else: 
            other_mark = "x"

        for i in range(3**9):
            b = Game(i)
            if b._islegal():
                if b.wins(self.mark):
                    valuefunc[i] = 1
                elif b.wins(other_mark):
                    valuefunc[i] = 0
                else:
                    valuefunc[i] = 0.5
        return valuefunc

    def save_valuefunc(self, filename: str):
        """Save the value function table to a file."""
        with open(f"pickles/{filename}", "wb") as f:
            pickle.dump(self.valuefunc, f)

    def load_valuefunc(self, filename: str) -> dict:
        """Load the value function table from a file."""
        with open(f"pickles/{filename}", "rb") as f:
            value_func = pickle.load(f)
            assert type(value_func) == dict
            return value_func

    def update(self, cur_state:  int, new_val: float):
        cur_val = self.valuefunc[cur_state]
        updatestep = cur_val + self.step_size_parameter * (new_val - cur_val)
        assert 0 <= updatestep <= 1.0 
        self.valuefunc[cur_state] = updatestep

    def predict(self, game: Game, checkvalue: str) -> int:
        free_states = game.free_states(checkvalue)
        shuffle(free_states)

        if random() > self.exploration_parameter:
            best_val = -1

            best_state = None
            for state in free_states:
                if self.valuefunc[state] > best_val:
                    best_state = state
                    best_val = self.valuefunc[state]

            if best_state is None:
                raise Exception("no best state")
            self.update(game._get_state_num(), best_val)

            return best_state
        else:
            return free_states[0]

        


class Agent:
    def __init__(self, policy: Policy, mark: str):
        assert mark in ["x",  "o"]
        self.mark = mark

        if self.mark == "x":
            self.myturns = 0
        else:
            self.myturns = 1
        self.policy = policy

    def predict(self, game: Game) -> int:
        return self.policy.predict(game, self.mark)

class Match:
    def __init__(self, agent_1: Agent, agent_2: Agent):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, game: Game):
        won = False
        turn = 0
        while won is False and turn < 9:
            moving_agent = [self.agent_1, self.agent_2][turn % 2]
            game.update_state(moving_agent.predict(game))
            game.draw()
            turn += 1
            if game.wins("x") or game.wins("o"):
                won = True
                game.draw()


if __name__ == "__main__":
    a_1 = Agent(TDPolicy(0.01, None, "x"), "x")
    a_2 = Agent(RandomPolicy(), "o")
    m = Match(a_1, a_2)


    for i in range(100000):
        g = Game()
        m.play(g)

    for key in a_1.policy.valuefunc.keys():
        print(key, a_1.policy.valuefunc[key])
