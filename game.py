# %%
import numpy as np

# %%
BACKGROUND_CHAR = ' '
FILLED_CHAR = 'O'


class ConsoleGame:

    def __init__(self, map_path):
        self.map_path = map_path
        self.map = None
        self.load_map(self.map_path)

    def load_map(self, map_path):
        with open(map_path, 'r') as f:
            lines = f.read().splitlines()
        map_matrix = np.array([list(line) for line in lines], dtype='object')
        map_matrix = map_matrix == 'O'
        self.map = map_matrix

    
    def render(self):
        _map = np.full_like(self.map, BACKGROUND_CHAR, dtype='object')
        _map[self.map] = FILLED_CHAR

        output_lines = [''.join(row) for row in _map]
        for line in output_lines:
            print(line)

game = ConsoleGame('Map/B.txt')

# %%
game.render()

# %%
