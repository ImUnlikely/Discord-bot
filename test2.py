from logging import error, exception
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

def window_set_foreground(hwnd):
    win32gui.ShowWindow(hwnd,6) # Minimize (hide window)
    win32gui.ShowWindow(hwnd,9) # Un-minimize
    sleep(0.25)

hwin = win32gui.GetDesktopWindow()
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
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


print(width, type(width))
print(height, type(height))
print(left, type(left))
print(top, type(top))

print(width == height == left == top == 0)