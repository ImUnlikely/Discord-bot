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
from statistics import median


# print(pyautogui.KEYBOARD_KEYS)
# print(pyautogui.KEY_NAMES)

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)

windows = [(hwnd, title) for hwnd, title in winlist if "notepad" in title.lower()]

hwnd = windows[0][0]


# Get desktop window hwnd
# hwnd = win32gui.GetDesktopWindow()
# print(hwnd)
 
# you can use this to capture only a specific window
l, t, r, b = win32gui.GetWindowRect(hwnd)
w = r - l
h = b - t
 
# get complete virtual screen including all monitors
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79
w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
r = l + w
b = t + h
 
print(l, t, r, b, ' -> ', w, h)
 
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()
 
saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
saveDC.SelectObject(saveBitMap)
saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)
bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)

# Save image
im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
im.save('screencapture.png', format = 'png')

