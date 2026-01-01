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
    """
    prints to the console screen to my server laptop to signal the bot is up and running.
    """

    print("ready when you're")

@bot.command()
async def plot(ctx, campus_name: str):
    """
    uses the analytics file's function to generate plots to end-user only based on campus
    """

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
    """
    uses the analytics file's function to generate plots to end-user now on both campus and its respective branch.
    """

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
    """
    sends hardcoded-data found in analytics file to end-user in a nice tabular-format.
    """

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
    """
    sends end-user all the resources to practice for the bitsat entrance examination.
    """

    await ctx.send(f"please follow : https://www.reddit.com/r/Bitsatards/wiki/resources/")

@bot.command()
async def help(ctx):
    """
    guides the end-user to help navigating with the bot.
    """

    helper = """
**Available Commands**

this bot helps you get a rough idea of BITSAT exam cutoffs for the upcoming year, please note that predictions are estimates and may not reflect actual values.

**Commands:**
• `!!plot <campus-name>` - plot marks trend for all branches in a campus
  Example: `!!plot Pilani`

• `!!plot-branch <campus-name>, <branch-name>` - plot marks trend for a specific branch
  Example: `!!plot-branch Pilani, B.E. Computer Science`
  Note: comma separator is required and is not optional also you can use shortcuts like `cse`, `ece`, `mech`

• `!!predict [campus-name]` - show predictions for 2026 BITSAT exam
  Example: `!!predict` or `!!predict Pilani`

• `!!resources` - get study resources for the BITSAT examination

• `!!help` - shows this help message

**Available Campuses:** Pilani, Goa, Hyderabad
**Branch Shortcuts:** cse, ece, eee, mech, civil, chem, eni, manufacturing, pharm, and more
    """
    await ctx.send(helper)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
