import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
from discord import utils
from time import sleep
from win32api import GetSystemMetrics
import pyautogui
from PIL import ImageGrab
import win32gui

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

### Events
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

        if 'thomas' in message.content.lower():
            await message.channel.send(f'{message.author.mention} Thomas is currently in a __*meeting*__. Can I take a message?')
            sleep(3)
            await message.channel.send("SIKE! I won't tell him anything. He doesn't have time for your little boy problems")

        elif 'tommy' in message.content.lower():
            await message.channel.send("They call him Tommy99 aka Big T")

        if 'haha' in message.content.lower():
            await message.add_reaction(reactionEmoji)

        await client.process_commands(message)


### Commands
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
async def shutdown(ctx):
    """Shutdown/Disconnect the bot from Discord

    Args:
        ctx (obj): message context used to identify message author
    """
    if ctx.author.id == unlikely_discord_id:
        print("Bot owner called for shutdown")
        await client.logout()

@client.command()
async def screenshot(ctx, region:str = "a"):
    """Take a screenshot and send it as a message

    Args:
        ctx (obj): Message context
        region (str, optional): Screen region to capture. Defaults to "a" (all).

    Raises:
        NotImplementedError: Function that is not implemented
    """

    region = region.lower() # Convert to lowercase

    # Get screenshot of region

    # Whole screen
    if region == "a":
        pyautogui.screenshot(r"screenshot.png") # Take screenshot and save to file

    # Left side
    elif region == "l":
        # Start at 0,0
        # Get half the screen width and entire height
        pyautogui.screenshot(r"screenshot.png", region=(0,0, screen_width/2, screen_height))

    # Right side
    elif region == "r": 
        # Start top middle
        # Get the rest of right side and entire height
        pyautogui.screenshot(r"screenshot.png", region=(screen_width/2,0, screen_width/2, screen_height))
    
    # Top left
    elif region == "tl":
        raise NotImplementedError()
    
    # Top right
    elif region == "tr":
        raise NotImplementedError()

    # Bottom left
    elif region == "bl":
        raise NotImplementedError()

    # Bottom right
    elif region == "br":
        raise NotImplementedError()


    await ctx.send(file=discord.File(r"screenshot.png")) # Send screenshot

@client.command(name="ss")
async def server_status(ctx):

    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    server_window = [(hwnd, title) for hwnd, title in winlist if 'system32\cmd.exe' in title.lower()]
    print(server_window)
    server_window = server_window[0]
    hwnd = server_window[0]
    print(hwnd)

    win32gui.SetForegroundWindow(hwnd)
    bbox = win32gui.GetWindowRect(hwnd)
    print(bbox)
    img = ImageGrab.grab(bbox)
    img.save("window.png")
    
    await ctx.send(file=discord.File(r"window.png")) # Send screenshot


client.run(TOKEN)
