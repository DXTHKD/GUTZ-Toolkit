import subprocess

def run_file(file_path):
    try:
        subprocess.run(["start", "cmd", "/k", "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", file_path], check=True)
    except subprocess.CalledProcessError:
        print(f"Error running {file_path}")