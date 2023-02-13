import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime
import sqlite3

bot = commands.Bot(command_prefix="!", intents = discord.Intents.default())
TOKEN = "MTA2MzMwMTQxODMzNDgxNDIxOA.G8yHtQ.iGjiejod5DCknlQHAQnyS2xjcTEFetyh1gQ2es"

@bot.event
async def on_ready():
    print("봇 실행됨")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e :
        print(e)

@bot.tree.command(name="출석체크")
async def att(interaction: discord.Interaction):
    date_rec = datetime.today().strftime('%Y-%m-%d')
    time_rec = datetime.today().strftime('%H:%M')

    await interaction.response.send_message(f"{interaction.user.display_name} 출석했습니다.\n{date_rec} {time_rec}")
    #user.name -> 실제 사용자 이름
    #user.display_name -> 서버에서 설정한 별명

    conn = sqlite3.connect('Attendance.db')
    cur = conn.cursor()
    sql1 = "CREATE TABLE IF NOT EXISTS attTBL(name text,date text, time text);"
    sql2 = "INSERT INTO attTBL(name,date,text) values (?,?);"
    cur.execute(sql1)
    cur.execute(sql2, (interaction.user.display_name, date_rec, time_rec))
    conn.commit()
    cur.close()

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{thing_to_say}'")

@bot.tree.command(name="db조회")
async def db(interaction: discord.Interaction):
    conn = sqlite3.connect('Attendance.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM attTBL')
    lrow=[]
    for row in cur:
        lrow.append(list(row))
    lrow.sort()
    await interaction.response.send_message(f"{lrow}")
    cur.close()

@bot.tree.command(name="resetdb")
async def reset(interaction:discord.Interaction):
    conn = sqlite3.connect('Attendance.db')
    cur = conn.cursor()
    sql3 = "DROP TABLE IF EXISTS attTBL"
    cur.execute(sql3)
    cur.close()
    await interaction.response.send_message(f"초기화")

@bot.tree.command(name="check")
async def check(interaction:discord.Interaction):
    conn = sqlite3.connect('Attendance.db')
    cur = conn.cursor()
    sql4 = "SELECT name FROM attTBL"
    cur.execute(sql4)
    lrow=[]
    for row in cur:
        lrow.append(list(row))
    lrow.sort()
    members=['김주미', '양진']
    for i in lrow:
        members.remove(i)
    await interaction.response.send_message(f"출석하지 않은 명단 : {members}")
    cur.close()

bot.run(TOKEN)
