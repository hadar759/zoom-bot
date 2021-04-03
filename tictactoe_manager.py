from typing import Dict

from zoombot.core import Message

from tictactoe_game import TicTacToeGame


class TicTacToeManager:
    def __init__(self):
        self.players: Dict[str, TicTacToeGame] = {}

    def add_game(self, message: Message) -> bool:
        game = self.get_game(message)
        if game is not None:
            return False

        self.players[message.account_id] = TicTacToeGame()

        return True

    def remove_game(self, message: Message) -> bool:
        game = self.get_game(message)

        if game is None:
            return False

        self.players.pop(message.account_id)

        return True

    def get_game(self, message: Message) -> TicTacToeGame:
        return self.players.get(message.account_id)
