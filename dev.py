from logging import error
import os
import discord
from discord import utils
from discord.ext.commands import Bot
from discord.ext.commands.core import is_owner
from dotenv import load_dotenv
from time import sleep
import pyautogui
from PIL import Image
import pyautogui
import win32api
from win32api import GetSystemMetrics
import win32con
import win32gui
import win32ui


toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

server_window = [(hwnd, title) for hwnd, title in winlist if 'system32\cmd.exe' in title.lower()]
if len(server_window) == 0:
    print("Window not found")
    exit()

# Set window as foreground before screenshot
hwnd = server_window[0][0]
print(hwnd)
win32gui.SetForegroundWindow(hwnd)

# Get virtual screen
hwnd = win32gui.GetDesktopWindow()
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

# Get coords and calculate width and height
# startX, startY, endX, endY = bbox = win32gui.GetWindowRect(hwnd)
# l = startX
# t = startY
# w = startX - endX
# h = endY - startY
# w = w*-1 if w<0 else w  # Convert to positive if negative
# h = h*-1 if h<0 else h  # Convert to positive if negative

SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79
w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)

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
