# chess_env.py
import chess

class ChessEnvironment:
    """
    A chess environment that provides rewards based on material value.
    """
    def __init__(self):
        self.board = chess.Board()
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3.1,  # Slightly higher value for bishops
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }

    def reset(self):
        """Resets the board to the starting position."""
        self.board.reset()
        return self.board

    def get_material_value(self, color):
        """Calculates the total material value for a given color."""
        value = 0
        for piece_type, piece_value in self.piece_values.items():
            value += len(self.board.pieces(piece_type, color)) * piece_value
        return value

    def step(self, move):
        """
        Applies a move and calculates the reward from the perspective of the player who moved.
        Reward = (Our material change) - (Opponent's material change).
        """
        # Calculate material difference before the move
        my_color = self.board.turn
        value_before = self.get_material_value(my_color) - self.get_material_value(not my_color)

        # Make the move
        self.board.push(move)

        # Calculate material difference after the move
        # Note: The turn has now switched, so 'not my_color' is the new player.
        value_after = self.get_material_value(my_color) - self.get_material_value(not my_color)

        reward = value_after - value_before

        # Add a large bonus for winning or penalty for losing
        if self.board.is_checkmate():
            reward += 100
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            reward += 0 # No penalty for a draw

        done = self.board.is_game_over()
        
        return self.board, reward, done