from pandas.core import window
from agents import Agent, RandomPolicy, TDPolicy 
from tictactoegame import Game
from matplotlib import pyplot as plt
import pandas as pd

class Match:
    def __init__(self, agent_1: Agent, agent_2: Agent):
        assert set([agent_2.mark, agent_1.mark]) == set(["x", "o"])

        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, game: Game) -> None | Agent:
        won = False
        winner = None
        turn = 0
        if self.agent_2.mark == "x": 
            order = [self.agent_2, self.agent_1]
        else:
            order = [self.agent_1, self.agent_2]
        while won is False and turn < 9:
            moving_agent = order[turn % 2]
            old_state = game._get_state_num()
            game.update_state(moving_agent.predict(game))
            new_state = game._get_state_num()

            self.agent_1.policy.update(old_state, new_state)
            self.agent_2.policy.update(old_state, new_state)

            turn += 1
            if game.wins("x") or game.wins("o"):
                won = True
                winner = moving_agent        
        return winner

if __name__ == "__main__":
    a_1 = Agent(TDPolicy(0.01, 0.1, None, "o"), "o")
    # a_2 = Agent(TDPolicy(0.01, None, "o"), "o")
    a_2 = Agent(RandomPolicy(), "x")
    # a_1 = Agent(RandomPolicy(), "x")
    m = Match(a_1, a_2)
    a1_wins, a2_wins, draws, total = 0,0,0,0
    a_1_history, a_2_history, draw_history = [], [], []
    history = []

    num_games = 10000
    for i in range(num_games):
        g = Game()
        winner = m.play(g)
        if winner == a_1:
            a1_wins += 1
            history.append(1)
        elif winner == a_2:
            a2_wins += 1
            history.append(-1)
        else:
            draws += 1
            history.append(0)
        total += 1
        if i % (num_games/100) == 0:
            print(f"{(100*i)/num_games}%", end="\r")
            # valuefunc = list(set([a_1.policy.valuefunc[k] for k in a_1.policy.valuefunc.keys()]))
            # valuefunc.sort() 
            # print(len(valuefunc))
            # print(valuefunc)
            # largest = 0
            # largest_k = 0
            # for k in a_1.policy.valuefunc.keys():
            #     if  a_1.policy.valuefunc[k] < 1:
            #         if a_1.policy.valuefunc[k] > largest:
            #             largest = a_1.policy.valuefunc[k]
            #             largest_k = k
            # Game(largest_k).draw()
            #
    df = pd.DataFrame({"game_number": range(len(history)), "result": history})


    df["rolling_win_rate_a1"] = df["result"].rolling(window=300).apply(lambda x: (x > 0).mean(), raw=True)
    df["rolling_win_rate_a2"] = df["result"].rolling(window=300).apply(lambda x: (x < 0).mean(), raw=True)
    df["rolling_draw_rate"] = df["result"].rolling(window=300).apply(lambda x: (x == 0).mean(), raw=True)

    # Plotting
    plt.figure(figsize=(12, 6))

    plt.plot(df["game_number"], df["rolling_win_rate_a1"], label="Agent 1 Win Rate", color="blue")
    plt.plot(df["game_number"], df["rolling_win_rate_a2"], label="Agent 2 Win Rate", color="red")
    plt.plot(df["game_number"], df["rolling_draw_rate"], label="Draw Rate", color="gray")
    plt.axhline(0.5, color="black", linestyle="--", label="50% Threshold")

    plt.xlabel("Game Number")
    plt.ylabel("Rate")
    plt.title("Rolling Win/Draw Rates Over Time")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
