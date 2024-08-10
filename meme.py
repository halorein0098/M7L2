import discord
from discord.ext import commands
import os
import random
import requests
from model import get_class

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
# Dan inilah cara Kamu mengganti nama file dari variabel!
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')
@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)
@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
                    picture = discord.File(f)
    await ctx.send(file=picture)

def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)


organic = ['veggie','grass','dried veggie','kayu','ranting pohon','daun','kulit buah','makanan sisa','buah','tisu','kapas','kertas']
anorganic =['plastik','botol','kaleng minuman','kresek','ban bekas','besi','kaca','kabel','barang elektronik','bohlam lampu','plastik']

@bot.command()
async def trash(ctx):
    await ctx.send("input your trash: ")
    msg = await bot.wait_for("message")
    if msg.content in organic:
        await ctx.send("put into organic trash can:")
    elif msg.content in anorganic:
        await ctx.send("put into anorganic trash can:")
@bot.command()
async def predict(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            await ctx.send(get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=f"./{attachment.filename}"))
    else:
        await ctx.send("You forgot to upload the image :(")
bot.run("")