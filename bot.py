from ctypes.wintypes import PULARGE_INTEGER
import logging
import os
import discord
from discord import utils
from discord.ext.commands import Bot
from dotenv import load_dotenv
from time import sleep
import pyautogui
from PIL import Image
import pyautogui
import win32api
import win32con
import win32gui
import win32ui
from statistics import median

### Search for tags
# (TBD) - To be determined
# (TODO) - To do 

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# client = discord.Client()
client = Bot(command_prefix = ">")

# Emojos
emoji_xddd = "<:XDDD:748114052726652968>"

# Bot owner ID:
OWNER_ID = 138364425122873345

# Server window name
SERVER_WINDOW_NAME = r"system32\cmd.exe"



########################################################
######################## Events ########################
########################################################

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
            await message.add_reaction(emoji_xddd)

        if message.author.id == 243846951005716480:
            await message.add_reaction("🕖")


        await client.process_commands(message)



##########################################################
######################## Commands ########################
##########################################################

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

@client.command(name="dc")
async def shutdown(ctx):
    """Shutdown/Disconnect the bot from Discord

    Args:
        ctx (obj): message context used to identify message author
    """

    if ctx.author.id == OWNER_ID:
        print("Bot owner called for shutdown")
        await client.logout()
    else:
        print("Only the owner can shut down the bot via that command!")

@client.command(name="screenshot")
async def screenshot(ctx, monitor:int=None):
    w, h, l, t = get_bbox_monitor(monitor)
    img = screen_capture(w, h, l, t)
    
    # Send message and image
    if monitor is None:
        await ctx.send(content=f"All monitors", file=img)
    else:
        await ctx.send(content=f"Monitor {monitor}", file=img)

@client.command("server")
async def server(ctx, *args):
    command = args[0].lower()

    print(f"Server command invoked, args: {args}")

    if command == "console":
        await server_console(ctx, *args[1:])

    elif command == "view":
        hwnd = get_hwnd(SERVER_WINDOW_NAME)
        console_img = window_capture(hwnd)

        if console_img is None:
            await ctx.send(content="Could not get console window")
        else:
            await ctx.send(file=console_img)

    elif command == "start":
        # server_start() (TODO)
        raise NotImplementedError()
        await server_start(ctx)

    elif command == "save":
        # server_start() (TODO)
        raise NotImplementedError()
        await server_save(ctx)

    elif command == "stop":
        # server_stop() (TODO)
        raise NotImplementedError()
        await server_stop(ctx)
    
    elif command == "crashcheck" or command == "crashtest":
        crash = await crashcheck(ctx)
        if crash is False:
            await ctx.send(content="Server is running and survived crashtest", file=discord.File(r"screencapture.png"))



###########################################################
######################## Functions ########################
###########################################################

def screen_capture(width, height, left, top):
    img = None

    if width == height == left == top == 0:
        width, height, left, top = get_screen_resolution()
    try:
        print(width, type(width))
        print(height, type(height))
        print(left, type(left))
        print(top, type(top))

        hwin = win32gui.GetDesktopWindow()
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
        bmpinfo = bmp.GetInfo()
        bmpstr = bmp.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        im.save('screencapture.png', format = 'png')
        img = get_screenshot(r"screencapture.png")
    except Exception as ex:
        logging.error(f"Could not take screenshot because {ex}")
    return img


def window_capture(hwnd:int, visible:bool=False):
    img = None

    try:
        l, t, r, b = get_bbox_hwnd(hwnd)
        w = r - l
        h = b - t
        print("window_capture:", l, t, r, b, w, h)
        hwin = win32gui.GetDesktopWindow()
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, w, h)
        memdc.SelectObject(bmp)
        if visible is False:
            window_set_foreground(hwnd)
        memdc.BitBlt((0, 0), (w, h), srcdc, (l, t), win32con.SRCCOPY)
        bmpinfo = bmp.GetInfo()
        bmpstr = bmp.GetBitmapBits(True)
        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
        im.save('screencapture.png', format = 'png')
        img = get_screenshot(r"screencapture.png")
    except Exception as ex:
        logging.error(f"Could not take screenshot because {ex}")
    return img


