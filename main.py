from agents import Agent, RandomPolicy, TDPolicy 
from tictactoegame import Game
from matplotlib import pyplot as plt

class Match:
    def __init__(self, agent_1: Agent, agent_2: Agent):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def play(self, game: Game) -> None | Agent:
        won = False
        winner = None
        turn = 0
        while won is False and turn < 9:
            moving_agent = [self.agent_1, self.agent_2][turn % 2]
            game.update_state(moving_agent.predict(game))
            turn += 1
            if game.wins("x") or game.wins("o"):
                won = True
                winner = moving_agent        
        return winner

if __name__ == "__main__":
    a_1 = Agent(TDPolicy(0.01, None, "x"), "x")
    a_2 = Agent(RandomPolicy(), "o")
    m = Match(a_1, a_2)
    a1_wins, a2_wins, draws, total = 0,0,0,0
    a_1_history, a_2_history, draw_history = [], [], []

    for i in range(1000):
        g = Game()
        winner = m.play(g)
        if winner == a_1:
            a1_wins += 1
        elif winner == a_2:
            a2_wins += 1
        else:
            draws += 1
        total += 1
        draw_history.append(draws/total)
        a_2_history.append(a2_wins/total)
        a_1_history.append(a1_wins/total)

    plt.plot(a_1_history, label="A1 History")
    plt.plot(a_2_history, label="A2 History")
    plt.plot(draw_history, label="Draw History")
    plt.legend()  # Add a legend to differentiate lines
    plt.savefig("test.png")
