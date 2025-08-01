# agents/value_bot.py
import chess

class ValueBot:
    """
    A simple chess bot that greedily chooses the move with the highest
    immediate material gain. It does not learn.
    """
    def __init__(self, color, chess_environment):
        self.color = color
        self.env = chess_environment

    def get_move(self, board):
        """
        Finds the best move by checking the reward for all legal moves.
        """
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None

        best_move = legal_moves[0]
        max_reward = -float('inf')
        
        original_board_fen = board.fen()

        for move in legal_moves:
            # Simulate making the move in the environment
            temp_board = chess.Board(original_board_fen)
            temp_env = self.env
            temp_env.board = temp_board
            
            _, reward, _ = temp_env.step(move)

            if reward > max_reward:
                max_reward = reward
                best_move = move
        
        # Reset the environment board state after checking
        self.env.board.set_fen(original_board_fen)
        return best_move