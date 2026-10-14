import pyautogui,time,subprocess
url='https://upcommons.upc.edu/entities/publication/dd6bc38b-8dd6-420e-8283-417714a54353'
subprocess.Popen(['cmd','/c','start','','chrome.exe',url], shell=False)
time.sleep(8)
pyautogui.moveTo(600,500)
pyautogui.scroll(-7)
time.sleep(2)
pyautogui.click(315,377)
time.sleep(10)
