# agents/q_learning_bot.py
import chess
import random
import numpy as np

class QLearningBot:
    def __init__(self, color, learning_rate=0.1, discount_factor=0.9, epsilon=0.9):
        self.color = color
        self.q_table = {}  # The Q-table: {(state): {action_uci: q_value}}

        # RL parameters
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = 0.9995
        self.epsilon_min = 0.05

    # THIS IS THE CORRECTED VERSION of the function
    def get_simplified_state(self, board):
        """
        Converts the board state into a simplified tuple for the Q-table.
        State = (our total material, opponent total material, our # of legal moves)
        """
        my_material = sum(len(board.pieces(pt, self.color)) for pt in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN])
        opp_material = sum(len(board.pieces(pt, not self.color)) for pt in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN])
        
        # --- FIX IS HERE ---
        # Create a temporary copy of the board to calculate mobility
        # without changing the real board's turn.
        temp_board = board.copy()
        temp_board.turn = self.color
        my_mobility = temp_board.legal_moves.count()
        
        return (my_material, opp_material, my_mobility)

    def choose_action(self, board, legal_moves):
        """
        Chooses an action using an epsilon-greedy policy.
        """
        state = self.get_simplified_state(board)

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(legal_moves)  # Explore
        else:
            state_actions = self.q_table.get(state, {})
            if not state_actions:
                return random.choice(legal_moves)  # Explore if state is new
            
            # Exploit: choose the best known move that is currently legal
            best_move_uci = None
            max_q = -float('inf')
            
            # Find the best legal move from our Q-table
            legal_moves_uci = {m.uci() for m in legal_moves}
            for move_uci, q_val in state_actions.items():
                if move_uci in legal_moves_uci and q_val > max_q:
                    max_q = q_val
                    best_move_uci = move_uci
            
            return chess.Move.from_uci(best_move_uci) if best_move_uci else random.choice(legal_moves)

    def update(self, state, action, reward, next_state):
        """
        Updates the Q-table using the Bellman equation.
        """
        action_uci = action.uci()
        old_value = self.q_table.setdefault(state, {}).get(action_uci, 0)
        
        next_max = max(self.q_table.get(next_state, {}).values()) if self.q_table.get(next_state) else 0
        
        new_value = old_value + self.lr * (reward + self.gamma * next_max - old_value)
        self.q_table[state][action_uci] = new_value

    def decay_epsilon(self):
        """Reduces the exploration rate."""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay