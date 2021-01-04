import os
import discord
from discord import utils
from discord.ext.commands import Bot
from dotenv import load_dotenv
from time import sleep
import pyautogui
from PIL import Image
import win32api
from win32api import GetSystemMetrics
import win32con
import win32gui
import win32ui

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

@client.command(name="ss", )
async def screenshot(ctx, monitor:int=None):
    """Takes and sends a screenshot of any given monitor. Sends screenshot of all monitors if nothing is specified

    Args:
        ctx (obj): The message context
        monitor (int, optional): The monitor to screenshot (from 1 and up). Defaults to None.
    """

    def get_monitor_bbox(monitor:int=None):
        """Gets specified monitor bounding box (assumes monitors are 1920x1080)

        Args:
            monitor (int, optional): The monitor to screenshot (from 1 and up). Defaults to None.

        Returns:
            w, h, l, t: The resolution and starting coordinates of any given monitor
        """
        SM_XVIRTUALSCREEN = 76
        SM_YVIRTUALSCREEN = 77
        SM_CXVIRTUALSCREEN = 78
        SM_CYVIRTUALSCREEN = 79
        w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
        l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
        t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)

        if monitor is None:
            return w, h, l, t

        ## Assumes monitor is 1920 pixels wide
        monitors_start = []
        # _is_negative = True if w<0 else False
        for _ in range(1, (w//1920)+1):
            monitors_start.append(l)
            l += 1920
        print(monitors_start)

        l = monitors_start[monitor-1]

        return int(w/len(monitors_start)), h, l, t

    w, h, l, t = get_monitor_bbox(monitor)
    print(w, h, l, t)

    # Get virtual screen
    hwnd = win32gui.GetDesktopWindow()

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    # Create bitmap
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)

    # Save bitmap
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    # Save image
    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    im.save('screencapture.png', format = 'png')
    
    # Send message and image
    if monitor is None:
        await ctx.send(content=f"All monitors @{w}x{h}, {l},{t}", file=discord.File(r"screencapture.png"))
    else:
        await ctx.send(content=f"Monitor {monitor} @{w}x{h}, {l},{t}", file=discord.File(r"screencapture.png"))



client.run(TOKEN)
