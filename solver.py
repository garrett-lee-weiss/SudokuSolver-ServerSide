import pandas as pd
import itertools

class solve_puzzle:

    def __init__(self, dict, inception = False):
        if inception:
            self.form_dict = dict
        else:
            self.form_dict = self.create_clean_dict(dict)
        self.winning_list = None
        self.full_set = {i for i in range(1, 10)}
        self.data_frame, self.form_list = self.convert_to_data_frame()
        self.row_sets, self.col_sets, self.box_sets = self.create_sets()
        self.count_dict, self.value_dict = self.create_value_list()
        self.solved = self.solve()

    def create_clean_dict(self, form):
        form_dict = {}
        for coordinate in form:
            new_coordinate, new_value = tuple(int(coordinate[i]) for i in (1,4)), None
            if form[coordinate].isdigit():
                new_value = int(form[coordinate])
            form_dict[new_coordinate] = new_value
        return form_dict

    def convert_to_data_frame(self):
        list = [[None] * 9 for i in range(9)]
        for key in self.form_dict:
            list[key[0]][key[1]] = self.form_dict[key]
        return pd.DataFrame(list), list

    def create_sets(self):
        self.data_frame.fillna('', inplace=True)
        row_dict = {f'row_{i}' : set(self.data_frame.loc[i]) for i in range(9)}
        col_dict = {f'col_{i}': set(self.data_frame[i]) for i in range(9)}
        box_dict = {}

        box_dict['box_0'] = self.return_set(self.data_frame.loc[0:2, 0:2])
        box_dict['box_1'] = self.return_set(self.data_frame.loc[0:2, 3:5])
        box_dict['box_2'] = self.return_set(self.data_frame.loc[0:2, 6:8])
        box_dict['box_3'] = self.return_set(self.data_frame.loc[3:5, 0:2])
        box_dict['box_4'] = self.return_set(self.data_frame.loc[3:5, 3:5])
        box_dict['box_5'] = self.return_set(self.data_frame.loc[3:5, 6:8])
        box_dict['box_6'] = self.return_set(self.data_frame.loc[6:8, 0:2])
        box_dict['box_7'] = self.return_set(self.data_frame.loc[6:8, 3:5])
        box_dict['box_8'] = self.return_set(self.data_frame.loc[6:8, 6:8])

        for i in range(9):
            row_dict[f'row_{i}'].discard('')
            col_dict[f'col_{i}'].discard('')
            box_dict[f'box_{i}'].discard('')

        return row_dict, col_dict, box_dict

    def assign_new_values(self,row, column, value):
        print(f'plugging in {value} into {row, column}')
        self.form_list[row][column] = value
        self.form_dict[(row, column)] = value
        self.data_frame = pd.DataFrame(self.form_list)
        # print(self.data_frame)
        self.row_sets, self.col_sets, self.box_sets = self.create_sets()
        self.count_dict, self.value_dict = self.create_value_list()

    def create_value_list(self):
        count_dict, value_dict = {}, {}
        for row in range(0,9):
            for column in range(0,9):
                r = self.full_set.difference(self.row_sets[f'row_{row}'])
                c = self.full_set.difference(self.col_sets[f'col_{column}'])
                b = self.full_set.difference(self.box_sets[self.get_box_set(row, column)])
                d = r.intersection(c.intersection(b))
                if not self.form_list[row][column]:
                    value_dict[(row, column)] = d
                    count_dict[(row, column)] = len(d)

        return count_dict, value_dict

    def solve(self):
        solved, i = False, 0
        print(f'--Inside {self}--')

        while not solved and i < 100:
            small = min(set([self.count_dict[i] for i in self.count_dict]))
            if small == 0:
                print(f'we are out of options: {small}')
                return False

            elif small == 1:
                print(f'We have singles {small}')
                for item in self.count_dict:
                    if self.count_dict[item] == 1:
                        self.assign_new_values(item[0], item[1], self.value_dict[item].pop())
            else:
                print(f'We have doubles {small}')
                for item in self.count_dict:
                        if self.count_dict[item] == 2:
                            # print(f'{item} : {self.count_dict[item]} | {self.value_dict[item]}')
                            value1, value2 = self.value_dict[item].pop(), self.value_dict[item].pop()
                            for i in (value1, value2):
                                cop = self.form_dict.copy()
                                cop[item] = i
                                print(f'****Begining Trial****{self}')
                                trial = solve_puzzle(cop, inception=True)
                                print(f'****ENDING Trial****{self}')
                                if trial.solved:
                                    solved = True
                                    self.winning_list = trial.winning_list
                                    return True
                            return trial.solved
                return solved
            i += 1
            solved = self.solve_check()
        print(f'number of loops: {i} | solved? {solved}')
        if self.solve_check():
            print(f'----WE HAVE SOLVED THE PUZZLE---{self}')
            print(self.data_frame)
            self.winning_list = self.form_list
            print(self.winning_list)
            return True
        else:
            print('Puzzle has NOT been solved.')
            return False


    def solve_check(self):
        for row in range(0,9):
            for column in range(0,9):
                if self.form_list[row][column] is None:
                    print(f'NOT SOLVED | {row, column} is not filled in.')
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
    def return_set(array):
        list = []
        for i in array.values:
            list.extend(i)
        return set(list)
