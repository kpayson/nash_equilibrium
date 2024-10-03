import configparser
import argparse
import matplotlib.pyplot as plt
import player
import game_config_parser
import matplotlib

# Switch to the TkAgg backend
matplotlib.use('TkAgg')

config = configparser.ConfigParser()
config.read('./config.ini')

# Read the command line using argparse
arg_parser = argparse.ArgumentParser(description='Nash Equilibrium Simulation')
arg_parser.add_argument('game', type=str, choices=['pd', 'sh', 'bs'], help='The game to simulate: choices are pd, sh, bs') 
args = arg_parser.parse_args()
game = args.game

# Get the payoff matrix, strategies and title of the game
game_matrix, strategies, title = game_config_parser.GameConfigParser(game).parse()

number_of_players = int(config['game_simulation_settings']['number_of_players'])
number_of_sessions = int(config['game_simulation_settings']['number_of_sessions'])

number_games_total = (number_of_players -1) * number_of_sessions

players = [player.Player(i) for i in range(number_of_players)]

for s in range(number_of_sessions):
    for p1 in range(number_of_players):
        for p2 in range(p1+1, number_of_players):

            player1_strategy = players[p1].choose_strategy()
            player2_strategy = players[p2].choose_strategy()

            player1_score = game_matrix[player1_strategy][player2_strategy][0]
            player2_score = game_matrix[player1_strategy][player2_strategy][1]
            
            players[p1].update(player1_score, player1_strategy)
            players[p2].update(player2_score, player2_strategy)

def plot_result(p1,p2,x_pos, y_pos):
    # Create a new figure
    plt.figure()
      
    # Data for plotting
    x = list(range(number_games_total+1))

    # Create a plot
    plt.plot(x, players[p1].all_preferences(), label=f'player {p1}')
    plt.plot(x, players[p2].all_preferences(), label=f'player {p2}' )

    # Add a title and labels and legend
    plt.title(title)
    plt.xlabel("Game Number") 
    plt.ylabel(f"{strategies[1].capitalize()} Strategy Preference")
    plt.legend()
    
    fig = plt.gcf()
    fig.canvas.manager.set_window_title(f"Game Result: Player {p1} vs Player {p2}")

    # Move the window to the specified position
    backend = plt.get_backend()
    if backend == 'TkAgg':
        fig.canvas.manager.window.wm_geometry(f"+{x_pos}+{y_pos}")
    elif backend == 'Qt5Agg':
        fig.canvas.manager.window.setGeometry(x_pos, y_pos, 800, 600)
    else:
        print(f"Backend {backend} is not supported for window positioning")
        
    #Show the plot
    plt.show(block=False)
    
plot_result(0, 1, 100, 100)
plot_result(2, 3, 500, 100)
plot_result(3, 4, 900, 100)
plot_result(5, 6, 100, 500)
plot_result(7, 8, 500, 500)

# Keep all windows open
plt.show()