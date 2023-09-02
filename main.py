import discord
import json
from yt_dlp import YoutubeDL
from discord.ext import commands
from asyncio import sleep

# install PyNaCl

#Use only Windows users or if you are not installed ffmpeg on your system
FFMPEG_PATH = 'YOUR PATH'
#Options for yt_dlp
YDL_OPTIONS = {
    'format': 'bestaudio',} #only audio
#Options for ffmpeg
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#file with config your bot
file = open('config.json', 'r')
config = json.load(file)
#list video
playlist = set()
#init bot
bot = commands.Bot(intents=discord.Intents.all(), command_prefix=config['prefix'])

@bot.event
async def on_ready():
    print('Bot online')

@bot.command(name='play')
async def play(ctx, args):
    global voice
    try:
        voice = await ctx.message.author.voice.channel.connect(reconnect=True, timeout=None)
    except:
        print('Error voice')
    if voice.is_playing():
        playlist.add(args)
        print("added")
        return
    playlist.add(args)

    await ctx.message.delete() #auto delete message on chat

    while True:
        if voice.is_playing() or len(playlist) == 0:
            await sleep(5)
            continue
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(playlist.pop(), download=False)
        URL = info['url']
        voice.play(discord.FFmpegPCMAudio(#executable=FFMPEG_PATH USE THIS IF YOU CHANGE FFMPEG PATH
                   source=URL, **FFMPEG_OPTIONS))

@bot.command(name='stop')
async def stop(ctx):
    await ctx.message.delete()
    if voice.is_playing():
        voice.pause()

@bot.command(name='skip')
async def skip(ctx):
    await ctx.message.delete()
    voice.stop()

@bot.command(name='resume')
async def resume(ctx):
    await ctx.message.delete()
    if not voice.is_playing():
        voice.resume()

@bot.command(name='leave')
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.message.delete()
    playlist.clear()

#run your bot
bot.run(config['token'])
