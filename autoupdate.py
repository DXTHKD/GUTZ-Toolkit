import requests
import os
import subprocess
import zipfile
import shutil

GITHUB_USER = "DXTHKD"
GITHUB_REPO = "GUTZ-Toolkit"
GITHUB_TOKEN = os.environ.get("GIIITHUB_TOKEN")  # Access the secret via environment variable

CURRENT_VERSION = "1.0.3"

def get_latest_release_version():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    data = response.json()
    latest_version = data["tag_name"]
    return latest_version

import zipfile
import os

def update_project():
    latest_version = get_latest_release_version()

    if latest_version != CURRENT_VERSION:
        print(f"New version available: {latest_version}")
        user_input = input("Do you want to update? (y/n): ").lower()

        if user_input == "y":
            zip_url = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/archive/refs/tags/{latest_version}.zip"
            zip_filename = f"GUTZ-Toolkit-{latest_version}.zip"
            
            subprocess.run(["curl", "-LO", zip_url])
            
            with zipfile.ZipFile(zip_filename, "r") as zip_ref:
                # Extract contents to a consistent folder name
                extracted_folder = f"{GITHUB_REPO}-extracted"
                zip_ref.extractall(extracted_folder)
            
            # Move contents of the extracted folder to the current directory
            for item in os.listdir(extracted_folder):
                item_path = os.path.join(extracted_folder, item)
                if os.path.isfile(item_path):
                    shutil.move(item_path, ".")
            
            # Remove the extracted folder
            shutil.rmtree(extracted_folder)
            
            os.remove(zip_filename)
            
update_project()
