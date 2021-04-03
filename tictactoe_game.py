import random
from typing import List, Tuple, Dict

from my_enums import SquareStates, GameStates


class TicTacToeGame:
    def __init__(self):
        self.Screen = [[SquareStates.EMPTY, SquareStates.EMPTY, SquareStates.EMPTY],
                       [SquareStates.EMPTY, SquareStates.EMPTY, SquareStates.EMPTY],
                       [SquareStates.EMPTY, SquareStates.EMPTY, SquareStates.EMPTY]]

    def do_turn_move(self, move: Tuple[int, int]) -> GameStates:
        if not self.valid_move(move):
            return GameStates.INVALID_SCREEN

        self.register_move(move, SquareStates.X)

        return self.proccess_game()

    def do_turn_screen(self, screen_matrix, translation_dict) -> GameStates:
        screen = self.matrix_to_screen(screen_matrix, translation_dict)

        if not self.is_screen_valid(screen, self.Screen):
            return GameStates.INVALID_SCREEN

        self.update_screen(screen)

        return self.proccess_game()

    def proccess_game(self) -> GameStates:
        if self.did_sign_win(SquareStates.X):
            return GameStates.XWIN

        draw = self.is_draw()

        if not draw:
            self.move()

        sign = self.winning_sign()

        if sign == SquareStates.X:
            return GameStates.XWIN

        elif sign == SquareStates.O:
            return GameStates.OWIN

        elif draw:
            return GameStates.DRAW

        return GameStates.GOING_ON

    def update_screen(self, screen: List[List[SquareStates]]):
        self.Screen = screen

    def register_move(self, move: Tuple[int, int], sign: SquareStates):
        self.Screen[move[0]][move[1]] = sign

    def matrix_to_screen(self, screen_matrix: List, translation_dict: Dict) -> bool:
        pass

    def valid_move(self, move: Tuple[int, int]) -> bool:
        return self.Screen[move[0]][move[1]] == SquareStates.EMPTY

    def move(self):
        available_moves = self.get_available_moves()

        move = random.choice(available_moves)

        self.register_move(move, SquareStates.O)

    def get_available_moves(self) -> List[Tuple[int, int]]:
        available_moves = []

        for i in range(len(self.Screen)):
            for j in range(len(self.Screen[i])):
                if self.Screen[i][j] == SquareStates.EMPTY:
                    available_moves.append((i, j))

        return available_moves

    def is_draw(self) -> bool:
        return len(self.get_available_moves()) == 0

    def winning_sign(self) -> SquareStates:
        for sign in [SquareStates.X, SquareStates.O]:
            if self.did_sign_win(sign):
                return sign

        return SquareStates.EMPTY

    def did_sign_win(self, sign: SquareStates) -> bool:
        row_wins = [True, True, True]
        column_wins = [True, True, True]
        diagonal_wins = [True, True]

        for i in range(len(self.Screen)):
            for j in range(len(self.Screen[i])):
                if self.Screen[i][j] == sign:
                    continue

                row_wins[i] = False
                column_wins[j] = False

                if i == j:
                    diagonal_wins[0] = False
                    if i == 1:
                        diagonal_wins[1] = False

                elif abs(i - j) == len(self.Screen) - 1:
                    diagonal_wins[1] = False

        wins = row_wins + column_wins + diagonal_wins

        for win in wins:
            if win:
                return True

        return False

    def is_screen_valid(self,
                        new_screen: List[List[SquareStates]],
                        old_screen: List[List[SquareStates]]) -> bool:
        differences = self.generate_screen_differences(new_screen, old_screen)
        return self.are_differences_valid(differences)

    def are_differences_valid(self, differences: List[Tuple[SquareStates, SquareStates]]) -> bool:
        if len(differences) != 1:
            return False

        for dif in differences:
            if dif[0] == SquareStates.O:
                return False

            if dif[1] != SquareStates.EMPTY:
                return False

        return True

    def generate_screen_differences(self,
                                    new_screen: List[List[SquareStates]],
                                    old_screen: List[List[SquareStates]]):
        differences = []

        for i in range(len(new_screen)):
            for j in range(len(new_screen[i])):
                new_square = new_screen[i][j]
                old_square = old_screen[i][j]

                if new_square != old_square:
                    differences.append((new_square, old_square))

        return differences

    def screen_to_matrix(self, translation_dict: Dict) -> List[List]:
        screen = []

        for i in range(len(self.Screen)):
            screen.append([])
            for j in range(len(self.Screen[i])):
                square = self.Screen[i][j]

                screen[i].append(
                    (list(translation_dict.keys())
                    [list(translation_dict.values()).index(square)])[0])

        return screen

    def matrix_to_screen(self,
                         screen_matrix: List[List],
                         translation_dict: Dict) -> List[List[SquareStates]]:
        screen = []

        for i in range(len(screen_matrix)):
            screen.append([])
            for j in range(len(screen_matrix[i])):
                screen[i].append(translation_dict[screen_matrix[i][j]])

        return screen