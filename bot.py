import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

client = discord.Client()

reactionEmoji = "<:XDDD:748114052726652968>" # XDDD

@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guilds:')
    for guild in client.guilds:
        print(
            f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_message(message):
    if client.user.id != message.author.id:
        if "thomas schedule" == message.content.lower():            
            embedVar = discord.Embed(title="Thomas' Schedule", description="For the coming week", color=0xff0000)
            embedVar.add_field(name="Monday", value="Busy")
            embedVar.add_field(name="Tuesday", value="Very Busy")
            embedVar.add_field(name="Wednesday", value="__**Omega Busy**__")
            embedVar.add_field(name="Thurday", value="Chilling and GAMING MINECRAFT BABY WOOOOOOOOOOOOOO")
            embedVar.add_field(name="Friday", value="Doing laundry and PLAYING MINECRAFT WOOOOOO")
            embedVar.add_field(name="Saturday", value="Going home for smissmas!!")
            await message.channel.send(embed=embedVar)

        elif 'thomas' in message.content.lower():
            await message.channel.send(f'{message.author.mention} Thomas does not want to speak with you. Please fuck the fuck off.')

        elif 'tommy' in message.content.lower():
            await message.channel.send("They call him Tommy99 aka Big T")

        if 'id' == message.content.lower():
            await message.channel.send(f"{message.author.mention} Your user id is: {message.author.id}")

        if 'haha' in message.content.lower():
            await message.add_reaction(reactionEmoji)
            # await message.add_reaction("mike")


client.run(TOKEN)