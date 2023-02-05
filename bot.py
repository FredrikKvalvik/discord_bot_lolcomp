import discord
from discord.ext import commands
import responses

from dotenv import load_dotenv
import os

load_dotenv()

SECRET = os.getenv("SECRET")

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.event
    async def on_ready():
        print(f'Bot is now running!')

    @bot.hybrid_group(fallback="help")
    async def lolcomp(ctx):
        res = responses.help_text
        await ctx.send(res)

    @lolcomp.command()
    async def challenges(ctx, challenge=None):
        if challenge is None:
            res = responses.challenges_response()
        else:
            res = responses.challenge_response(challenge)

        await ctx.send(res)

    @lolcomp.command()
    async def champ(ctx, champion=None):
        if champion is None:
            res = f"write the command `lolcomp champ [champ_name]` to get available challenges"
        else:
            res = responses.champ_challenges_response(champion)
        await ctx.send(res)

    bot.run(SECRET)
