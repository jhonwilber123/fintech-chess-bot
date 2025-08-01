# train.py
import chess
from chess_env import ChessEnvironment
from agents.q_learning_bot import QLearningBot
from agents.value_bot import ValueBot
import pickle
from tqdm import tqdm

def train(episodes=10000):
    print("Initializing agents and environment...")
    
    # The agent we want to train
    learning_agent = QLearningBot(color=chess.WHITE)
    
    # Its sparring partner
    opponent_agent = ValueBot(color=chess.BLACK, chess_environment=ChessEnvironment())
    
    print(f"Starting training for {episodes} episodes...")
    for episode in tqdm(range(episodes)):
        env = ChessEnvironment()
        board = env.reset()
        done = False

        while not done:
            if board.turn == learning_agent.color:
                # Learning Agent's turn
                state = learning_agent.get_simplified_state(board)
                legal_moves = list(board.legal_moves)
                if not legal_moves: break
                
                action = learning_agent.choose_action(board, legal_moves)
                
                board_after_move, reward, done = env.step(action)
                next_state = learning_agent.get_simplified_state(board_after_move)
                
                learning_agent.update(state, action, reward, next_state)
            else:
                # Opponent's turn
                move = opponent_agent.get_move(board)
                if move:
                    env.board.push(move)
            
            done = env.board.is_game_over()
        
        learning_agent.decay_epsilon()

    # Save the learned Q-table
    print("\nTraining complete.")
    print(f"Q-table has {len(learning_agent.q_table)} states.")
    with open('q_table.pkl', 'wb') as f:
        pickle.dump(learning_agent.q_table, f)
    print("Q-table saved to q_table.pkl")

if __name__ == "__main__":
    train(episodes=20000) # Let's train for 20,000 games. This can take a while!