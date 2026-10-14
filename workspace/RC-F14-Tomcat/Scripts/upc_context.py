import pyautogui,time
# focus Chrome UPC page
pyautogui.click(600,350)
pyautogui.press('end')
time.sleep(2)
pyautogui.rightClick(320,364)
time.sleep(1)
pyautogui.screenshot(r'C:\Users\dezen\Desktop\upc_context.png')
