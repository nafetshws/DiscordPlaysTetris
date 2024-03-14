import discord
from discord.ext import commands
from TetrisBot import TetrisBot
import json
import os

def load_token():
    try:
        with open(os.path.dirname(__file__) + "/../discord_auth.json", "r") as f:
            return json.load(f)["TOKEN"]
    except:
        raise Exception("You need a file called discord_auth.json with a field TOKEN!")

class TetrisBotForDiscord(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.default_text_channel = None
        self.command_prefix = command_prefix
        self.tetris_bot = None
        self.game_instance_running = False
        self.add_commands()
 
    async def on_ready(self):
        print("Hello {}".format(self.user.name))

    async def write(self, ctx, msg):
        if self.default_text_channel is None:
            await ctx.send(msg)
        else:
            await self.default_text_channel.send(msg) 

    async def send_current_board(self):
        with open(os.path.dirname(__file__) + "/../res/current_board.png", "rb") as f:
            image = discord.File(f)
            await self.default_text_channel.send(file=image)

    def add_commands(self):
        @self.command(name="default")
        async def set_default_text_channel(ctx, channel : discord.TextChannel):
            self.default_text_channel = channel

            up = ":arrow_up:"
            down = ":arrow_down:"
            left = ":arrow_left:"
            right = ":arrow_right:"
            rotate = ":arrows_clockwise:"

            DEFAULT_CHANNEL_MSG = "This is now the default text channel of <@{}>\nHow to engange with the bot react with the following Emojis or use the following commands:\n\n**Start a new game**: {}start\n**Move left**: {}\n**Move right**: {}\n**Drop down**: {}\n**Rotate (clockwise)**: {}".format(self.user.id, self.command_prefix, left, right, down, rotate)
            message = await self.default_text_channel.send(DEFAULT_CHANNEL_MSG)
            await message.pin()

        @self.command("start")
        async def start_game(ctx):
            if not self.game_instance_running:
                self.write("There is already a running instance of the game!")
                return                                

            self.game_instance_running = True
            self.tetris_bot = TetrisBot()
            self.tetris_bot.start_game()
            await self.send_current_board()

if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = TetrisBotForDiscord(command_prefix="!", intents=intents)
    bot.run(load_token())