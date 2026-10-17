import ctypes,time
from ctypes import wintypes
pid=356
wins=[]
@ctypes.WINFUNCTYPE(ctypes.c_bool,wintypes.HWND,wintypes.LPARAM)
def cb(hwnd,lparam):
    p=wintypes.DWORD()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd,ctypes.byref(p))
    if p.value==pid and ctypes.windll.user32.IsWindowVisible(hwnd):
        wins.append(hwnd)
    return True
ctypes.windll.user32.EnumWindows(cb,0)
if wins:
    h=wins[0]
    ctypes.windll.user32.ShowWindow(h,9)
    ctypes.windll.user32.SetForegroundWindow(h)
    time.sleep(0.8)
    VK_SHIFT=0x10; VK_S=0x53; KEYUP=0x0002
    ctypes.windll.user32.keybd_event(VK_SHIFT,0,0,0)
    ctypes.windll.user32.keybd_event(VK_S,0,0,0)
    ctypes.windll.user32.keybd_event(VK_S,0,KEYUP,0)
    ctypes.windll.user32.keybd_event(VK_SHIFT,0,KEYUP,0)
    time.sleep(2)
from PIL import ImageGrab
ImageGrab.grab(all_screens=True).save(r'C:\Users\dezen\Desktop\fusion_scripts.png')
print(wins)
