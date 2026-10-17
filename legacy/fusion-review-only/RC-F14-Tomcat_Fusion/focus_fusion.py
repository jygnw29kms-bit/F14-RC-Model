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
print(wins)
for h in wins:
    ctypes.windll.user32.ShowWindow(h,9)
    ctypes.windll.user32.SetForegroundWindow(h)
time.sleep(1)
