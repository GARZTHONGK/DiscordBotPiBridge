import discord
import responses
from discord import app_commands
import json
import commands


def get_token():
    with open("config.json", 'r') as file:
        data = json.loads(file.read())
    return data["token"]



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
