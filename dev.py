from PIL import Image
import win32gui, win32ui, win32api, win32con

# Get entire virtual screen
hwnd = win32gui.GetDesktopWindow()

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

print(w, h, l, t, r, b)

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
print(bmpinfo)
bmpstr = saveBitMap.GetBitmapBits(True)

# Save image
im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
im.save('screencapture.png', format = 'png')