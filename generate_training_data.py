import sys
from tqdm import tqdm

from alpha_template.agents.mcts_agent import MCTSAgent
from alpha_template.agents.neural_mcts_agent import NeuralMCTSAgent

from gameplay.game import Game

# Parallelize to generate samples in parallel
for _ in tqdm(range(500)):
    try:
        agent0 = MCTSAgent(simulation_time=1,  training_path="./data/training_neural_pipo.npy")
        agent1 = MCTSAgent(simulation_time=1,  training_path="./data/training_neural_pipo.npy")

        game = Game(agent0=agent0, agent1=agent1, enable_ui=True)
        game.play()
    except Exception as exception:
        print(exception)

sys.exit()
