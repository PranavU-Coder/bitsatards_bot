import discord 
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import analytics as anal

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='@', intents=intents)
bot.remove_command('help')

# all bot events/commands from here on now

@bot.event 
async def on_ready():
    print("ready when you're")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def plot(ctx, campus_name: str):
    try:
        await ctx.send(f"generating plot for {campus_name}...")
        
        anal.plot_marks_by_campus(campus_name)
        
        filename = f"{campus_name.lower()}_marks_trend.png"
        
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                await ctx.send(file=discord.File(f, filename))
            os.remove(filename)
        else:
            await ctx.send(f"No data found for campus: {campus_name}")
    except Exception as e:
        await ctx.send(f"Error generating plot: {str(e)}")

@bot.command(name='plot-branch')
async def plot_branch(ctx, campus_name: str, *, branch: str):
    try:
        await ctx.send(f"Generating plot for {branch} in {campus_name}...")
        
        anal.plot_marks_by_branch(campus_name, branch)
        filename = f"{campus_name.lower()}_{branch.lower().replace(' ', '_').replace('.', '')}_marks_trend.png"
        
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                await ctx.send(file=discord.File(f, filename))
            os.remove(filename)
        else:
            await ctx.send(f"No data found for {branch} in {campus_name}")
    except Exception as e:
        await ctx.send(f"Error generating plot: {str(e)}")

@bot.command()
async def help(ctx):
    helper = """
**available commands**

this bot helps you give a rough idea what the bitsat exam cutoffs for the upcoming year should be and should be noted that this bot can't possibly predict the actual/exact value.

**Commands:**
• `@plot <campus-name>` - plot marks trend for all branches in a campus
  Example: `@plot Pilani`

• `@plot-branch <campus-name> <branch-name>` - plot marks trend for a specific branch
  Example: `@plot-branch Pilani B.E. Computer Science`

• `@help` - show this help message

**Available Campuses:** Pilani, Goa, Hyderabad
**Branch Names:** Use exact names like "B.E. Computer Science", etc.
    """
    await ctx.send(helper)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)