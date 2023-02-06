import discord
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents = discord.Intents.default())
TOKEN = "MTA2MjkxNjU2NDMzNDE0OTczNA.G6QQ23.evo2wsorKEKq-4lXwHQKEwMHk7IbROV1X0DfZs"
@bot.event
async def on_ready():
    print("봇 실행됨")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e :
        print(e)

@bot.tree.command(name="출석체크")
async def check(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.display_name} 출석했습니다.\n(여기날짜)")
    #user.name -> 실제 사용자 이름
    #user.display_name -> 서버에서 설정한 별명

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")

bot.run(TOKEN)
