import requests
import os
import subprocess
import zipfile
import shutil
import time
import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL('user32')

MB_OK = 0x00000000
MB_ICONERROR = 0x00000010
MB_ICONINFORMATION = 0x00000040
MB_ICONWARNING = 0x00000030
MB_ICONQUESTION = 0x00000020
MB_YESNO = 0x00000004

GITHUB_USER = "DXTHKD"
GITHUB_REPO = "GUTZ-Toolkit"
GITHUB_TOKEN = os.environ.get("GIIITHUB_TOKEN")  # Access the secret via environment variable

CURRENT_VERSION = "v1.0.2"

def get_latest_release_version():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    data = response.json()
    latest_version = data["tag_name"]
    return latest_version

def update_project():
    latest_version = get_latest_release_version()

    if latest_version == CURRENT_VERSION:
        print("aight")
        ctypes.windll.user32.MessageBoxW(0, "No update available.", "Update Check", 0)
    else:
        result = ctypes.windll.user32.MessageBoxW(0, f"Theres a new version of GUTZ available ({latest_version}). \n\nDo you want to update?", f"GUTZ {CURRENT_VERSION} - Update", 4)
        
        if result == 6:  # Yes button was clicked
            zip_url = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/download/{latest_version}/gutz-toolkit.zip"
            zip_filename = f"gutz-toolkit.zip"
            temp_folder = "temp_extracted_folder"
            
            subprocess.run(["curl", "-LO", zip_url])
            
            with zipfile.ZipFile(zip_filename, "r") as zip_ref:
                zip_ref.extractall(temp_folder)
                
            time.sleep(2)
            
            for item in os.listdir("."):
                if os.path.isdir(item) and item != temp_folder:
                    shutil.rmtree(item)
                elif os.path.isfile(item) and item != "autoupdate.py":
                    os.remove(item)
                    
            time.sleep(2)
            
            for item in os.listdir(temp_folder):
                if item != "autoupdate.py":
                    item_path = os.path.join(temp_folder, item)
                    shutil.move(item_path, ".")
                    
            time.sleep(2)
            
            shutil.rmtree(temp_folder)
            
            time.sleep(3)
            
            ctypes.windll.user32.MessageBoxW(0, f"Succesfully updated!", f"GUTZ", MB_OK)

            
update_project()