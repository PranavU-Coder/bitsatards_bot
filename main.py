import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv

import os
import re

from datetime import datetime, time as dt_time, timezone, timedelta
import asyncio
from functools import partial

from services.exam_tracker import ExamTracker
from services.reminder import Reminder
import analytics as anal

load_dotenv()

CAMPUSES = ["pilani", "goa", "hyderabad"]

exam_tracker = ExamTracker()
reminder_service = Reminder()

token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!!", intents=intents)
bot.remove_command("help")

DISCLAIMER_MSG = "all scores pre-**2022** have been standardized to **390**, so a score in **2021** which may have been **300** becomes **260** in current standards and settings of exam."

IST = timezone(timedelta(hours=5, minutes=30))


async def display(ctx, cache_key, title, generator_func, filename, disclaimer=True):
    """
    generates a plot/table based on user-req throught generator_func availed in analytics.py, if cache-hit is found it immediately sends the embed of that to user.
    disclaimer message is optional.
    """

    cached_url = anal.get_cached_url(cache_key)

    if cached_url:
        print(f"cache hit: {cache_key}")
        embed = discord.Embed(title=title)
        embed.set_image(url=cached_url)
        await ctx.send(embed=embed)
        if disclaimer:
            await ctx.send(DISCLAIMER_MSG)
        return True

    image_buffer = await generator_func

    if image_buffer is None:
        return None

    try:
        image_buffer.seek(0)
        file = discord.File(fp=image_buffer, filename=filename)
        sent_message = await ctx.send(file=file)
        if disclaimer:
            await ctx.send(DISCLAIMER_MSG)

        if sent_message.attachments:
            anal.save_url_to_cache(cache_key, sent_message.attachments[0].url)
            print(f"cached: {cache_key}")

    except Exception as e:
        await ctx.send(f"error uploading: {e}")
        return None
    finally:
        image_buffer.close()

    return True


def parse_campus(args):
    clean_args = args.lower()
    for c in CAMPUSES:
        if c in clean_args:
            return c, clean_args.replace(c, "", 1)
    return None, clean_args


async def send_dm(user_id, message):
    try:
        user = await bot.fetch_user(user_id)
        await user.send(message)
        print(f"sent DM fallback to {user.name}")
    except Exception as e:
        print(f"failed to DM user {user_id}: {e}")


@tasks.loop(time=dt_time(hour=9, minute=0, tzinfo=IST))
async def send_exam_reminders():
    """
    send daily reminders in the channel where interaction with bot was made.
    """

    reminder_service.reset_daily_tracking()
    reminders = reminder_service.users_to_remind()

    for reminder in reminders:
        channel = bot.get_channel(reminder["channel_id"])
        msg = f"<@{reminder['user_id']}> {reminder['message']}"

        if channel:
            try:
                await channel.send(msg)
                print(
                    f"sent reminder to user {reminder['user_id']} in channel {channel.name}"
                )
            except discord.Forbidden:
                print(f"no permission in channel {reminder['channel_id']}")
                await send_dm(reminder["user_id"], reminder["message"])
            except Exception as e:
                print(f"failed to send reminder: {e}")
        else:
            print(f"channel {reminder['channel_id']} not found")
            await send_dm(reminder["user_id"], reminder["message"])


@send_exam_reminders.before_loop
async def before_reminder():
    await bot.wait_until_ready()


@bot.event
async def on_ready():
    print("ready when you're")
    if not send_exam_reminders.is_running():
        send_exam_reminders.start()


@bot.command(name="plot")
async def plot(ctx, *, args: str = None):
    if not args:
        return await ctx.send("Usage: `!!plot <campus>`")

    campus, _ = parse_campus(args)

    if not campus:
        return await ctx.send("invalid campus. Please use Pilani, Goa, or Hyderabad.")

    loop = asyncio.get_event_loop()
    generator = loop.run_in_executor(None, partial(anal.plot_marks_by_campus, campus))

    result = await display(
        ctx,
        cache_key=f"plot_{campus}",
        title=f"{campus.title()} Cutoff Trends",
        generator_func=generator,
        filename=f"{campus}_plot.png",
    )

    if result is None:
        await ctx.send(f"No data found for campus: {campus}")


