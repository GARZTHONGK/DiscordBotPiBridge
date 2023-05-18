import multiprocessing

import discord
import responses
from discord import app_commands
import json
import commands
import subprocess
import time
import os
import signal


def get_token(): # gets token from config.json
    print("getting Token")
    with open("config.json", 'r') as file:
        data = json.loads(file.read())
    return data["token"]


def convert_from_hours(hours):
    return hours * 3600  # returns time in seconds


def run_file():
    try:
        cmdline = r"C:\Users\alber\DiscordBotPiBridge\ProgramToRun\testing exe file\Hello world.exe"
        print("starting process")
        process = subprocess.Popen(cmdline)
        print("sleeping")
        time.sleep(5)
    except Exception as e:
        print(e)
        return f"Error executing file!, {e}"
    return "Executing file succeeded"


def start_process():
    try:
        cmdline = r"C:\Users\alber\DiscordBotPiBridge\ProgramToRun\testing exe file\Hello world.exe"
        print("starting process")
        process = subprocess.Popen(cmdline)
        time.sleep(1)
        print(process.pid)
        # process.terminate()
        return process.pid
    except Exception as e:
        print(e)
        return


def start_process_timed(hours):
    duration = convert_from_hours(hours)
    pid = start_process()
    time.sleep(duration)
    kill_process(pid)

def kill_process(processpid):
    try:
        print(f"terminating process, pid:{processpid}")
        os.kill(processpid, signal.SIGTERM)
    except Exception as e:
        print(e)
        return


def get_all_pids():
    pids = multiprocessing.active_children()
    print(pids)
    return pids


async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as e:
        print(e)


def run_discord_bot():
    token = get_token()
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    processpid = None

    @tree.command(name="testcommand", description="My first application Command", guild=discord.Object(id=1054466267744051310))  # Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
    async def first_command(interaction):
        await interaction.response.send_message("Hello!")
        print("testing arad")

    @tree.command(name="testcommand2", description="test 2", guild=discord.Object(id=1054466267744051310))
    async def second_command(interaction):
        await interaction.response.send_message("hello 2")

    @tree.command(name="sleep5", description="sleeps for 5 seconds", guild=discord.Object(id=1054466267744051310))
    async def third_command(interaction):
        await interaction.response.send_message("Gonna sleep for 5 seconds")
        print("have slept for 5 seconds")

    @tree.command(name="start_program", description="runs a specific file", guild=discord.Object(id=1054466267744051310))
    async def fourth_command(interaction):
        processpid = start_process()

        print("pricess pid = ", processpid)
        await interaction.response.send_message(f"Starting program PID ID:{processpid}")

    @tree.command(name="kill_program", description="kills a program", guild=discord.Object(id=1054466267744051310))
    async def fifth_command(interaction, pidid: int):
        print("process pid = ", processpid)
        kill_process(pidid)
        await interaction.response.send_message("Killed program")

    @tree.command(name="start_program_timed", description="runs the program for a specific amount of time", guild=discord.Object(id=1054466267744051310))
    async def sixth_command(interaction, hours: float):
        print("Running program for ", hours, " hours")
        await interaction.response.send_message(f"Starting program, will end in {hours} hours")
        start_process_timed(hours)




    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=1054466267744051310))
        print(f"{client.user} is now running!")

    @client.event
    async def on_message(message):
        if message.author == client.user:  # checks if the message is sent by the bot
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said '{user_message}' in '{channel}'")

    client.run(token)
