# bot.py
import os
import random
import discord
import time
import io

from discord.ext import commands
from dotenv import load_dotenv
from environ import Env

env = Env()
env.read_env()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

USER1 = int(os.getenv('DISCORD_USER1'))
USER2 = int(os.getenv('DISCORD_USER2'))
USER3 = int(os.getenv('DISCORD_USER3'))

# client = discord.Client(intents=discord.Intents.default())

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


 
@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado a Discord!')
 
    print(f'{bot.user} is connected to the following guild:\n')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')



@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Pium Pium {member.name}, bienvenido al Monke Server Pium Pium!'
    )



@bot.event
async def on_voice_state_update(member,before,after):

    if after.channel == None:
        return
    
    # print(f"{member.name} ha cambiado su estado en el canal de voz")
    list_id = (USER1,USER2)
    
    # print(list_id)
    
    if member.id in list_id and before.channel == None:

        channel = bot.get_channel(after.channel.id)

        contador = 0
        max_cont = 2
        # print(f"miembros del canal: {channel.members}")
        
        for _ in channel.members:
            # print(f"id: {_.id}")
            if _.id in list_id:
                contador += 1
                # print("Se ha conectado alguien relevante")
        
        if contador == max_cont:
            print("Hora de unirme al servidor")
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio('testing.mp3'), after=lambda e: print('done', e))
            time.sleep(7)
            await vc.disconnect()

        else:
            print("Falta gente")

    if member.id == USER3 or member.id == USER1 and before.channel == None:
        channel = bot.get_channel(after.channel.id)
        print("Hora de ser un Saco Bot")
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('sus.mp3'), after=lambda e: print('done', e))
        time.sleep(5)
        await vc.disconnect()



@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    
    message_content = message.content

    if message_content == '/sus':
        user_id = message.author.id
        guild_id = message.guild.id

        for guild in bot.guilds:
            if guild.id == guild_id:
                for channel in guild.voice_channels:
                    # print(channel.members)
                    for member in channel.members:
                        if member.id == user_id:
                            print(f"{member.name} me ha invocado")
                            vc = await channel.connect()
                            vc.play(discord.FFmpegPCMAudio('sus.mp3'), after=lambda e: print('done', e))
                            time.sleep(5)
                            await vc.disconnect()
                            break
                break

    elif message_content == '/piumpium':
        jokes = io.open("jokes.txt", mode="r", encoding="utf-8")
        response = random.choice(jokes.readlines())
        jokes.close()
        print("piumpium")
        await message.channel.send(response)

        
 
bot.run(TOKEN)