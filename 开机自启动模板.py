# 本程序会将自己添加进开机启动项
from __future__ import print_function
import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    PaTh = sys.argv[0]
    with open("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\启动.bat" ,mode="w") as f:
        f.write(f'start {PaTh}')
else:
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
