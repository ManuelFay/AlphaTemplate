from typing import Optional

from alpha_template.agents.mcts_agent import MCTSAgent
from alpha_template.engines.neural_mcts import NeuralMCTS


class NeuralMCTSAgent(MCTSAgent):
    def __init__(self,
                 simulation_time: float = 3.,
                 training_path: Optional[str] = None,
                 show_pbar: bool = False,
                 model_path: Optional[str] = None):
        super().__init__(simulation_time, training_path, show_pbar)
        self.tree = NeuralMCTS(model_path=model_path)
