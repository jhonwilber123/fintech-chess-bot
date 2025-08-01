# play_gui.py
import pygame
import chess
import pickle
from agents.q_learning_bot import QLearningBot

# --- Pygame Setup ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8
ASSET_PATH = 'assets/'

# Colors
WHITE = (238, 238, 210)
GREEN = (118, 150, 86)
HIGHLIGHT_COLOR = (255, 255, 51, 100) # Yellow with transparency

def load_assets():
    """Loads piece images into a dictionary."""
    pieces = {}
    piece_symbols = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for symbol in piece_symbols:
        path = f"{ASSET_PATH}{symbol}.png"
        pieces[symbol] = pygame.transform.scale(pygame.image.load(path), (SQUARE_SIZE, SQUARE_SIZE))
    return pieces

def draw_board(screen):
    """Draws the checkered board."""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board, assets):
    """Draws the pieces on the board."""
    for row in range(8):
        for col in range(8):
            square = chess.square(col, 7 - row) # chess library rows are bottom-up
            piece = board.piece_at(square)
            if piece:
                # Construct the symbol (e.g., 'w' + 'P' -> 'wP')
                symbol = f"{'w' if piece.color == chess.WHITE else 'b'}{piece.symbol().upper()}"
                screen.blit(assets[symbol], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def main():
    # --- Load the Bot ---
    print("Loading the trained Q-learning bot...")
    try:
        with open('q_table.pkl', 'rb') as f:
            q_table = pickle.load(f)
    except FileNotFoundError:
        print("Error: q_table.pkl not found. Please run train.py first.")
        return

    bot = QLearningBot(color=chess.WHITE)
    bot.q_table = q_table
    bot.epsilon = 0  # Exploitation mode

    # --- Initialize Pygame and the Board ---
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fintech Chess Bot")
    assets = load_assets()
    board = chess.Board()
    
    selected_square = None
    player_from_square = None
    running = True
    
    while running:
        # --- Handle Bot's Turn ---
        if board.turn == bot.color and not board.is_game_over():
            pygame.display.set_caption("Fintech Chess Bot - Bot is thinking...")
            legal_moves = list(board.legal_moves)
            if legal_moves:
                bot_move = bot.choose_action(board, legal_moves)
                print(f"Bot plays: {bot_move.uci()}")
                board.push(bot_move)
            pygame.display.set_caption("Fintech Chess Bot")

        # --- Event Handling (Player's Turn) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and board.turn == chess.BLACK:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                square_index = chess.square(col, 7 - row)

                if player_from_square is None:
                    # First click: select a piece
                    piece = board.piece_at(square_index)
                    if piece and piece.color == chess.BLACK:
                        player_from_square = square_index
                        selected_square = (col, row)
                else:
                    # Second click: make a move
                    player_to_square = square_index
                    move = chess.Move(player_from_square, player_to_square)
                    
                    # Handle promotions automatically (defaults to Queen)
                    if board.piece_type_at(player_from_square) == chess.PAWN and chess.square_rank(player_to_square) == 0:
                        move = chess.Move(player_from_square, player_to_square, promotion=chess.QUEEN)

                    if move in board.legal_moves:
                        board.push(move)
                    
                    # Reset selection
                    player_from_square = None
                    selected_square = None

        # --- Drawing ---
        draw_board(screen)
        
        # Highlight selected square
        if selected_square:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(HIGHLIGHT_COLOR)
            screen.blit(s, (selected_square[0] * SQUARE_SIZE, selected_square[1] * SQUARE_SIZE))
            
        draw_pieces(screen, board, assets)
        pygame.display.flip()

        # --- Check for Game Over ---
        if board.is_game_over():
            result = board.result()
            print(f"Game Over. Result: {result}")
            pygame.time.wait(3000) # Wait 3 seconds before closing
            running = False

    pygame.quit()

if __name__ == '__main__':
    main()