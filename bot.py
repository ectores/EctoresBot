# bot.py
import os
import random
import discord
import time
import io

# from commands import new_command
from discord.ext import commands
from dotenv import load_dotenv
from environ import Env
from mutagen.mp3 import MP3

env = Env()
env.read_env()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND = os.getenv('DISCORD_COMMAND')
SOUND1 = os.getenv('DISCORD_SOUND1')
SOUND2 = os.getenv('DISCORD_SOUND2')
USER1 = int(os.getenv('DISCORD_USER1'))
USER2 = int(os.getenv('DISCORD_USER2'))
USER3 = int(os.getenv('DISCORD_USER3'))
USER4 = int(os.getenv('DISCORD_USER4'))
# print(f"Comando: {COMMAND}")

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)


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

    if after.channel == None:
        return

    #When 2 users are connected simultaneously, the bot join at voice channel and will play a sound
    list_id = (USER1,USER2)
    
    channel = bot.get_channel(after.channel.id)

    if member.id in list_id and before.channel == None:

        contador = 0
        max_cont = 2
        
        for _ in channel.members:
            if _.id in list_id:
                contador += 1
        
        if contador == max_cont:
            await bot_music(SOUND1,channel,1)

        else:
            print("I need more users for talking")
    #When a specific user enter a channel, the bot join at voice channel and will play a sound
    if (member.id == USER3 or member.id == USER4) and before.channel == None:
        await bot_music(SOUND2,channel,1)



@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
    message_content = message.content
    #Here the bot detect a valid command
    if message_content.startswith(f"{COMMAND}"):
        list_message = message_content.split(" ")
        total_message = [i for i in list_message if i != ""]
        if len(total_message) == 1:
            await message.channel.send(f"For showing my commands use **{COMMAND} help**")
            return
        #See all the mp3 files in the MP3 folder
        if message_content == f"{COMMAND} playlist":
            archivos = os.listdir("mp3/")
            mensaje_1 = "I have the followings audios (separated by space):"

            mensaje_2 = ""

            for elem in archivos:
                mensaje_2 += " " + elem[:len(elem) - 4]

            await message.channel.send(f"{mensaje_1}{mensaje_2}")
        
        #See if is a play command
        elif message_content.startswith(f"{COMMAND} play"):
            if len(total_message) == len(f"{COMMAND} play"):
                await message.channel.send("The audio input doesn't exists :(")
                return
            #If
            elif len(total_message) == (len(f"{COMMAND}") + 2):
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
        elif message_content == f"{COMMAND} joke" or message_content == f"{COMMAND} jokes":
            jokes = io.open("jokes.txt", mode="r", encoding="utf-8")
            response = random.choice(jokes.readlines())
            jokes.close()
            await message.channel.send(response)
        #See all the command's bot
        elif message_content == f"{COMMAND} help":
            await message.channel.send("Hi, I'm EctoresBOT and I'm here ~~for stealing your money hehe,~~ say dumb jokes, enter at voices channel and play audios. These are my commands:")
            await message.channel.send(f"**{COMMAND} help**   For showing my commands (recursion :O)")
            await message.channel.send(f"**{COMMAND} joke**   For telling a ~~dumb~~ joke")
            await message.channel.send(f"**{COMMAND} play *mp3_file***   For playing a mp3 file in my directory (you should be in a voice channel)")
            await message.channel.send(f"**{COMMAND} playlist**   For showing all the mp3 files in the folder.")


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
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio(music_format))
    time.sleep(mutagen_length(music_format))
    await vc.disconnect()

#See the mp3 duration
def mutagen_length(path):
    audio = MP3(path)
    length = audio.info.length
    return length

#Run Barry Run :D
bot.run(TOKEN)