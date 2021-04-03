from zoombot.core import Bot, Message
from tictactoe_command import TicTacToeCommand
from tictactoe_manager import TicTacToeManager


class MyBot(Bot):
    TICTACTOE_COMMAND = TicTacToeCommand(TicTacToeManager())

    def __init__(self, client_id, client_secret, bot_jid, verification_token):
        super().__init__(client_id=client_id,
                         client_secret=client_secret,
                         bot_jid=bot_jid,
                         verification_token =verification_token)
        self.command_dict = {"tictactoe": self.tictactoe}

    async def on_message(self, message: Message):
        split_msg = message.content.split(" ")
        command_text = split_msg[0]

        choosen_command = self.command_dict[command_text]

        await choosen_command(message)

    async def tictactoe(self, message: Message):
        await self.TICTACTOE_COMMAND.run(message)
