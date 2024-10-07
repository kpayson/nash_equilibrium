import configparser
import argparse
import matplotlib.pyplot as plt
import player
import game_config_parser
import matplotlib
import random

# Switch to the TkAgg backend
matplotlib.use('TkAgg')

config = configparser.ConfigParser()
config.read('./config.ini')

# Read the command line using argparse
arg_parser = argparse.ArgumentParser(description='Nash Equilibrium Simulation')
arg_parser.add_argument('-g','--game', type=str, choices=['pd', 'sh', 'bs'], help='The game to simulate: choices are pd, sh, bs') 
arg_parser.add_argument('-c','--chart', type=str, choices=['line', 'scatter'], help='The output chart type: choices are line, scatter') 
args = arg_parser.parse_args()
game = args.game
chart_type = args.chart

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

def line_chart_plot_result(p1,p2,x_pos, y_pos):
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
    
    
def scatter_plot_chart_result(p1,p2,x_pos, y_pos):
    # Create a new figure
    plt.figure()
    
    def count_frequencies(numbers):
        frequency_dict = {}
        for number in numbers:
            if number in frequency_dict:
                frequency_dict[number] += 1
            else:
                frequency_dict[number] = 1
        return frequency_dict
    
    dot_scale = 10

    p1_freq_dict = count_frequencies(players[p1].all_preferences())
    p1_strats_unique = list(p1_freq_dict.keys())
    p1_counts = list(p1_freq_dict.values())
    p1_sizes = [s*dot_scale for s in p1_counts]
    
    p2_freq_dict = count_frequencies(players[p2].all_preferences())
    p2_strats_unique = list(p2_freq_dict.keys())
    p2_counts = list(p2_freq_dict.values())
    p2_sizes = [s*dot_scale for s in p2_counts]
    
    p1_y_vals = list(p1_strats_unique)
    p1_x_vals = [1 - y_val for y_val in p1_y_vals] 

    p2_y_vals = list(p2_strats_unique)
    p2_x_vals = [1 - y_val for y_val in p2_y_vals]
  
    # plot
    fig, ax = plt.subplots()

    # adjusting transparency of scatter points by using 'alpha' parameter
    # https://dfrieds.com/data-visualizations/customize-scatter-plot-styles-python-matplotlib.html#adjust-the-size-of-scatter-points
    ax.scatter(p1_x_vals, p1_y_vals, s=p1_sizes, c='blue', label='P1', alpha=0.3)
    ax.scatter(p2_x_vals, p2_y_vals, s=p2_sizes, c='orange', label='P2', alpha=0.4)

    # labels and title
    ax.set_xlabel(strategies[0], fontsize=10)
    ax.set_ylabel(strategies[1], fontsize=10)
    ax.set_title(title)

    # show grid
    ax.grid(True)

    # create some mock scatterpoints for the legend, otherwise
    p1LegendX = [0.5]
    p1LegendY = [0.5]
    p1LegendSize = [50]
    p1CollectionLegend = ax.scatter(p1LegendX, p1LegendY, s=p1LegendSize, c='blue', alpha=0.3)

    p2LegendX = [0.5]
    p2LegendY = [0.5]
    p2LegendSize = [50]
    p2CollectionLegend = ax.scatter(p2LegendX, p2LegendY, s=p2LegendSize, c='orange', alpha=0.4)

    plt.legend([p1CollectionLegend, p2CollectionLegend], ['P1', 'P2'])

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

if(chart_type == 'line'):
    line_chart_plot_result(0, 1, 100, 100)
    line_chart_plot_result(3, 5, 500, 100)
    line_chart_plot_result(2, 7, 900, 100)
    line_chart_plot_result(5, 6, 100, 500)
    line_chart_plot_result(7, 8, 500, 500)

elif(chart_type == 'scatter'):
    scatter_plot_chart_result(0, 1, 100, 100)
    scatter_plot_chart_result(2, 3, 500, 100)
    scatter_plot_chart_result(3, 4, 900, 100)
    scatter_plot_chart_result(5, 6, 100, 500)
    scatter_plot_chart_result(7, 8, 500, 500)
# Keep all windows open
plt.show()