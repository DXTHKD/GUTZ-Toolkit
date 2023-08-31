import subprocess
import re

def get_wifi_ip():
    try:
        ipconfig_output = subprocess.check_output(["ipconfig"], universal_newlines=True)
        ip_match = re.search(r"IPv4 Address.*: (\d+\.\d+\.\d+\.\d+)", ipconfig_output)
        if ip_match:
            wifi_ip = ip_match.group(1)
            return wifi_ip
        else:
            return None
    except subprocess.CalledProcessError:
        return None

def get_wifi_ip_ping_time():
    wifi_ip = get_wifi_ip()
    if wifi_ip is None:
        return None

    try:
        output = subprocess.check_output(["ping", "-c", "1", wifi_ip], universal_newlines=True)
        time_match = re.search(r"time=([\d.]+) ms", output)
        if time_match:
            ping_time = float(time_match.group(1))
            return ping_time
        else:
            return None
    except subprocess.CalledProcessError:
        return None
