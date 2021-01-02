import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
from discord import utils
from time import sleep
from win32api import GetSystemMetrics
import pyautogui

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# client = discord.Client()
client = Bot(command_prefix = ">")

# Emojos
reactionEmoji = "<:XDDD:748114052726652968>"

# Unlikely Discord ID
unlikely_discord_id = 138364425122873345

# Resolution of screen
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

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
            embedVar.add_field(name="Thursday", value="Chilling and GAMING MINECRAFT BABY WOOOOOOOOOOOOOO")
            embedVar.add_field(name="Friday", value="Doing laundry and PLAYING MINECRAFT WOOOOOO")
            embedVar.add_field(name="Saturday", value="Going home for smissmas!!")
            await message.channel.send(embed=embedVar)

        elif 'thomas' in message.content.lower():
            await message.channel.send(f'{message.author.mention} Thomas is currently in a __*meeting*__. Can I take a message?')
            sleep(3)
            await message.channel.send("SIKE! I won't tell him anything. He doesn't have time for your little boy problems")

        elif 'tommy' in message.content.lower():
            await message.channel.send("They call him Tommy99 aka Big T")

        if 'haha' in message.content.lower():
            await message.add_reaction(reactionEmoji)

        # if "s" == message.content:
        #     await client.logout()

        await client.process_commands(message)


@client.command()
async def userinfo(ctx, *, user: discord.Member = None):
    """
    Get information about you, or a specified user.

    `user`: The user who you want information about. Can be an ID, mention or name.
    """

    # await ctx.send("TEST CTX RESPONSE")

    if user is None:
        user = ctx.author

    embed = discord.Embed(
        color = user.color,
        title=f"{user.name}'s Stats and Information."
    )
    embed.set_footer(text=f"ID: {user.id}")
    embed.set_thumbnail(url=user.avatar_url_as(format="png"))
    embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user.display_name}\n"
                                                                #f"**Account created:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
                                                                f"**Status:** {user.raw_status}\n"
                                                                f"**Activity:** {user.activity}", inline=False)
    embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
                                                                        f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
                                                                        f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}") # Skips @everyone
    await ctx.send(embed=embed)

@client.command()
async def s(ctx):
    """Shutdown/Disconnect the bot from Discord

    Args:
        ctx (obj): message context used to identify message author
    """
    if ctx.author.id == unlikely_discord_id:
        print("Bot owner called for shutdown")
        await client.logout()

@client.command()
async def screenshot(ctx, region:str = "topleft"):
    print(screen_width, screen_height)

    if region == "topleft":
        pass
    elif region == "topright":
        pass
    elif region == "bottomleft":
        pass
    elif region == "bottomright":
        pass

    _sc = pyautogui.screenshot()

    await ctx.send(_sc)


client.run(TOKEN)
