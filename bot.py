from logging import error
import os
import discord
from discord import utils
from discord.ext.commands import Bot
from discord.ext.commands.core import is_owner
from dotenv import load_dotenv
from time import sleep
# import pyautogui
from PIL import Image
import pyautogui
import win32api
from win32api import GetSystemMetrics
import win32con
import win32gui
import win32ui

### Search for tags
# (TBD) - To be determined
# (TODO) - To do 

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# client = discord.Client()
client = Bot(command_prefix = ">")

# Emojos
emoji_xddd = "<:XDDD:748114052726652968>"

# Resolution of screen
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

# Bot owner ID:
owner_id = 138364425122873345




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

    if ctx.author.id == owner_id:
        print("Bot owner called for shutdown")
        await client.logout()
    else:
        print("Only the owner can shut down the bot via that command!")

@client.command(name="ss")
async def screenshot(ctx, monitor:int=None, message:str=None):
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

        w, h, l, t = get_screen_resolution()

        if monitor is None:
            return w, h, l, t

        ## Assumes monitor is 1920 pixels wide
        monitors_start = []
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
    if message is None:
        if monitor is None:
            await ctx.send(content=f"All monitors @{w}x{h}, {l},{t}", file=discord.File(r"screencapture.png"))
        else:
            await ctx.send(content=f"Monitor {monitor} @{w}x{h}, {l},{t}", file=discord.File(r"screencapture.png"))
    else:
        if monitor is None:
            await ctx.send(content=f"{message}All monitors @{w}x{h}, {l},{t}", file=discord.File(r"screencapture.png"))
        else:
            await ctx.send(content=f"{message}Monitor {monitor} @{w}x{h}, {l},{t}", file=discord.File(r"screencapture.png"))

@client.command("server")
async def server(ctx, command:str="status", *args):
    command = command.lower()

    print(args)

    if command == "status":
        # server_status()
        await server_status(ctx, *args)

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




###########################################################
######################## Functions ########################
###########################################################

def is_server_running():
    """Checks if server is running or not by looking for system window

    Returns:
        bool, hwnd: Boolean for whether or not the server is running, hwnd for the window if it exists
    """

    toplist, winlist = [], []
    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
    win32gui.EnumWindows(enum_cb, toplist)

    server_window = [(hwnd, title) for hwnd, title in winlist if 'system32\cmd.exe' in title.lower()]
    if len(server_window) == 0:
        return False, None
    else:
        return True, server_window[0][0]

def determine_monitor(x1, x2, w, l):
    """Tries to determine which monitor any given window is located on

    Args:
        x1 (int): x coordinate 1
        x2 (int): x coordinate 2
        w (int): width of all monitors together
        l (int): monitor start coordinate

    Returns:
        (int): Integer representing the monitor on which the window is located
    """

    monitor = None

    ## Assumes monitor is 1920 pixels wide
    monitors_start = []
    for _ in range(1, (w//1920)+2):
        monitors_start.append(l)
        l += 1920

    try:
        for index, xVal in enumerate(monitors_start):
            if x1 in range(xVal, monitors_start[index+1]) and x2 in range(xVal, monitors_start[index+1]):
                monitor = index+1
                print("Server window found on monitor", monitor)
                return monitor
    except Exception as ex:
        print("Could not find window on any monitor")
    
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

async def server_status(ctx, *args):
    """Send a message containing the status of the server (online/offline)
        add system resources used in message later (TODO)
    """

    # Check if server is running. Gets status and window handle
    # Assumes server window is the only window with 'system32\cmd.exe' in its name
    _status, hwnd = is_server_running()
    print(hwnd)

    # If server is running
    if _status == True:
        message = "Window was located.\n"
        message += "Server is running.\n"

        # Get screen details
        w, h, l, t = get_screen_resolution()

        # Get window details
        x1, y1, x2, y2 = bbox = win32gui.GetWindowRect(hwnd)
        print("Console window bbox:", bbox)
        monitor = determine_monitor(x1, x2, w, l)
        

        if "fullscreen" in args:
            message += f"Console Window location: Monitor {monitor}.\n"
            window_prepare_for_screenshot(hwnd)
            sleep(0.2)
        else:
            message += f"Console Window location: {bbox}.\n"

        try:
            await screenshot(ctx=ctx, monitor=monitor, message=message) # Take and send screenshot
            if "fullscreen" in args:
                window_restore_from_pre_screenshot(hwnd) # Restore window position
        except Exception as ex:
            await ctx.send(content=f"{message}Could not send screenshot because of error: {ex}")

    else:
        await ctx.send(content=f"Server window could not be located. Server is not running")

    return None

def server_start(): # (TODO)
    """Start the server if it is not running
    """

    print("Starting server...")

    # open cmd
    pyautogui.hotkey("win","r")
    sleep(0.4)
    pyautogui.typewrite("cmd\n")
    sleep(0.5)


    return None

def server_save(): # (TODO)
    """Save the world!
        Send an image of the console after command has gone through
    """
    return None

def server_stop(): # (TODO)
    """Stop the server.
        Should always call server_save() before stopping server
    """
    return None    

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

def get_screen_resolution():
    SM_XVIRTUALSCREEN = 76
    SM_YVIRTUALSCREEN = 77
    SM_CXVIRTUALSCREEN = 78
    SM_CYVIRTUALSCREEN = 79
    vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
    vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
    vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
    vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)

    return vscreenwidth, vscreenheigth, vscreenx, vscreeny


client.run(TOKEN)
