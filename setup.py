import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"
exe = Executable(script = "main.py", base = base)
path = r"C:\Users\uk982\anaconda3\zlib.dll"

setup(
    name = 'KYNCounter2',#作成するexeファイルの名前
    version = '0.1',
    description = 'Counter that records the number of wins, losses and winning streaks.',
    options = {
        "build_exe":{
            "include_files" : [
                (path, "zlib.dll"),
                "conf"
            ]
        }
    },
    executables = [exe]
)