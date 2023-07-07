# bot.py
import os
import random
import discord
import time
import io
import pandas as pd
import config

# from commands import new_command
from discord.ext import commands
from dotenv import load_dotenv
from environ import Env
from mutagen.mp3 import MP3

env = Env()
env.read_env()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# SOUND1 = os.getenv('DISCORD_SOUND1')
# USER1 = int(os.getenv('DISCORD_USER1'))
# USER2 = int(os.getenv('DISCORD_USER2'))

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

config_file = config.Config().config_file
command = config_file["Information"]["Command"]
print(f"Comando: {command}")

@bot.event
#When the bot runs, it will print when it is connected and will say in which server it is
async def on_ready():
    print(f'{bot.user.name} is connected to Discord!')
 
    print(f'{bot.user} is connected to the following Discord Servers:\n')
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')


#Special Use
@bot.event
async def on_voice_state_update(member,before,after):
    server_id = str(member.guild.id)
    member_id = str(member.id)
    sound = "default"

    if after.channel == None:
        return

    #When 2 users are connected simultaneously, the bot join at voice channel and will play a sound
    #With the new customization, i think this feature is not needed.
    # list_id = (USER1,USER2)
    

    # if member.id in list_id and before.channel == None:

    #     contador = 0
    #     max_cont = 2
        
    #     for _ in channel.members:
    #         if _.id in list_id:
    #             contador += 1
        
    #     if contador == max_cont:
    #         await bot_music(SOUND1,channel,1)

    #     else:
    #         print("I need more users for talking")
    #When a specific user enter a channel, the bot join at voice channel and will play a sound
    if before.channel == None:
        channel = bot.get_channel(after.channel.id)
        try:
            sound = config.Config().search_sound(server_id, member_id)
            await bot_music(sound,channel,1)
        except:
            pass


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    message_content = message.content
    #Here the bot detect a valid command
    if message_content.startswith(f"{command}"):
        list_message = message_content.split(" ")
        total_message = [i for i in list_message if i != ""]

        list_command = command.split(" ")
        total_command = [i for i in list_command if i != ""]
        if len(total_message) == 1:
            await message.channel.send(f"For showing my commands use **{command} help**")
            return
        #See all the mp3 files in the MP3 folder
        if message_content.startswith(f"{command} addsound"):
            if len(total_message) == len(f"{command} addsound"):
                await message.channel.send("You need add a argument(sound name)")
                return
            elif len(total_message) == (len(total_command) + 2):
                
                config.Config().add_user(message.guild.id, message.author.id, total_message[len(total_message) - 1])
                await message.channel.send(f"Hey {message.author.name}, your sound has been added.")

        elif message_content == f"{command} playlist":
            archivos = os.listdir("mp3/")
            mensaje_1 = "I have the followings audios (separated by space):"
            mensaje_2 = ""

            for elem in archivos:
                mensaje_2 += " " + elem[:len(elem) - 4]

            await message.channel.send(f"{mensaje_1}{mensaje_2}")
        
        #See if is a play command
        elif message_content.startswith(f"{command} play"):
            if len(total_message) == len(f"{command} play"):
                await message.channel.send("You need add a argument(sound name)")
                return
            #If
            elif len(total_message) == (len(total_command) + 2):
                text_channel = message.channel 
                user_id = message.author.id
                guild_id = message.guild.id

                for guild in bot.guilds:
                    if guild.id == guild_id:
                        for voice_channel in guild.voice_channels:
                            for member in voice_channel.members:
                                if member.id == user_id:
                                    print(f"{member.name}(ID: {member.id}) invoke me")
                                    await bot_music(total_message[2],voice_channel, text_channel)
                                    break
                        break
        #See if is a joke command
        elif message_content == f"{command} joke" or message_content == f"{command} jokes":
            jokes = io.open("jokes.txt", mode="r", encoding="utf-8")
            response = random.choice(jokes.readlines())
            jokes.close()
            await message.channel.send(response)
        #See all the command's bot
        elif message_content == f"{command} help":
            await message.channel.send("Hi, I'm EctoresBOT and I'm here ~~for stealing your money hehe,~~ say dumb jokes, enter at voices channel and play audios. These are my commands:")
            await message.channel.send(f"**{command} addsound *sound**   For adding your custom sound when you enter at the voice chat :D")
            await message.channel.send(f"**{command} help**   For showing my commands (recursion :O)")
            await message.channel.send(f"**{command} joke**   For telling a ~~dumb~~ joke")
            await message.channel.send(f"**{command} play *mp3_file***   For playing a mp3 file in my directory (you should be in a voice channel)")
            await message.channel.send(f"**{command} playlist**   For showing all the mp3 files in the folder.")


#Funtion for playing a mp3 file in a specific channel
async def bot_music(music, channel, text):
    music_format = "mp3/" + music + ".mp3"
    # print(f"1er formato: {music_format}")
    file_exist = os.path.isfile(music_format)
    if not file_exist and text != 1:
        music_format = "mp3/default.mp3"
        await text.send("I don't found the mp3, I'm scared D:")
    channel = channel
    print(f"audio to play: {music_format}")
    await wait(channel, music_format)

#See the mp3 duration
def mutagen_length(path):
    audio = MP3(path)
    length = audio.info.length
    return length

#If the bot is already connected, the bot wait until it isn't in the voice channel
async def wait(channel, music_format):
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(music_format))
    time.sleep(mutagen_length(music_format))
    await vc.disconnect()

#Run Barry Run :D
bot.run(TOKEN)