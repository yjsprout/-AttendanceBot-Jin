import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime
import sqlite3

import itertools

bot = commands.Bot(command_prefix="!", intents = discord.Intents.default())
TOKEN = "MTA2MzMwMTQxODMzNDgxNDIxOA.G71WwG.aMQPwQOXBD4hxGBg6WYA4kBfonCcDt1WnzNsw8"

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
    sql2 = "INSERT INTO attTBL(name,date,time) values (?,?,?);"
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
    db_list=[]
    for row in cur:
        db_list.append(list(row))
    await interaction.response.send_message(f"{db_list}")
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
    appeared = []
    for row in cur:
        appeared.append(list(row))
    appeared2 = list(itertools.chain(*appeared))
    members = ['김주미', '양진', '김세연']
    for i in appeared2:
        members.remove(i)
    absent = members
    await interaction.response.send_message(f"출석 하지 않은 분들 명단 : {absent}")
    cur.close()

bot.run(TOKEN)
