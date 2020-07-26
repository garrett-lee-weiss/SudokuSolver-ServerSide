import pandas as pd
import itertools

class SolvePuzzle:

    def __init__(self, dict, inception = False):
        if inception:
            self.current_puzz_value_dict = dict
        else:
            self.current_puzz_value_dict = self.create_clean_dict(dict)
        self.final_solved_puzzle = None

        self.current_puzz_data_frame, self.current_puzz_value_list = self.convert_to_data_frame()
        self.row_sets, self.col_sets, self.box_sets = self.create_sets()
        self.count_solutions_by_cell, self.potential_solutions_by_cell = self.find_potential_solutions()
        self.is_puzzle_solved = self.solve()

    def create_clean_dict(self, data_from_html):

        # converts dictionary of strings '(x,y)':'#' to tuple(x,y): int(#)

        clean_dict = {}
        for coordinate in data_from_html:
            new_coordinate, new_value = tuple(int(coordinate[i]) for i in (1,4)), None
            if data_from_html[coordinate].isdigit():
                new_value = int(data_from_html[coordinate])
            clean_dict[new_coordinate] = new_value
        return clean_dict

    def convert_to_data_frame(self):

        # Creates data frame from current puzzle values. Data frame is used in creating sets.

        list = [[None] * 9 for i in range(9)]
        for key in self.current_puzz_value_dict:
            list[key[0]][key[1]] = self.current_puzz_value_dict[key]
        return pd.DataFrame(list), list

    def create_sets(self):

        # creates sets of values from current row, column, and box in the puzzle. Discards empty strings

        self.current_puzz_data_frame.fillna('', inplace=True)
        row_dict = {f'row_{i}' : set(self.current_puzz_data_frame.loc[i]) for i in range(9)}
        col_dict = {f'col_{i}': set(self.current_puzz_data_frame[i]) for i in range(9)}
        box_dict = {'box_0': self.convert_to_set(self.current_puzz_data_frame.loc[0:2, 0:2]),
                    'box_1': self.convert_to_set(self.current_puzz_data_frame.loc[0:2, 3:5]),
                    'box_2': self.convert_to_set(self.current_puzz_data_frame.loc[0:2, 6:8]),
                    'box_3': self.convert_to_set(self.current_puzz_data_frame.loc[3:5, 0:2]),
                    'box_4': self.convert_to_set(self.current_puzz_data_frame.loc[3:5, 3:5]),
                    'box_5': self.convert_to_set(self.current_puzz_data_frame.loc[3:5, 6:8]),
                    'box_6': self.convert_to_set(self.current_puzz_data_frame.loc[6:8, 0:2]),
                    'box_7': self.convert_to_set(self.current_puzz_data_frame.loc[6:8, 3:5]),
                    'box_8': self.convert_to_set(self.current_puzz_data_frame.loc[6:8, 6:8])}

        for i in range(9):
            row_dict[f'row_{i}'].discard('')
            col_dict[f'col_{i}'].discard('')
            box_dict[f'box_{i}'].discard('')

        return row_dict, col_dict, box_dict

    def assign_new_values(self,row, column, value):
        # print(f'plugging in {value} into {row, column}')
        self.current_puzz_value_list[row][column] = value
        self.current_puzz_value_dict[(row, column)] = value
        self.current_puzz_data_frame = pd.DataFrame(self.current_puzz_value_list)
        # print(self.data_frame)
        self.row_sets, self.col_sets, self.box_sets = self.create_sets()
        self.count_solutions_by_cell, self.potential_solutions_by_cell = self.find_potential_solutions()

    def find_potential_solutions(self):

        # finds differences in every row, column, and box set compared to the complete set to find values missing from the set.
        # Differences are overlapped to determine potetial values for every cell.

        complete_set = {i for i in range(1, 10)}
        count_dict, value_dict = {}, {}
        for row in range(0,9):
            for column in range(0,9):
                row_diff = complete_set.difference(self.row_sets[f'row_{row}'])
                col_diff = complete_set.difference(self.col_sets[f'col_{column}'])
                box_diff = complete_set.difference(self.box_sets[self.get_box_set(row, column)])
                overlap = row_diff.intersection(col_diff.intersection(box_diff))
                if not self.current_puzz_value_list[row][column]:
                    value_dict[(row, column)] = overlap
                    count_dict[(row, column)] = len(overlap)

        return count_dict, value_dict

    def solve(self):

        # loops through all cells & the corresponding counts of potential solutions.
        # If the minumum num of solutions in all cells is Zero, the puzzle cannot be solved.
        # If the minimum num of solutions in all cells is 1, plug in those values & re-loop.
        # If the minimum num of solutions in all cells is two, plug the value into a dictionary( copied from current value dict)
        # and instantiate a new SolvePuzzle class with that dictionary.

        solved, i = False, 0
        while not solved and i < 100:
            small = min(set([self.count_solutions_by_cell[i] for i in self.count_solutions_by_cell]))
            if small == 0:
                return False
            elif small == 1:
                for item in self.count_solutions_by_cell:
                    if self.count_solutions_by_cell[item] == 1:
                        self.assign_new_values(item[0], item[1], self.potential_solutions_by_cell[item].pop())
            else:
                for item in self.count_solutions_by_cell:
                    if self.count_solutions_by_cell[item] == 2:
                        value1, value2 = self.potential_solutions_by_cell[item].pop(), self.potential_solutions_by_cell[item].pop()
                        for i in (value1, value2):
                            puzzle_copy = self.current_puzz_value_dict.copy()
                            puzzle_copy[item] = i
                            trial = SolvePuzzle(puzzle_copy, inception=True)
                            if trial.is_puzzle_solved:
                                self.final_solved_puzzle = trial.final_solved_puzzle
                                return True
                        return trial.is_puzzle_solved
            i += 1
            solved = self.is_puzzle_solved()
        if solved:
            self.final_solved_puzzle = self.current_puzz_value_list
        return solved

    def is_puzzle_solved(self):
        for row in range(0,9):
            for column in range(0,9):
                if self.current_puzz_value_list[row][column] is None:
                    return False
        return True

    @staticmethod
    def get_box_set(row, column):
        list = [
            ['box_0', 'box_0', 'box_0', 'box_1', 'box_1', 'box_1', 'box_2', 'box_2', 'box_2'],
            ['box_0', 'box_0', 'box_0', 'box_1', 'box_1', 'box_1', 'box_2', 'box_2', 'box_2'],
            ['box_0', 'box_0', 'box_0', 'box_1', 'box_1', 'box_1', 'box_2', 'box_2', 'box_2'],
            ['box_3', 'box_3', 'box_3', 'box_4', 'box_4', 'box_4', 'box_5', 'box_5', 'box_5'],
            ['box_3', 'box_3', 'box_3', 'box_4', 'box_4', 'box_4', 'box_5', 'box_5', 'box_5'],
            ['box_3', 'box_3', 'box_3', 'box_4', 'box_4', 'box_4', 'box_5', 'box_5', 'box_5'],
            ['box_6', 'box_6', 'box_6', 'box_7', 'box_7', 'box_7', 'box_8', 'box_8', 'box_8'],
            ['box_6', 'box_6', 'box_6', 'box_7', 'box_7', 'box_7', 'box_8', 'box_8', 'box_8'],
            ['box_6', 'box_6', 'box_6', 'box_7', 'box_7', 'box_7', 'box_8', 'box_8', 'box_8'],
        ]
        return list[row][column]

    @staticmethod
    def convert_to_set(array):
        list = []
        for i in array.values:
            list.extend(i)
        return set(list)
