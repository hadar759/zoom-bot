from typing import Dict, List

from my_enums import SquareStates, GameStates
from zoombot.core import Message

from tictactoe_game import TicTacToeGame
from tictactoe_manager import TicTacToeManager


class TicTacToeCommand:
    WIN_TEXT = "You won!!"
    LOSE_TEXT = "You lost :("
    INVALID_TEXT = "Invalid screen"
    DRAW_TEXT = "Game drawn"
    BLANK_SCREEN = "⬜⬜⬜\r⬜⬜⬜\r⬜⬜⬜"

    def __init__(self, manager: TicTacToeManager):
        self.translation_dict: Dict[chr, SquareStates] = {
            '❌': SquareStates.X,
            '⭕': SquareStates.O,
            '⬜': SquareStates.EMPTY
        }
        self.manager = manager

    async def run(self, message: Message):
        split_msg = message.content.split(" ")

        if split_msg[1] == "start":
            await message.reply(head=self.start_text(message))

        elif split_msg[1] == "stop":
            await message.reply(head=self.stop_text(message))

        elif split_msg[1] == "help":
            await message.reply(head=self.help_text())

        elif split_msg[1] == "blank":
            await message.reply(head=self.BLANK_SCREEN)

        else:
            game = self.manager.get_game(message)

            if game is not None:
                for text in self.turn_text(message, game):
                    await message.reply(head=text)
            else:
                await message.reply(head="No game currently running")

    def start_text(self, message: Message) -> str:
        game_started = self.manager.add_game(message)

        if not game_started:
            return "Game already taking place"

        game = self.manager.get_game(message)
        screen = game.screen_to_matrix(self.translation_dict)

        return self.matrix_to_string_non_emoji(screen)

    def stop_text(self, message: Message) -> str:
        game_stopped = self.manager.remove_game(message)

        if not game_stopped:
            return "No game currently taking place"

        return "Game stopped"

    def help_text(self) -> str:
        return """Each turn the bot will send a tic tac toe screen.
Place an ❌ wherever you want to play and send the screen.
Make sure to avoid spaces and other unnecessary characters.
First to complete a row, column, or diagonal wins."""

    def turn_text(self, message: Message, game: TicTacToeGame):
        content = message.content
        content = content.replace("tictactoe ", "")

        if len(content) == 2:
            move = (ord(content[0]) - ord('a'), int(content[1]) - 1)
            game_state = game.do_turn_move(move)
            screen_matrix = game.screen_to_matrix(self.translation_dict)
            final_screen_string = self.matrix_to_string_non_emoji(screen_matrix)

        elif len(content) == 12:
            content = content.replace("\r", "")
            screen = self.string_to_matrix(content)

            game_state = game.do_turn_screen(screen, self.translation_dict)
            screen_matrix = game.screen_to_matrix(self.translation_dict)
            final_screen_string = self.matrix_to_string_emoji(screen_matrix)

        else:
            yield "Invalid move"
            return

        if game_state == GameStates.INVALID_SCREEN:
            yield self.INVALID_TEXT
            return

        elif game_state == GameStates.XWIN:
            self.manager.remove_game(message)
            yield final_screen_string
            yield self.WIN_TEXT
            return

        elif game_state == GameStates.OWIN:
            self.manager.remove_game(message)
            yield final_screen_string
            yield self.LOSE_TEXT
            return

        elif game_state == GameStates.DRAW:
            self.manager.remove_game(message)
            yield self.DRAW_TEXT
            return

        yield final_screen_string

    def matrix_to_string_emoji(self, matrix: List[List[chr]]) -> str:
        str = ""

        for arr in matrix:
            for char in arr:
                str += char

            str += "\r"

        return str

    def matrix_to_string_non_emoji(self, matrix: List[List[chr]]) -> str:
        str = "    1  2  3\n"
        counter = 0

        for arr in matrix:
            str += chr(ord("a") + counter) + "    "
            counter += 1

            for char in arr:
                str += char

            str += "\r"

        return str

    def string_to_matrix(self, string: str):
        string = string.replace("\r", "")

        matrix = []

        for i in range(3):
            matrix.append([])
            for j in range(3):
                matrix[i].append(string[i * 3 + j])

        return matrix
