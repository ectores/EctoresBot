# bot.py
import os
import random
import discord
import time

from discord.ext import commands
from dotenv import load_dotenv
from environ import Env

env = Env()
env.read_env()
 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
JOKES = os.getenv('DISCORD_JOKES').split(',')
USER1 = int(os.getenv('DISCORD_USER1'))
USER2 = int(os.getenv('DISCORD_USER2'))
 
# client = discord.Client(intents=discord.Intents.default())

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
 
@bot.event
async def on_ready():
    print(f'{bot.user.name} se ha conectado a Discord!')
 
    for guild in bot.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Pium Pium {member.name}, bienvenido al Monke Server Pium Pium!'
    )
 

 
@bot.event
async def on_message(message):
    print(f'Jokes: {JOKES}')
    message_content = message.content
    # print('Mensaje recibido')

    if message_content == '/piumpium':

        response = random.choice(JOKES)

        await message.channel.send(response.replace("'","").replace("]","").replace("[",""))




@bot.event
async def on_voice_state_update(member,before,after):

    if after.channel == None:
        return
    
    list_id = (USER1,USER2)
    print(list_id)
    
    if member.id in list_id:

        channel = bot.get_channel(after.channel.id)

        contador = 0
        max_cont = 2
        for _ in channel.members:
            if _.id in list_id:
                contador += 1
                print("Se ha conectado alguien relevante")
        
        if contador == max_cont:
            print("Hora de unirme al servicor")
            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio('testing.mp3'), after=lambda e: print('done', e))
            time.sleep(7)
            await vc.disconnect()


        else:
            print("Falta gente")

@bot.command("piumpiumon")
async def join(ctx):
    print("piumpiumon :3")
    channel = ctx.author.voice.channel
    await channel.connect() 

@bot.command("piumpiumof")
async def leave(ctx):
    print("piumpiumof :()")
    await ctx.voice_client.disconnect()

 
bot.run(TOKEN)