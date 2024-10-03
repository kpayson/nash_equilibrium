class GameConfigParser:
    def __init__(self, game):
        self.game = game
        
    def parse(self):
        # # Example of a game file:
        # # pd.txt

        # # the number below indicates the number of choices,
        # # which is helpful for file parsing
        # 2	

        # # title of game
        # Prisoner’s Dilemma Game
        # quiet   -1   -1	    -12  0
        # confess	  0  -12		-8   -8
  
        # Open the file in read mode
        with open(f"{self.game}.txt", 'r') as file:
            # Read all lines into a list
            lines = file.readlines()

        # Filter out lines that start with a #
        filtered_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]

        # first non-comment line has the count of choices
        choice_count = int(filtered_lines[0].strip())
        
        # second non-comment line has the title of the game
        title = filtered_lines[1].strip()
        
        strategies = []
        matrix = []
        
        for line in filtered_lines[2:]:
            tokens = line.split()
            strategy = tokens[0]
            payoffs = tokens[1:]
            strategies.append(strategy)
            row = []
            
            for i in range(0, len(payoffs), 2):
                payoff_pair = (int(payoffs[i]), int(payoffs[i + 1]))
                row.append(payoff_pair)
                
            matrix.append(row)
            
        return matrix, strategies, title
            
        
        