def get_screenshot(path:str=r"screencapture.png"):
    img = None
    try:
        img = discord.File(path)
    except Exception as ex:
        logging.error(f"Could not get image from path '{path}'. Got {ex}")
    return img


def window_set_foreground(hwnd):
    win32gui.ShowWindow(hwnd,6) # Minimize (hide window)
    win32gui.ShowWindow(hwnd,9) # Un-minimize
    sleep(0.2)


def get_bbox_hwnd(hwnd:int=None):
    # Get the bbox of given window handle or monitor
    bbox = None

    try:
        bbox = win32gui.GetWindowRect(hwnd) # x1, y1, x2, y2 
    except Exception as ex:
        logging.error(f"Could not get bbox for hwnd '{hwnd}'. Got {ex}")

    return bbox


def get_bbox_monitor(monitor:int=None):
        w, h, l, t = bbox = get_screen_resolution()

        if monitor is None:
            return bbox

        ## Assumes monitor is 1920 pixels wide
        monitors_start = []
        for _ in range(1, (w//1920)+1):
            monitors_start.append(l)
            l += 1920

        l = monitors_start[monitor-1]

        return int(w/len(monitors_start)), h, l, t


def get_hwnd(window_name:str="system32\cmd.exe"):
    # Get window handle of given window name
    hwnd = None

    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    windows = [(hwnd, title) for hwnd, title in winlist if window_name in title.lower()]

    try:
        hwnd = windows[0][0]
    except Exception as ex:
        logging.error(f"Could not get window handle (hwnd) for {window_name}. Because {ex}")

    if len(windows) == 0:
        return hwnd
    else:
        return hwnd


def get_monitor(window_x1, window_x2, screen_width, screen_start):
    # Get monitor number given a bbox
    monitor = None
    
    ## Assumes monitor is 1920 pixels wide
    monitors_start = []
    for _ in range(1, (screen_width//1920)+2):
        monitors_start.append(screen_start)
        screen_start += 1920

    try:
        for index, xVal in enumerate(monitors_start):
            if window_x1 in range(xVal, monitors_start[index+1]) and \
                window_x2 in range(xVal, monitors_start[index+1]):
                monitor = index+1
                return monitor
    except Exception:
        if window_x1 == -1928 and window_x2 == -8 or \
            window_x1 == -1928 and window_x2 == 8:
            return 1

    return monitor


def window_prepare_for_screenshot(hwnd):
    win32gui.ShowWindow(hwnd, 6) # Minimize
    win32gui.ShowWindow(hwnd, 3) # Fullscreen

    # win32gui.ShowWindow(hwnd,0) # Closes window fully (but can still be recovered by 1)
    # win32gui.ShowWindow(hwnd,1) # Brings window to front (recovers window from 0)
    # win32gui.ShowWindow(hwnd,2) # Minimize (hide)
    # win32gui.ShowWindow(hwnd,3) # Fullscreen (not toggle, brings window to front if hidden)
    # win32gui.ShowWindow(hwnd,4) # Exit fullscreen (brings window to front if hidden)
    # win32gui.ShowWindow(hwnd,5) # Nothing?
    # win32gui.ShowWindow(hwnd,6) # Minimize (hide window)
    # win32gui.ShowWindow(hwnd,7) # Minimize (hide window)
    # win32gui.ShowWindow(hwnd,8) # Nothing?
    # win32gui.ShowWindow(hwnd,9) # Un-minimize
    # win32gui.ShowWindow(hwnd,10) # Small window in front (brings window to front if not visible and exits fullscreen if in fullscreen)


def window_restore_from_pre_screenshot(hwnd):
    win32gui.ShowWindow(hwnd,1)


def get_screen_resolution():
    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    SM_CXVIRTUALSCREEN = 78
    SM_CYVIRTUALSCREEN = 79
    w = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    h = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    l = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
    t = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)

    return w, h, l, t


def get_emote(emoji):
    """
    Gets a specific emote by lookup.
    :param emoji: The emote to get.
    :type emoji: str or discord.Emoji
    :return:
    :rtype: (str, int)
    """
    import re
    lookup, eid = emoji, None
    if ':' in emoji:
        # matches custom emote
        server_match = re.search(r'<a?:(\w+):(\d+)>', emoji)
        # matches global emote
        custom_match = re.search(r':(\w+):', emoji)
        if server_match:
            lookup, eid = server_match.group(1), server_match.group(2)
        elif custom_match:
            lookup, eid = custom_match.group(1), None
        else:
            lookup, eid = emoji.split(':')
        try:
            eid = int(eid)
        except (ValueError, TypeError):
            eid = None
    return lookup, eid


def window_exists(window_name):
    hwnd = get_hwnd(window_name=window_name)
    exists = True if hwnd != None else False

    return exists


async def server_console(ctx, *args):
    visible = False
    if "stop" in args:
        await ctx.send(content="Please use `>server stop` instead. Only admins can close the server")
        return None

    if "visible" in args[0]:
        visible = True
    
    # Check if server is running
    if window_exists(SERVER_WINDOW_NAME) is False:
        logging.info("Server window could not be found")
        await ctx.send(content="Cannot send console commands when the server is offline.")
        return None

    # Get window details
    hwnd = get_hwnd(SERVER_WINDOW_NAME)
    l, t, r, b = get_bbox_hwnd(hwnd)

    if visible is False:
        # Set window to foreground
        window_set_foreground(hwnd)

    # Take screenshot of console window
    img = window_capture(hwnd, visible=visible)

    # Click in the middle of the monitor
    x = int(median([r, l]))
    y = int(median([t, b]))
    pyautogui.leftClick(x, y)

    # Wait a little
    sleep(0.5)

    # Check if server has crashed
    pyautogui.typewrite(" ") # This will completely close the window if something is wrong
    sleep(0.5)

    # Try again to locate window
    try:
        l, t, r, b = win32gui.GetWindowRect(hwnd)
    except Exception as ex:
        await ctx.send(
            content=f"Server did not survive crashcheck. It likely crashed a while ago. Got error {ex}",
            file=img)
        return None
    
    # Start new line if server is still alive
    pyautogui.typewrite("\n")
    if visible is False:
        for arg in args:
            pyautogui.typewrite(str(arg) + " ")
            sleep(0.1)
    else:
        for arg in args[1:]:
            pyautogui.typewrite(str(arg) + " ")
            sleep(0.1)

    pyautogui.typewrite(['backspace'])

    # Execute command
    pyautogui.typewrite("\n")

    sleep(1.5)
    img = window_capture(hwnd, visible=visible)

    # Tell user that commands went through
    content = f"Successfully ran `{str().join([(str(arg)+' ') for arg in args])}`" if visible is False else f"Successfully ran `{str().join([(str(arg)+' ') for arg in args[1:]])}`"
    await ctx.send(
        content=content,
        file=img
    )
  

async def crashcheck(ctx):
    crash = False

    # Check if server is running
    if window_exists(SERVER_WINDOW_NAME) is False:
        logging.info("Server window could not be found")
        await ctx.send(content="Cannot send console commands when the server is offline.")
        return None

    # Get window details
    hwnd = get_hwnd(SERVER_WINDOW_NAME)
    l, t, r, b = get_bbox_hwnd(hwnd)

    # Set window to foreground
    window_set_foreground(hwnd)

    # Take screenshot of console window
    img = window_capture(hwnd)

    # Click in the middle of the monitor
    x = int(median([r, l]))
    y = int(median([t, b]))
    pyautogui.leftClick(x, y)

    # Wait a little
    sleep(0.5)

    # Check if server has crashed
    pyautogui.typewrite(" ") # This will completely close the window if something is wrong
    sleep(0.5)

    # Try again to locate window
    try:
        l, t, r, b = win32gui.GetWindowRect(hwnd)
    except Exception as ex:
        crash = True
        await ctx.send(
            content=f"Server did not survive crashcheck. It likely crashed a while ago. Got error {ex}",
            file=img)
        return crash

    # New line
    pyautogui.typewrite("\n")
    return crash
    


client.run(TOKEN)