@bot.command(name="plot-branch")
async def plot_branch(ctx, *, args: str = None):
    if not args:
        return await ctx.send("Usage: `!!plot-branch <branch> <campus>`")

    campus, clean_args = parse_campus(args)

    if not campus:
        return await ctx.send("please specify a campus (Pilani, Goa, or Hyderabad).")

    branch = clean_args.replace(",", "").strip()

    if not branch:
        return await ctx.send("please specify a branch name.")

    await ctx.send(f"generating plot for **{branch}** in **{campus.title()}**...")

    loop = asyncio.get_event_loop()
    generator = loop.run_in_executor(
        None, partial(anal.plot_marks_by_branch, campus, branch)
    )

    result = await display(
        ctx,
        cache_key=f"plot_branch_{campus}_{branch}",
        title=f"{branch} - {campus.title()}",
        generator_func=generator,
        filename=f"{campus}_{branch}.png",
    )

    if result is None:
        await ctx.send(f"no data found for **{branch}** in **{campus}**.")


@bot.command(name="select")
async def select(ctx, *, args: str = None):
    if not args:
        return await ctx.send("usage: `!!select 2024` or `!!select 2024 Pilani`")

    year_match = re.search(r"\b(20\d{2})\b", args)
    if not year_match:
        return await ctx.send(
            "could not find a valid year (e.g., 2024) in your command."
        )

    year = int(year_match.group(1))
    remaining_args = args.replace(year_match.group(1), "")

    campus, _ = parse_campus(remaining_args)
    campus_title = campus.title() if campus else None

    filter_msg = f" - {campus_title}" if campus_title else " - All Campuses"
    await ctx.send(
        f"fetching **{year}** cutoffs{filter_msg.replace(' - ', ' for ')}..."
    )

    loop = asyncio.get_event_loop()
    generator = loop.run_in_executor(
        None, partial(anal.select, limit=25, year=year, campus_filter=campus_title)
    )

    result = await display(
        ctx,
        cache_key=f"select_{year}_{campus_title or 'all'}",
        title=f"{year} Cutoffs{filter_msg}",
        generator_func=generator,
        filename=f"cutoff_{year}.png",
    )

    if result is None:
        await ctx.send(f"No data found for {year}.")


@bot.command(name="predict")
async def predict(ctx, *, args: str = None):
    situation = "most-likely"
    campus = None

    if args:
        raw_args = args.lower().replace("most likely", "most-likely")

        for s in ["worst", "best", "most-likely"]:
            if s in raw_args:
                situation = s
                raw_args = raw_args.replace(s, "")
                break

        campus = raw_args.replace(",", "").strip() or None

    filter_msg = f" - {campus.title()}" if campus else " - All Campuses"
    await ctx.send(
        f"fetching **{situation}** case predictions{filter_msg.replace(' - ', ' for ')}..."
    )

    loop = asyncio.get_event_loop()
    generator = loop.run_in_executor(
        None,
        partial(
            anal.get_predictions, limit=25, campus_filter=campus, situation=situation
        ),
    )

    result = await display(
        ctx,
        cache_key=f"predict_{situation}_{campus or 'all'}",
        title=f"{situation.title()} Case Predictions{filter_msg}",
        generator_func=generator,
        filename=f"pred_2026_{situation}.png",
    )

    if result is None:
        await ctx.send("no prediction data found.")


@bot.command()
async def sy(ctx):
    await ctx.send(
        "please check: https://admissions.bits-pilani.ac.in/FD/downloads/BITSAT_Syllabus.pdf?06012025"
    )


