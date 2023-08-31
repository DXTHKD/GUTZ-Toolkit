import pypresence
import time
import colorama
from colorama import Fore, Back, init
import os
import shutil

def get_current_user():
    return os.getenv("USERNAME")

pcuser = get_current_user()

client_id = "1146057122942046270"

RPC = pypresence.Presence(client_id)
RPC.connect()

os.system("cls")

def hidecursor():
    os.system("<nul set /p=[?25l")
    
def cmd_size(columns, lines):
      command1 = f"mode con cols={columns} lines={lines}"
      os.system(command1)
      
cmd_size(46, 5)
      
center = shutil.get_terminal_size().columns
    
hidecursor()

title = '''
─── Rich Presence is running ───

This window can be minimized now.
'''

for line in title.splitlines():
    print(line.center(center))

while True:
    RPC.update(
        state="Current User: " + pcuser,
        details="───────────────#-",
        large_image="prasset1_large",
        small_image="prasset1_smalll",
        start=time.time(),
    )
    time.sleep(15)  

RPC.close()