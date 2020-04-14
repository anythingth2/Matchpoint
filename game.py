# %%
import seaborn as sns
from tqdm import tqdm, trange
import numpy as np
import time
from fractions import Fraction
# %%
BACKGROUND_CHAR = ' '
FILLED_CHAR = 'O'


class ConsoleGame:

    def __init__(self, map_path):
        self.map_path = map_path
        self.answer_map = self.load_map(self.map_path)
        self.map = np.full_like(self.answer_map, False)
        self.row_counts = self.count_neighbours(
            self.answer_map, count_value=True)
        self.column_counts = self.count_neighbours(
            self.answer_map.T, count_value=True)

    @classmethod
    def from_game(cls, game):
        new_game = cls(game.map_path)
        new_game.map = game.map.copy()
        return new_game

    def load_map(self, map_path):
        with open(map_path, 'r') as f:
            lines = f.read().splitlines()
        map_matrix = np.array([np.array(list(line), dtype='object')
                               for line in lines], dtype='object')
        map_matrix = map_matrix == 'O'
        return map_matrix

    # Print answer map
    def render_answer(self):
        _map = np.full_like(self.answer_map, BACKGROUND_CHAR, dtype='object')
        _map[self.answer_map] = FILLED_CHAR

        map_lines = []
        for i, row in enumerate(_map):
            order = str(i).rjust(2, ' ')
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

    def check_rule(self, input_neighbours, label_neighbours):
        if len(input_neighbours) > len(label_neighbours):
            return False

        for i in range(len(input_neighbours)):
            if input_neighbours[i] > label_neighbours[i]:
                return False
        return True

    # Check position (x,y) is paintable
    # return Boolean
    def is_paintable(self, x, y):
        _map = self.map.copy()
        _map[y, x] = True
        input_row_neighbours = self.count_neighbour_vector(
            _map[y], count_value=True)
        input_column_neighbours = self.count_neighbour_vector(
            _map[:, x], count_value=True)
        return self.check_rule(input_row_neighbours, self.row_counts[y])\
            and self.check_rule(input_column_neighbours, self.column_counts[x])

    # Try to paint at (x,y)
    # return boolean of result of paint

    # If inplace=False then will paint on a copy of game object and return it
    # (Not modify current object)
    def paint(self, x, y, inplace=True):
        if inplace:
            game = self
        else:
            game = ConsoleGame.from_game(self)

        paintable = game.is_paintable(x, y)

        if paintable:
            game.map[y, x] = True

        if inplace:
            return paintable
        else:
            return paintable, game

    # Erase painted cell at (x,y)

    # If inplace=False then will erase on a copy of game object and return it
    # (Not modify current object)
    def erase(self, x, y, inplace=True):
        if inplace:
            self.map[y, x] = False
        else:
            game = ConsoleGame.from_game(self)
            game.map[y, x] = False
            return game

    # Clear map
    def clear(self):
        self.map = np.full_like(self.answer_map, False)

    # Check result of game
    # return boolean of correction
    def check_result(self):
        # return np.all(self.answer_map == self.map)
        painted_row_counts = self.count_neighbours(
            self.map, count_value=True)
        # row_result = all([self.check_rule(painted_row_counts[i], self.row_counts[i])
        #                   for i in range(len(painted_row_counts))])
        row_result = painted_row_counts == self.row_counts
        painted_column_counts = self.count_neighbours(
            self.map.T, count_value=True)
        # column_result = all([self.check_rule(painted_column_counts[i], self.column_counts[i])
        #                      for i in range(len(painted_column_counts))])
        column_result = painted_column_counts == self.column_counts
        return row_result and column_result

    # Print current map

    def render(self):
        _map = np.full_like(self.map, BACKGROUND_CHAR, dtype='object')
        _map[self.map] = FILLED_CHAR

        map_lines = []
        map_lines += [' '*3 + ''.join([str(i) for i in range(_map.shape[1])])]
        map_lines += [' '*3 + '_'*_map.shape[1]]
        for i, row in enumerate(_map):
            order = str(i).rjust(2, ' ')
            map_text = ''.join(row)
            row_neighbour_text = ' '.join(
                [str(count) for count in self.row_counts[i]])
            line = f"{order}|{map_text}|{row_neighbour_text}"
            map_lines.append(line)
        column_counts = [[str(count) for count in neighbors]
                         for neighbors in self.column_counts]
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

    @property
    def count_painted_cell(self):
        return np.sum(self.map)

    # Count number of painted cell on answer map
    @property
    def count_answer_cell(self):
        return np.sum(self.answer_map)

    # Return List of answer cell of this problem
    @property
    def answer_path(self):
        return np.argwhere(self.answer_map)[:, ::-1]

    # return height, width of answer map
    @property
    def shape(self):
        return self.answer_map.shape