@bot.command()
async def ypt(ctx):
    await ctx.send(
        "Group Name: BITSATards, Password: 123\nthe link is as follows: https://link.yeolpumta.com/P3R5cGU9Z3JvdXBJbnZpdGUmaWQ9MzU5OTUzNg=="
    )


@bot.command()
async def da(ctx):
    await ctx.send(
        "Session 1 Starts From: Wednesday, 15 April 2026\nSession 2 Starts From: Sunday, 24 May 2026"
    )


@bot.command()
async def resources(ctx):
    await ctx.send(
        "please follow: https://www.reddit.com/r/Bitsatards/wiki/resources/ \nadditionally please refer to: https://discord.com/channels/1221093390167576646/1224005178106187877"
    )


@bot.command()
async def src(ctx):
    await ctx.send(
        "please consider starring this project if you liked it: https://github.com/PranavU-Coder/bitsatards_bot"
    )


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
            return await ctx.send(exam_tracker.get_countdown(ctx.author.id))

        if flag in ["-s", "-set", "--set"]:
            if not date_str:
                return await ctx.send(
                    "please provide a date\nusage: `!!exam -s DD-MM-YYYY`\nExample: `!!exam -s 15-04-2026`"
                )

            try:
                exam_date = datetime.strptime(date_str, "%d-%m-%Y").date()
                message = exam_tracker.set_exam_date(
                    user_id=ctx.author.id,
                    username=str(ctx.author),
                    channel_id=ctx.channel.id,
                    exam_date=exam_date,
                )
                await ctx.send(message)
            except ValueError:
                await ctx.send(
                    "invalid date format!\nplease use: `!!exam -s DD-MM-YYYY`\nExample: `!!exam -s 15-04-2026`"
                )

        elif flag in ["-r", "-reset", "--reset"]:
            await ctx.send(exam_tracker.reset(ctx.author.id))

    except Exception as e:
        await ctx.send(f"error: {str(e)}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("missing a required argument! check command usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "invalid argument provided, did you type text instead of a year?"
        )
    else:
        print(f"error: {error}")
        await ctx.send("an unexpected error occurred.")


@bot.command()
async def help(ctx):
    helper = """
This bot helps you get a rough idea of BITSAT exam cutoffs for the upcoming year, please note that predictions are estimates and may not reflect actual values.

**Commands:**
- `!!plot [campus-name]` - plot marks trend for all branches in a campus
  Example: `!!plot Pilani`

- `!!plot-branch [branch-name] [campus-name]` - plot marks trend for a specific branch
  Example: `!!plot-branch Computer Science Pilani` or `!!plot-branch cse Pilani`
  Note: you can use shortcuts like `cse`, `ece`, `mech`, etc. Comma-separators are no longer needed.

- `!!select [year] [campus-name]` - shows cutoff values for a particular year in tabulated format for all or a specified campus
  Example: `!!select 2025`, `!!select 2025 pilani`

- `!!predict [campus-name] [situation]` - shows predictions for 2026 BITSAT exam with different scenarios (worst/best/most-likely)
  Example: `!!predict`, `!!predict Pilani`, `!!predict Pilani worst`

- `!!da` - get exam-shift dates for both sessions

- `!!time` - track your time till your bitsat-shift, use flags such as -s & -r for your needs
  Example: `!!time -s 15-04-2026` or `!!time -r`

- `!!ypt` - get the link, group-name & password for the official bitsatards-YPT group 

- `!!sy` - get syllabus for current BITSAT examination

- `!!resources` - get study resources for the BITSAT examination

- `!!src` - get the source code of this bot

- `!!help` - shows this help message

**Available Campuses:** Pilani, Goa, Hyderabad
**Branch Shortcuts:** cse, ece, eee, mech, civil, chem, eni, manufacturing, pharm, and more
    """
    await ctx.send(helper)


bot.run(token, log_handler=handler, log_level=logging.DEBUG)
