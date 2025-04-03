import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict


from agent import *
from random import *
from game_manager import *
from random_agent import *

# Simulation parameters
NUM_GAMES = 50  # Number of games per depth
DEPTHS = [1, 2, 3, 4]  # Depths to test


def send_to_file(file_path,data):
    with open(file_path,'a') as f:
        f.write(data)

def generate_filename():
    """Generates a filename based on the current date and time."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"game_stats_{timestamp}.txt"


def run_experiment(agent_class, random_agent_class, game_manager_class):
    results = defaultdict(lambda: {"wins": 0, "losses": 0, "times_per_move": [], "total_moves": []})
    
    
    for depth in DEPTHS:
        print(f"Running {NUM_GAMES} games for depth {depth}...")
        for _ in range(NUM_GAMES):
            agent_1 = agent_class(1, depth)
            agent_2 = random_agent_class(-1)
            game_manager = game_manager_class(agent_1, agent_2, display=False)
            
            move_times = []
            start_time = time.perf_counter()
            p1_score, p2_score = game_manager.play()
            end_time = time.perf_counter()
            
            game_duration = end_time - start_time
            num_moves = len(move_times)
            avg_time_per_move = sum(move_times) / num_moves if num_moves > 0 else 0
            
            results[depth]["wins"] += (1 if p1_score > p2_score else 0)
            results[depth]["losses"] += (1 if p1_score < p2_score else 0)
            results[depth]["times_per_move"].append(avg_time_per_move)
            results[depth]["total_moves"].append(num_moves)

    return results

def plot_results(results):
    depths = list(results.keys())
    wins = [results[d]["wins"] for d in depths]
    avg_times = [np.mean(results[d]["times_per_move"]) for d in depths]
    avg_moves = [np.mean(results[d]["total_moves"]) for d in depths]
    
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))
    axs[0].bar(depths, wins, color='blue')
    axs[0].set_title("Number of Wins per Depth")
    axs[0].set_xlabel("Depth")
    axs[0].set_ylabel("Wins")
    
    axs[1].plot(depths, avg_times, marker='o', color='red')
    axs[1].set_title("Average Time per Move by Depth")
    axs[1].set_xlabel("Depth")
    axs[1].set_ylabel("Time (seconds)")
    
    axs[2].plot(depths, avg_moves, marker='o', color='green')
    axs[2].set_title("Average Number of Moves per Game by Depth")
    axs[2].set_xlabel("Depth")
    axs[2].set_ylabel("Moves")
    
    plt.tight_layout()
    plt.show()

# Example usage:
# results = run_experiment(AlphaBetaAgent, RandomAgent, TextGameManager)
# plot_results(results)


