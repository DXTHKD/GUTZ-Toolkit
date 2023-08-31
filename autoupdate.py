import requests
import os
import subprocess

GITHUB_USER = "DXTHKD"
GITHUB_REPO = "GUTZ-Toolkit"
GITHUB_TOKEN = os.environ.get("GIIITHUB_TOKEN")  # Access the secret via environment variable

CURRENT_VERSION = "1.0.1"

def get_latest_release_version():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    data = response.json()
    latest_version = data["tag_name"]
    return latest_version

def update_project():
    latest_version = get_latest_release_version()

    if latest_version != CURRENT_VERSION:
        print(f"New version available: {latest_version}")
        user_input = input("Do you want to update? (y/n): ").lower()

        if user_input == "y":
            subprocess.run(["wget", f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/latest/download/GUTZ-Toolkit.zip"])
            subprocess.run(["unzip", "GUTZ-Toolkit.zip"])
            subprocess.run(["rm", "GUTZ-Toolkit.zip"])