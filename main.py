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

DISCLAIMER_MSG = "all scores pre-**2022** have been standardized to **390**, so a score in **2021** which may have been **300** becomes **260** in current standards and settings of exam."

async def display(ctx, filename: str, disclaimer: bool = True, not_found_msg: str = None):
    """
    sends a file to discord then cleanup.
    disclaimer message is optional.
    """

    if filename and os.path.exists(filename):
        try:
            with open(filename, 'rb') as f:
                await ctx.send(file=discord.File(f, filename=os.path.basename(filename)))
                if disclaimer:
                    await ctx.send(DISCLAIMER_MSG)
            return True
        finally:
            os.remove(filename)
    else:
        if not_found_msg:
            await ctx.send(not_found_msg)
        else:
            await ctx.send(f"error: could not generate or find file.")
        return False

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
        
        await display(ctx, filename, 
                     not_found_msg=f"no data found for campus: {campus_name}")
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
        
        await display(ctx, filename,
                     not_found_msg="error: file generated but not found.")
        
    except Exception as e:
        await ctx.send(f"error: {str(e)}")

@bot.command(name='select')
async def select(ctx, *, args: str = None):
    """
    sends cutoffs for a particular year for a specified campus (if any).
    uses select func in analytics file.
    """
    
    if not args:
        await ctx.send("**Usage:** `!!select [year]` or `!!select [year], [campus]`\n"
                      "Example: `!!select 2024` or `!!select 2024, Pilani`")
        return
    
    # parse-args
    year = None
    campus = None
    
    if "," in args:
        parts = args.split(",", 1)
        year_str = parts[0].strip()
        campus = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
    else:
        year_str = args.strip()
    
    try:
        year = int(year_str)
    except ValueError:
        await ctx.send(f"**error:** invalid year '{year_str}'. Please provide a valid year such as 2024")
        return
    
    if campus:
        await ctx.send(f"**fetching {year} cutoffs for {campus.title()}...**")
    else:
        await ctx.send(f"**fetching {year} cutoffs for all campuses...**")
    
    try:
        filename = anal.select(limit=25, year=year, campus_filter=campus)
        
        await display(ctx, filename,
                     not_found_msg=f"**No data found**\n"
                                   f"• Year: {year}\n"
                                   f"• Campus: {campus if campus else 'All'}\n\n"
                                   "**Available campuses:** Pilani, Goa, Hyderabad")
    except Exception as e:
        await ctx.send(f"**error:** {str(e)}")

@bot.command(name='predict')
async def predict(ctx, *, args: str = None):
    """
    sends predicted-data found in csv files in neat and tabular manner.
    uses get_predictions func in analytics file.
    """
    
    # parse-args
    campus = None
    situation = 'most-likely'
    
    if args:
        if "," in args:
            parts = args.split(",", 1)
            campus = parts[0].strip() if parts[0].strip() else None
            situation = parts[1].strip() if len(parts) > 1 and parts[1].strip() else 'most-likely'
        else:
            campus = args.strip()
    
    if campus:
        await ctx.send(f"**generating 2026 {situation} predictions for {campus.title()}...**")
    else:
        await ctx.send(f"**generating 2026 {situation} predictions...**")
    
    try:
        filename = anal.get_predictions(limit=25, campus_filter=campus, situation=situation)
        
        await display(ctx, filename,
                     not_found_msg=f"no data found for campus: **{campus}**\n"
                                   "available campuses: Pilani, Goa, Hyderabad\n"
                                   "available situations: best, most-likely (can keep blank), worst")
    except Exception as e:
        await ctx.send(f"critical Error: {e}")

@bot.command()
async def resources(ctx):
    """
    Send study resources for BITSAT exam.
    """

    await ctx.send(f"please follow : https://www.reddit.com/r/Bitsatards/wiki/resources/")

@bot.command()
async def help(ctx):
    """
    Show help message with all available commands.
    """
    
    helper = """
**Available Commands**

this bot helps you get a rough idea of BITSAT exam cutoffs for the upcoming year, please note that predictions are estimates and may not reflect actual values.

**Commands:**
• `!!plot [campus-name]` - plot marks trend for all branches in a campus
  Example: `!!plot Pilani`

• `!!plot-branch [campus-name], [branch-name]` - plot marks trend for a specific branch
  Example: `!!plot-branch Pilani, B.E. Computer Science`
  Note: comma separator is required and is not optional and now you can also use shortcuts like `cse`, `ece`, `mech`

• `!!select [year], [campus-name]` - shows values of cutoffs for a particular year in BITSAT exam for all or a specified campus in tabulated manner.
  Example: `!!select 2025`, `!!select 2025, pilani`

• `!!predict [campus-name], [situation]` - show predictions for 2026 BITSAT exam with option to see different scenarios
  Example: `!!predict`, `!!predict Pilani`, `!!predict Pilani, worst`

• `!!resources` - get study resources for the BITSAT examination

• `!!help` - shows this help message

**Available Campuses:** Pilani, Goa, Hyderabad
**Branch Shortcuts:** cse, ece, eee, mech, civil, chem, eni, manufacturing, pharm, and more
    """
    await ctx.send(helper)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
