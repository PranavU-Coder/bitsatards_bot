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

bot = commands.Bot(command_prefix='!!', intents=intents)
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
            await ctx.send(f"no data found for campus: {campus_name}")
    except Exception as e:
        await ctx.send(f"error generating plot: {str(e)}")

@bot.command(name='plot-branch')
async def plot_branch(ctx, *, args: str):
    try:
        if "," not in args:
            await ctx.send("**usage:** `!!plot-branch <Campus>, <Branch>`")
            return

        campus_raw, branch_raw = args.split(",", 1)
        campus = campus_raw.strip() 
        branch = branch_raw.strip()

        await ctx.send(f"generating plot for **{branch}** in **{campus}**...")
        
        filename = anal.plot_marks_by_branch(campus, branch)
        
        if filename is None:
            await ctx.send(f"no data found for **{branch}** in **{campus}**.")
            return

        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as f:
                    await ctx.send(file=discord.File(f, filename=filename))
            finally:
                os.remove(filename)
        else:
            await ctx.send("error: file generated but not found.")

    except Exception as e:
        await ctx.send(f"error: {str(e)}")

@bot.command(name='predict')
async def predict(ctx, campus: str = None):
    if campus:
        await ctx.send(f"**generating 2026 predictions for {campus.title()}...**")
    else:
        await ctx.send(f"**generating 2026 predictions...**")
    
    try:
        filename = anal.get_predictions(limit=25, campus_filter=campus)
        if filename and os.path.exists(filename):
            with open(filename, 'rb') as f:
                await ctx.send(file=discord.File(f, filename))
            os.remove(filename)
        else:
            await ctx.send(f"no data found for campus: **{campus}**\n"
                           "Available campuses: Pilani, Goa, Hyderabad")
    except Exception as e:
        await ctx.send(f"critical Error: {e}")

@bot.command()
async def resources(ctx):
    await ctx.send(f"please follow : https://www.reddit.com/r/Bitsatards/wiki/resources/")

@bot.command()
async def help(ctx):
    helper = """
**available commands**

this bot helps you give a rough idea what the bitsat exam cutoffs for the upcoming year should be and should be noted that this bot can't possibly predict the actual/exact value.

**Commands:**
• `!!plot <campus-name>` - plot marks trend for all branches in a campus.
  Example: `!!plot Pilani`

• `!!plot-branch <campus-name>, <branch-name>` - plot marks trend for a specific branch
  Example: `!!plot-branch Pilani, B.E. Computer Science` please note that the comma is a must for the bot to read and execute command in this function.

• `!!predict` - shows all the predictions made for the 2026 bitsat exam through past years data, you can also add a campus name infront of it to see in detail wrt all branches.

• `!!resources' - to get all the resources that can help you score better for this examination.

• `!!help` - shows this help message.

**Available Campuses:** Pilani, Goa, Hyderabad
**Branch Names:** Use exact names like "B.E. Computer Science", etc.
    """
    await ctx.send(helper)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)