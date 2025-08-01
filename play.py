# play.py
import chess
import pickle
from agents.q_learning_bot import QLearningBot

def play():
    # --- Load the Trained Agent ---
    print("Loading the trained Q-learning bot...")
    try:
        with open('q_table.pkl', 'rb') as f:
            q_table = pickle.load(f)
    except FileNotFoundError:
        print("Error: q_table.pkl not found. Please run train.py first.")
        return

    # --- Setup the Game ---
    # Our trained bot will play as White
    bot = QLearningBot(color=chess.WHITE)
    bot.q_table = q_table
    bot.epsilon = 0  # IMPORTANT: Set epsilon to 0 for exploitation mode (no random moves)
    
    board = chess.Board()
    print("Game start. You are playing as Black. Good luck!")

    # --- Game Loop ---
    while not board.is_game_over():
        print("\n" + str(board))
        
        if board.turn == bot.color:
            # Bot's turn
            print("\nBot is thinking...")
            legal_moves = list(board.legal_moves)
            if not legal_moves: break
            
            bot_move = bot.choose_action(board, legal_moves)
            print(f"Bot plays: {bot_move.uci()}")
            board.push(bot_move)
        else:
            # Human's turn (as Black)
            move_uci = None
            while True:
                try:
                    move_uci = input("Enter your move in UCI format (e.g., g8f6): ")
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        board.push(move)
                        break
                    else:
                        print("That move is not legal. Try again.")
                except ValueError:
                    print("Invalid format. Please use UCI format (e.g., e2e4).")

    # --- Game Over ---
    print("\n--- GAME OVER ---")
    print(f"Final Board Position:\n{board}")
    result = board.result()
    print(f"Result: {result}")
    if result == "1-0":
        print("The Bot (White) wins!")
    elif result == "0-1":
        print("Congratulations, you (Black) win!")
    else:
        print("The game is a draw.")

if __name__ == "__main__":
    play()