import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

if os.getenv('RAILWAY_ENVIRONMENT') is None:  
    load_dotenv()

token = os.getenv('TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

secret_role = 'gaymer'

bot = commands.Bot(command_prefix='@', intents=intents)

# all bot events/commands from here on now

@bot.event 
async def on_ready():
    print("ready when you're")

@bot.event 
async def on_member_join(member):
    await member.send(f"welcome to the server! {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} don't use that word")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send("hello {ctx.author.mention}")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} has been assigned to {secret_role}")
    else:
        await ctx.send("role doesn't exist")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has been removed of the role")
    else:
        await ctx.send("role doesn't exist")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)