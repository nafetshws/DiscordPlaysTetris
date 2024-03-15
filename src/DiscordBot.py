import discord
from discord.ext import commands
from TetrisBot import TetrisBot
import json
import os
import time
import asyncio
import emoji 

def load_token():
    try:
        with open(os.path.dirname(__file__) + "/../discord_auth.json", "r") as f:
            return json.load(f)["TOKEN"]
    except:
        raise Exception("You need a file called discord_auth.json with a field TOKEN!")

class TetrisBotForDiscord(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.default_text_channel : discord.TextChannel = None
        self.command_prefix = command_prefix
        self.tetris_bot = None
        self.game_instance_running = False

        #emojis
        self.down = ":down_arrow:"
        self.left = ":left_arrow:"
        self.right = ":right_arrow:"
        self.rotate = ":arrows_clockwise:"

        self.add_commands()
 
    async def on_ready(self):
        print("Hello {}".format(self.user.name))

    async def on_reaction_add(self, reaction : discord.Reaction, user : discord.User):
        pass
        #print(user.name)
        #print(reaction.emoji)

    async def write(self, ctx, msg):
        if self.default_text_channel is None:
            await ctx.send(msg)
        else:
            await self.default_text_channel.send(msg) 

    async def send_current_board(self):
        with open(os.path.dirname(__file__) + "/../res/current_board.png", "rb") as f:
            image = discord.File(f)
            return await self.default_text_channel.send(file=image)

    #returns a dict with the amount of certain emojis
    async def count_reactions(self, ctx, msg_id):
        reaction_count = {f"{self.left}": 0,
                          f"{self.right}": 0,
                          f"{self.down}": 0,
                          f"{self.rotate}": 0}
        #fetch message from discord (not from cache, because reactions aren't added yet)
        msg : discord.Message = await ctx.fetch_message(msg_id) 

        for reaction in msg.reactions:
            #get string representation of emoji 
            e = emoji.demojize(reaction.emoji)
            #the emoji module and discord use different names for the emoji. Conversion is necessary.
            if "clockwise" in e:
                e = self.rotate

            #increment emoji count in dict
            if e in reaction_count:
                reaction_count[e] += 1

        return reaction_count

    def add_commands(self):
        @self.command(name="default")
        async def set_default_text_channel(ctx, channel : discord.TextChannel):
            self.default_text_channel = channel


            DEFAULT_CHANNEL_MSG = "This is now the default text channel of <@{}>\nHow to engange with the bot react with the following Emojis or use the following commands:\n\n**Start a new game**: {}start\n**Move left**: {}\n**Move right**: {}\n**Drop down**: {}\n**Rotate (clockwise)**: {}".format(self.user.id, self.command_prefix, self.left, self.right, self.down, self.rotate)
            message = await self.default_text_channel.send(DEFAULT_CHANNEL_MSG)
            await message.pin()

        @self.command("start")
        async def start_game(ctx):
            if self.game_instance_running:
                await self.write(ctx, "There is already a running instance of the game!")
                return                                

            self.game_instance_running = True
            self.tetris_bot = TetrisBot()
            self.tetris_bot.start_game()
            msg = await self.send_current_board()

            #wait 30s
            await asyncio.sleep(10)

            await self.count_reactions(ctx, msg.id)



if __name__ == "__main__":
    intents = discord.Intents.all()
    bot = TetrisBotForDiscord(command_prefix="!", intents=intents)
    bot.run(load_token())