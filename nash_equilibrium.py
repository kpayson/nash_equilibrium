import configparser

import matplotlib.pyplot as plt
import player

config = configparser.ConfigParser()
config.read('./config.ini')

number_of_players = int(config['game_simulation_settings']['number_of_players'])
number_of_sessions = int(config['game_simulation_settings']['number_of_sessions'])

number_games_total = (number_of_players -1) * number_of_sessions

pd_matrix = [
    [(-1, -1),(-12, 0)],
    [(0, -12),(-8, -8)]
]   



players = [player.Player(i) for i in range(number_of_players)]

for s in range(number_of_sessions):
    for p1 in range(number_of_players):
        for p2 in range(p1+1, number_of_players):

            player1_strategy = players[p1].choose_strategy()
            player2_strategy = players[p2].choose_strategy()

            player1_score = pd_matrix[player1_strategy][player2_strategy][0]
            player2_score = pd_matrix[player1_strategy][player2_strategy][1]
            
            players[p1].update(player1_score)
            players[p2].update(player2_score)

# Data for plotting
x = list(range(number_games_total+1))

first_player = 1
second_player = 2

prefs_p1 = players[first_player].all_preferences()
prefs_p2 = players[second_player].all_preferences()

# Create a plot
plt.plot(x, prefs_p1, label='player ' + str(first_player))
plt.plot(x, prefs_p2, label='player ' + str(second_player))

# Add a title and labels and legend
plt.title("Nash Equilibrium Simulation") #config['plot_settings']['title']
plt.xlabel("Game Number") #config['plot_settings']['xlabel']
plt.ylabel("Strategy Preference") #config['plot_settings']['ylabel']
plt.legend()

# # Show the plot
plt.show()