# %%
# %%
game: ConsoleGame = ConsoleGame('map/test.txt')
# game: ConsoleGame = ConsoleGame('map/B.txt')

# %%


def search_pattern(vector, counts):
    def criteria(_vector):
        return game.count_neighbour_vector(_vector, True) == counts
    blank_idxes = np.argwhere(~vector).squeeze(axis=1)

    patterns = []
    for idx in blank_idxes:
        painted_vector = vector.copy()
        painted_vector[idx] = True
        founded_patterns = search_pattern(painted_vector, counts)

        if founded_patterns is not None:

            patterns.extend(founded_patterns)

    if len(patterns) == 0 and criteria(vector):
        patterns.append(vector)
    return patterns


def find_patterns(vector, counts):
    patterns = search_pattern(
        vector, counts=counts)
    patterns = np.unique(patterns, axis=0)
    probs = patterns.sum(
        axis=0) / len(patterns)
    return patterns, probs


prob_table = np.zeros(game.shape, dtype=np.float)


horizontal_pattern_table = []
horizontal_prob_table = []
for vector, counts in tqdm(zip(game.map, game.row_counts)):
    patterns, probs = find_patterns(vector, counts)
    horizontal_pattern_table.append(patterns)
    horizontal_prob_table.append(probs)
horizontal_prob_table = np.array(horizontal_prob_table)

vertical_pattern_table = []
vertical_prob_table = []
for vector, counts in tqdm(zip(game.map.T, game.column_counts)):
    patterns, probs = find_patterns(vector, counts)
    vertical_pattern_table.append(patterns)
    vertical_prob_table.append(probs)
vertical_prob_table = np.array(vertical_prob_table)
# %%
for y in range(game.map.shape[0]):
    for x in range(game.map.shape[1]):
        # vector = game.map[y].copy()
        # counts = game.row_counts[y]
        # horizontal_patterns = search_pattern(
        #     vector, counts=counts)
        # horizontal_patterns = np.unique(horizontal_patterns, axis=0)
        # horizontal_probs = horizontal_patterns.sum(
        #     axis=0) / len(horizontal_patterns)

        # vertial_vector = game.map[:, x].copy()
        # vertical_counts = game.column_counts[x]
        # vertical_patterns = search_pattern(
        #     vertial_vector, counts=vertical_counts)
        # vertical_patterns = np.unique(vertical_patterns, axis=0)
        # vertical_probs = vertical_patterns.sum(axis=0) / len(vertical_patterns)

        # prob_table[y, x] = (vertical_probs[y] * horizontal_probs[x])
        prob_table[y, x] = (vertical_prob_table[x, y] *
                            horizontal_prob_table[y, x])
# print(patterns)
# %%
print()
game.render_answer()

# %%


# %%
def float2fraction(v):
    fraction = Fraction(v).limit_denominator()
    return f'{fraction.numerator}/{fraction.denominator}'

# %%

# %%

sns.heatmap(prob_table, annot=np.vectorize(float2fraction)( prob_table), fmt='')
# %%
