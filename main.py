import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
from datetime import date, datetime, time as dt_time, timezone, timedelta

from services.exam_tracker import ExamTracker
from services.reminder import Reminder
import analytics as anal

load_dotenv()

exam_tracker = ExamTracker()
reminder_service = Reminder()

token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!!', intents=intents)
bot.remove_command('help')

DISCLAIMER_MSG = "all scores pre-**2022** have been standardized to **390**, so a score in **2021** which may have been **300** becomes **260** in current standards and settings of exam."

# default is UTC & I don't live in that region.
IST = timezone(timedelta(hours=5, minutes=30))

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

# this is for sending user reminders for their exam-time

@tasks.loop(time=dt_time(hour=9, minute=0, tzinfo=IST))
async def send_exam_reminders():
    """
    send daily reminders in the channel where interaction with bot was made.
    """
    
    reminder_service.reset_daily_tracking()
    reminders = reminder_service.users_to_remind()
    
    for reminder in reminders:
        channel = bot.get_channel(reminder['channel_id'])
        
        if channel:
            try:
                await channel.send(
                    f"<@{reminder['user_id']}> {reminder['message']}"
                )
                print(f"sent reminder to user {reminder['user_id']} in channel {channel.name}")
            except discord.Forbidden:
                print(f"no permission to send in channel {reminder['channel_id']}")
                try:
                    user = await bot.fetch_user(reminder['user_id'])
                    await user.send(reminder['message'])
                    print(f"sent DM fallback to {user.name}")
                except Exception as dm_error:
                    print(f"failed to DM user {reminder['user_id']}: {dm_error}")
            except Exception as e:
                print(f"failed to send reminder to {reminder['user_id']}: {e}")
        else:
            print(f"channel {reminder['channel_id']} not found, falling back to DM")
            try:
                user = await bot.fetch_user(reminder['user_id'])
                await user.send(reminder['message'])
                print(f"sent DM fallback to {user.name}")
            except Exception as e:
                print(f"failed to send to {reminder['user_id']}: {e}")

@send_exam_reminders.before_loop
async def before_reminder():
    await bot.wait_until_ready()

# all bot events/commands from here on now

@bot.event
async def on_ready():
    """
    prints to the console screen to my server laptop to signal the bot is up and running.
    """

    print("ready when you're")
    if not send_exam_reminders.is_running():
        send_exam_reminders.start()

@bot.command()
async def plot(ctx, campus_name: str):
    """
    uses the analytics file's function to generate plots to end-user only based on campus
    """
    
    try:
        await ctx.send(f"generating plot for {campus_name}")
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
        
        await ctx.send(f"generating plot for **{branch}** in **{campus}**")
        
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
        await ctx.send(f"**fetching {year} cutoffs for {campus.title()}**")
    else:
        await ctx.send(f"**fetching {year} cutoffs for all campuses**")
    
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
        await ctx.send(f"**generating 2026 {situation} predictions for {campus.title()}**")
    else:
        await ctx.send(f"**generating 2026 {situation} predictions**")
    
    try:
        filename = anal.get_predictions(limit=25, campus_filter=campus, situation=situation)
        
        await display(ctx, filename,
                     not_found_msg=f"no data found for campus: **{campus}**\n"
                                   "available campuses: Pilani, Goa, Hyderabad\n"
                                   "available situations: best, most-likely (can keep blank), worst")
    except Exception as e:
        await ctx.send(f"critical Error: {e}")


@bot.command()
async def sy(ctx):
    """
    sends syllabus of current year's bitsat examination syllabus to user.
    """

    await ctx.send(f"please check: https://admissions.bits-pilani.ac.in/FD/downloads/BITSAT_Syllabus.pdf?06012025")

@bot.command()
async def ypt(ctx):
    """
    sends information regarding official YPT group of the server to user.
    """

    await ctx.send(f"Group Name: BITSATards, Password: 123\nthe link is as follows: https://link.yeolpumta.com/P3R5cGU9Z3JvdXBJbnZpdGUmaWQ9MzU5OTUzNg==")

@bot.command()
async def da(ctx):
    """
    dates of bitsat-shifts & other such important tasks.
    """

    await ctx.send("Session 1 Starts From: Wednesday, 15 April 2026\nSession 2 Starts From: Sunday, 24 May 2026")

@bot.command()
async def resources(ctx):
    """
    Send study resources for BITSAT exam.
    """

    await ctx.send(f"please follow: https://www.reddit.com/r/Bitsatards/wiki/resources/ \nadditionally please refer to: https://discord.com/channels/1221093390167576646/1224005178106187877")

@bot.command()
async def time(ctx, flag: str = None, *, date_str: str = None):
    """
    this is for users to effectively track how much time they have till their D-Day.

    flags:
        !!time (default, no flags) does the job of returning user how much time is left till their exam.
        !!time -s DD-MM-YYYY to set the exam date to track.
        !!time -r will reset exam-date that has been set by user.
    """

    try:
        if flag is None:
            message = exam_tracker.get_countdown(ctx.author.id)
            await ctx.send(message)
            return

        if flag in ['-s', '-set', '--set']:
            if not date_str:
                await ctx.send("please provide a date\nusage: `!!exam -s DD-MM-YYYY`\nExample: `!!exam -s 15-04-2026`")
                return

            try:
                exam_date = datetime.strptime(date_str, '%d-%m-%Y').date()
                message = exam_tracker.set_exam_date(
                    user_id=ctx.author.id,
                    username=str(ctx.author),
                    channel_id=ctx.channel.id,
                    exam_date=exam_date
                )
                await ctx.send(message)
            except ValueError:
                await ctx.send("invalid date format!\nplease use: `!!exam -s DD-MM-YYYY`\nExample: `!!exam -s 15-04-2026`")

        elif flag in ['-r', '-reset', '--reset']:
            message = exam_tracker.reset(ctx.author.id)
            await ctx.send(message)
    
    except Exception as e:
        await ctx.send(f"error: {str(e)}")

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

• `!!da` - get exam-shift dates for both sessions

• `!!time` - track your time till your bitsat-shift, use flags such as -s & -r for your needs
  Example: `!!time -s 15-04-2026` or `!!time -r`

• `!!ypt` - get the link, group-name & password for the official bitsatards-YPT group 

• `!!sy` - get syllabus for current BITSAT examination

• `!!resources` - get study resources for the BITSAT examination

• `!!help` - shows this help message

**Available Campuses:** Pilani, Goa, Hyderabad
**Branch Shortcuts:** cse, ece, eee, mech, civil, chem, eni, manufacturing, pharm, and more
    """
    await ctx.send(helper)

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
