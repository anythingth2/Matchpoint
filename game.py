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

        map_lines = []
        for i, row in enumerate(_map):
            order = str(i+1).rjust(2, ' ')
            map_text = ''.join(row)
            row_neighbour_text = ' '.join(
                self.count_neighbour_vector(row, FILLED_CHAR, is_output_str=True))
            line = f"{order}|{map_text}|{row_neighbour_text}"
            map_lines.append(line)

        column_counts = self.count_neighbours(
            _map.T, count_value=FILLED_CHAR, is_output_str=True)
        max_count_length = max([len(neighbour_counts)
                                for neighbour_counts in column_counts])
        column_counts = [column + [' '] *
                         (max_count_length-len(column)) for column in column_counts]
        column_counts = np.array(column_counts).T
        column_lines = [' '*3 + ''.join(column) for column in column_counts]

        map_lines += [' '*3 + '-'*_map.shape[1]]
        map_lines += column_lines
        
        for line in map_lines:
            print(line)

    def count_neighbour_vector(self, vector, count_value, is_output_str=False):
        vector = list(vector)
        neighbour_counts = []
        count = 0
        for v in vector:
            if v == count_value:
                count += 1
            else:
                if count > 0:
                    neighbour_counts.append(count)
                    count = 0
        if count > 0:
            neighbour_counts.append(count)
        if is_output_str:
            neighbour_counts = [str(count) for count in neighbour_counts]
        return neighbour_counts

    def count_neighbours(self, _map, **kwargs):
        return [self.count_neighbour_vector(vector, **kwargs) for vector in _map]


game = ConsoleGame('Map/B.txt')
game.render()
