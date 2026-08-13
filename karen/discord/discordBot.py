import discord
from discord.ext import commands

# causes ApplyAction functions to load
from karen.state.state import State
from karen.actions.basicActions import *
from karen.actions.earlyCancels import *
from karen.actions.movestacks import *

# getting environment variables
import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# basic discord setup
intents: discord.Intents = discord.Intents.default()
intents.guild_messages = True
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# prints to console on successful launch
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    try:
        await bot.tree.sync()
        print(f"successfully connected to {len(bot.guilds)} servers")
    except Exception as e:
        print(e)

# setting up commands
from karen.discord.eval import eval as evalCommand
from karen.discord.help import help as helpCommand

@bot.command()
async def eval(ctx: commands.Context, *arr: str):
    await evalCommand(ctx, *arr)

@bot.command()
async def comp(ctx: commands.Context, *arr: str):
    await evalCommand(ctx, *arr)

@bot.command
async def help(ctx: commands.Context, *arr: str):
    helpCommand(ctx, *arr)

# run bot
bot.run(BOT_TOKEN)