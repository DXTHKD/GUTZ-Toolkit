#         .                  .-.    .  _   *     _   .
#                *          /   \     ((       _/ \       *    .
#              _    .   .--'\/\_ \     `      /    \  *    ___
#          *  / \_    _/ ^      \/\'__        /\/\  /\  __/   \ *
#            /    \  /    .'   _/  /  \  *' /    \/  \/ .`'\_/\   .
#       .   /\/\  /\/ :' __  ^/  ^/    `--./.'  ^  `-.\ _    _:\ _
#          /    \/  \  _/  \-' __/.' ^ _   \_   .'\   _/ \ .  __/ \
#        /\  .-   `. \/     \ / -.   _/ \ -. `_/   \ /    `._/  ^  \
#       /  `-.__ ^   / .-'.--'    . /    `--./ .-'  `-.  `-. `.  -  `.
#     @/        `.  / /      `-.   /  .-'   / .   .'   \    \  \  .-  \%
#     @&8jgs@@%% @)&@&(88&@.-_=_-=_-=_-=_-=_.8@% &@&&8(8%@%8)(8@%8 8%@)%
#     @88:::&(&8&&8:::::%&`.~-_~~-~~_~-~_~-~~=.'@(&%::::%@8&8)::&#@8::::
#     `::::::8%@@%:::::@%&8:`.=~~-.~~-.~~=..~'8::::::::&@8:::::&8:::::'
#      `::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::.'
#
#                 #################
#                 # Script by rvt #
#                 #################
#                 # ver 1.0       #
#                 #################

#############
# <imports> #
#############
import pystyle
from pystyle import Colors, Colorate, Write, Center, Add, Box
import os
import ctypes
from ctypes import wintypes
from c_modules.hide_n_show_cursor import hidecursor, showcursor
from c_modules.dir_utils import create_directory_if_not_exists
from c_modules.get_current_ping import get_wifi_ip_ping_time
from c_modules.file_runner import run_file
import time
import subprocess
import re
import requests
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil
import json
import random
import string
import logging
import version
##############
# </imports> #
##############

###############
# auto update #
###############

###########
# <setup> #
###########

script_dirrr = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dirrr)

def get_current_user():
    return os.getenv("USERNAME")

pcuser = get_current_user()

log_filename = f"{pcuser}-logs.txt"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=log_filename,
    filemode="w"
)

logging.info(f"{pcuser} - started GUTZ V1")

main_banner = '''
      █████████  █████  █████ ███████████ ███████████            ███████████ █████   ████   
     ███░░░░░███░░███  ░░███ ░█░░░███░░░█░█░░░░░░███            ░█░░░███░░░█░░███   ███░ 
    ███     ░░░  ░███   ░███ ░   ░███  ░ ░     ███░             ░   ░███  ░  ░███  ███   
   ░███          ░███   ░███     ░███         ███     ██████████    ░███     ░███████    
   ░███    █████ ░███   ░███     ░███        ███     ░░░░░░░░░░     ░███     ░███░░███   
   ░░███  ░░███  ░███   ░███     ░███      ████     █               ░███     ░███ ░░███  
    ░░█████████  ░░████████      █████    ███████████               █████    █████ ░░████
     ░░░░░░░░░    ░░░░░░░░      ░░░░░    ░░░░░░░░░░░               ░░░░░    ░░░░░   ░░░░ 
'''

login_banner = '''
    |    /  \ / _` | |\ |    
    |___ \__/ \__> | | \| 
'''

webhooks = {}

def generate_random_id():
    return ''.join(random.choices(string.digits, k=6))

def load_webhooks(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}

def save_webhooks(filename):
    with open(filename, "w") as file:
        json.dump(webhooks, file, indent=4)

def send_webhook_message(webhook_url, message_content):
    payload = {
        "content": message_content
    }
    
    response = requests.post(webhook_url, json=payload)
    
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print("Failed to send message. Status code:", response.status_code)
        print(response.text)
        
def list_webhook_ids():
    for webhook_id, webhook_url in webhooks.items():
        print(f" {webhook_id}: {webhook_url}")
        
def delete_webhook(webhook_id):
    if webhook_id in webhooks:
        del webhooks[webhook_id]
        save_webhooks("webhooks.json")
        print(Colorate.Color(Colors.red, " Done.", True))
    else:
        print(" Invalid webhook ID.")
    
user32 = ctypes.WinDLL('user32')

MB_OK = 0x00000000
MB_ICONERROR = 0x00000010
MB_ICONINFORMATION = 0x00000040
MB_ICONWARNING = 0x00000030
MB_ICONQUESTION = 0x00000020
MB_YESNO = 0x00000004

def cmd_size(columns, lines):
  command1 = f"mode con cols={columns} lines={lines}"
  os.system(command1)
  
def clear_cmd():
  command2 = f"cls"
  os.system(command2)
  
def simulate_typing(text, delay=0.05):
  for char in text:
    print(char, end='', flush=True) 
    time.sleep(delay)
    
def cmd_title(new_title):
    title_text = new_title.replace("|", "^|")
    command3 = "title " + title_text
    os.system(command3)

def parse_port_range(port_range):
    match = re.match(r'^(\d+)-(\d+)$', port_range)
    if match:
        start_port = int(match.group(1))
        end_port = int(match.group(2))
        return start_port, end_port
    else:
        raise ValueError(" Invalid port range format.")
      
tui_ops = '''
                                          ┌ MAIN ┐
     ┌────────────────────────────────────┴──────┴────────────────────────────────────┐
     │ [1] Port Scanner                                                               │
     │ [2] Web-Vulnerability Checker                                                  │
     │ [3] IP Lookup                                                                  │
     │ [4] Get WIFI SSIDs                                                             │
     └────────────────────────────────────────────────────────────────────────────────┘
        [H] - Help                      [A] - About                       [E] - Exit   
'''

main_dir = os.getcwd()

user_inputs = [
   "Username",
   "Password",
   "Search queries",
   "Comments",
   "25",
   "10",
   "99.99",
   "2000-01-01",
   "2023-08-22",
   "14:30",
   "Country",
   "Male",
   "Technology",
   "Yes",
   "Disagree",
   "option1,option2",
   "image.jpg",
   "https://example.com",
   "user@example.com",
   "Long description goes here.",
   "42.3601, -71.0589",
   "123-456-7890",
   "@example_user",
   "api_key_here",
   "4111111111111111"
]
############
# </setup> #
############

def add_bg():
  subdirectory_name = "cmdbkg_files"
  new_dir = os.path.join(main_dir, subdirectory_name)
  os.chdir(new_dir)
  os.system("cmdbkg bg.bmp /t 5")
  os.chdir(main_dir)
  logging.info(f"added background")
  
add_bg()
 
def login_tui():
  showcursor()
  ping_time = get_wifi_ip_ping_time()
  cmd_title(f"GUTZ V1.0 | Ping: {ping_time}ms")
  if str(ping_time) == "None":
    cmd_title(f"GUTZ V1.0 | error_checking_ping")
  def login(username, password):
    if username == "root" and password == "root":
      logging.info(f"{pcuser} logged in as {username} with password: {password}")
      main_menu()
    else:
      ctypes.windll.user32.MessageBoxW(0, "Invalid login information.", "GUTZ v1.0 - LOGIN", MB_ICONERROR)
      cmd_size(45, 4)
      clear_cmd()
      print()
      simulate_typing(Colorate.Color(Colors.gray, " initializing::[type=func]reboot_login_tui()"))
      time.sleep(1)
      hidecursor()
      login_tui()
  clear_cmd()
  cmd_size(29, 8)
  
  print(Colorate.Color(Colors.red, login_banner, True))
  username = input(Colorate.Color(Colors.gray, " username > ", True))
  if username.lower() == "___back___".lower():
      login_tui()
  print()
  password = input(Colorate.Color(Colors.gray, " password > ", True))
  if password.lower() == "___back___".lower():
        login_tui()
  login(username, password)
  
def main_menu():
  ping_time = get_wifi_ip_ping_time()
  cmd_title(f"GUTZ V1 (User: {pcuser}) | MAIN | Ping: {ping_time}ms")
  if str(ping_time) == "None":
      cmd_title(f"GUTZ V1 (User: {pcuser}) | MAIN | error_checking_ping")
  cmd_size(92, 25)
  showcursor()
  clear_cmd()
  print(Colorate.Vertical(Colors.red_to_black, main_banner, 1))
  print(Colorate.Vertical(Colors.red_to_black, tui_ops, 1))
  print()
  option = input(Colorate.Color(Colors.dark_red, " ♦ " + pcuser + "/main ♦ > ", True))
  print()
  webhooks.update(load_webhooks("webhooks.json"))
  
  if option == ".run 1":
    target_ip = input(Colorate.Color(Colors.red, " ♣ IP > ", True))
    if target_ip.lower() == "___back___".lower():
      main_menu()
    port_range = input(Colorate.Color(Colors.red, " ♣ Range > ", True))
    if port_range.lower() == "___back___".lower():
      main_menu()
    try:
      start_port, end_port = parse_port_range(port_range)
    except ValueError as e:
      print(Colorate.Color(Colors.dark_red, " An error occurred"))
      time.sleep(2)
      main_menu()
      
    hidecursor()
    
    clear_cmd()
    
    ping_time = get_wifi_ip_ping_time()
    
    cmd_title(f"GUTZ V1 (User: {pcuser}) | Port Scanner | Scanning: {target_ip} | Ping: {ping_time}ms")
    if str(ping_time) == "None":
        cmd_title(f"GUTZ V1 (User: {pcuser}) | Port Scanner | Scanning: {target_ip} | error_checking_ping")
    cmd_size(80, 13)
    
    open_ports = scan_ports(target_ip, start_port, end_port)

    if open_ports:
        create_directory_if_not_exists("open-ports")
        filename = f"open-ports/{target_ip}-openports.txt"
        with open(filename, "w") as file:
            file.write(f"Open Ports for: {target_ip}\n")
            for port in open_ports:
                file.write(str(port) + "\n")
        print()
        print(Colorate.Color(Colors.red, f" Saved to 'open-ports/{target_ip}-openports.txt'"))
        time.sleep(3)
        main_menu()
    else:
      print()
      print(Colorate.Color(Colors.red, " No open ports found."))
      time.sleep(3)
      main_menu()
  elif option == ".run 2":
    urltxt = Colorate.Color(Colors.red, " ♣ URL > ")
    url = input(urltxt)
    if url.lower() == "___back___".lower():
      main_menu()
    
    clear_cmd()
    hidecursor
    ping_time = get_wifi_ip_ping_time()
    cmd_title(f"GUTZ V1 (User: {pcuser}) | Web-Vulnerability Checker | Checking: {url} | Ping: {ping_time}ms")
    if str(ping_time) == "None":
        cmd_title(f"GUTZ V1 (User: {pcuser}) | Web-Vulnerability Checker | Checking: {url} | error_checking_ping")
            
    print()
    url_nocol = Colorate.Color(Colors.reset, url, True)
    print(Colorate.Color(Colors.yellow, " TARGET : " + url_nocol))
    for input_value in user_inputs:
      invalidsh(url, input_value)
    check_vulnerabilities(url)
    print()
    input(Colorate.Color(Colors.gray, " Press enter to go back"))
    main_menu()
  elif option == ".run 3":
      lookup()
  elif option == ".run 4":
      cmd_size(92, 70)
      cmd_title(f"GUTZ V1 (User: {pcuser}) | Get WIFI SSIDs | Ping: {ping_time}ms")
      if str(ping_time) == "None":
        cmd_title(f"GUTZ V1 (User: {pcuser}) | Get WIFI SSIDs | error_checking_ping")
            
      hidecursor()
      pathrs = r"core\ssids.ps1"
      app_nameee = "powershell.exe"
      window_width = 92
      window_height = 70
      command = [app_nameee, "-ExecutionPolicy", "Bypass", "-File", pathrs]
      start_cmd = f"mode con: cols={window_width} lines={window_height} & {' '.join(command)}"
      subprocess.run(start_cmd, shell=True)
      time.sleep(2)
      main_menu()
  elif option.startswith(".add_webhook"):
        _, webhook_url = option.split(" ", 1)
        webhook_id = generate_random_id()
        webhooks[webhook_id] = webhook_url
        save_webhooks("webhooks.json")
        print(Colorate.Color(Colors.red, f" Webhook added with ID: {webhook_id}", True))
        time.sleep(2)
        logging.info(f"{pcuser} added webhook {webhook_id}: {webhook_url}")
  elif option.startswith(".sendmsg"):
      _, webhook_id, message = option.split(" ", 2)
      
      if webhook_id in webhooks:
          webhook_url = webhooks[webhook_id]
          send_webhook_message(webhook_url, message)
          logging.info(f"{pcuser} sended a message with url: {webhook_url} msg[{message}]")
          time.sleep(1)
          main_menu()
      else:
          print(Colorate.Color(Colors.red, " Invalid webhook ID.", True))
          time.sleep(3)
          main_menu()
  elif option == ".ids":
        logging.info(f"{pcuser} showed IDs")
        clear_cmd()
        hidecursor()
        cmd_size(132, 25)
        print()
        list_webhook_ids()
        print()
        input(Colorate.Color(Colors.gray, " Press enter to go back"))
        main_menu()
  elif option.startswith(".del_webhook"):
      _, webhook_id = option.split(" ", 1)
      delete_webhook(webhook_id)
      time.sleep(3)
      logging.info(f"{pcuser} deleted webhook with id: {webhook_id}")
      main_menu()
  elif option.lower() == ".run E".lower():
    logging.info(f"{pcuser} exited")
    os.system('taskkill /F /FI "WindowTitle eq  GUTZ - Discord Rich Presence" /T')
    exit()
  else:
    logging.error(f"user {pcuser} used an invalid option[{option}]")
    print(Colorate.Color(Colors.red, " Invalid Option\n  ╚> Syntax '.run{option}'", True))
    time.sleep(3)
    main_menu()
          
def scan_port(target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                prttxt = Colorate.Color(Colors.green, " hit:PORT > ")
                port_col = Colorate.Color(Colors.reset, str(port))
                other_shit = Colorate.Color(Colors.light_green, "                                                        > OPEN")
                if port > 10:
                    other_shit = Colorate.Color(Colors.light_green, "                                                       > OPEN")
                if port == 10:
                    other_shit = Colorate.Color(Colors.light_green, "                                                       > OPEN")
                if port > 100:
                     other_shit = Colorate.Color(Colors.light_green, "                                                      > OPEN")
                if port == 100:
                     other_shit = Colorate.Color(Colors.light_green, "                                                      > OPEN")
                if port > 1000:
                     other_shit = Colorate.Color(Colors.light_green, "                                                     > OPEN")
                if port == 1000:
                     other_shit = Colorate.Color(Colors.light_green, "                                                     > OPEN")
                if port > 10000:
                     other_shit = Colorate.Color(Colors.light_green, "                                                    > OPEN")
                if port == 10000:
                    other_shit = Colorate.Color(Colors.light_green, "                                                    > OPEN")
                print(prttxt + port_col + other_shit)
                return port
    except Exception as e:
        pass

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(scan_port_async, target_ip, port)
        result = future.result()
        
        if result is not None:
            prttxt = Colorate.Color(Colors.green, " hit:PORT > ")
            port_col = Colorate.Color(Colors.reset, str(port))
            other_shit = Colorate.Color(Colors.light_green, "                                                        > OPEN")
            if port > 10:
                other_shit = Colorate.Color(Colors.light_green, "                                                       > OPEN")
            if port == 10:
                other_shit = Colorate.Color(Colors.light_green, "                                                       > OPEN")
            if port > 100:
                 other_shit = Colorate.Color(Colors.light_green, "                                                      > OPEN")
            if port == 100:
                 other_shit = Colorate.Color(Colors.light_green, "                                                      > OPEN")
            if port > 1000:
                 other_shit = Colorate.Color(Colors.light_green, "                                                     > OPEN")
            if port == 1000:
                 other_shit = Colorate.Color(Colors.light_green, "                                                     > OPEN")
            if port > 10000:
                 other_shit = Colorate.Color(Colors.light_green, "                                                    > OPEN")
            if port == 10000:
                other_shit = Colorate.Color(Colors.light_green, "                                                    > OPEN")
            print(prttxt + port_col + other_shit)
            return port
    
    tryy = Colorate.Vertical(Colors.red_to_yellow, " try:PORT > ", 1)
    portr = Colorate.Color(Colors.gray, str(port), True)
    other_shit2 = Colorate.Color(Colors.light_red, "                                                        > NOT OPEN")
    if port > 10:
        other_shit2 = Colorate.Color(Colors.light_red, "                                                       > NOT OPEN")
    if port == 10:
        other_shit2 = Colorate.Color(Colors.light_red, "                                                       > NOT OPEN")
    if port > 100:
         other_shit2 = Colorate.Color(Colors.light_red, "                                                      > NOT OPEN")
    if port == 100:
         other_shit2 = Colorate.Color(Colors.light_red, "                                                      > NOT OPEN")
    if port > 1000:
         other_shit2 = Colorate.Color(Colors.light_red, "                                                     > NOT OPEN")
    if port == 1000:
         other_shit2 = Colorate.Color(Colors.light_red, "                                                     > NOT OPEN")
    if port > 10000:
         other_shit2 = Colorate.Color(Colors.light_red, "                                                    > NOT OPEN")
    if port == 10000:
        other_shit2 = Colorate.Color(Colors.light_red, "                                                    > NOT OPEN")
    print(tryy + " " + portr + other_shit2)
    
    return None
  
def scan_port_async(target_ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                return port
    except Exception as e:
        pass

    return None

def scan_ports(target_ip, start_port, end_port, max_workers=10):
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port): port for port in range(start_port, end_port + 1)}
        
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            result = future.result()
            if result is not None:
                open_ports.append(result)
    
    return open_ports

def check_vulnerabilities(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        content = response.text
    except Exception as e:
        os.system("cls")
        print()
        print(Colorate.Color(Colors.dark_red, " URLERROR_: url does not exist..."))
        return
    
    print()

    if status_code == 200:
        print(Colorate.Color(Colors.light_green, " [+] Website           > ONLINE"))
    else:
        print(Colorate.Color(Colors.light_red, " [-] Website           > OFFLINE"))
    
    try:
        payload = "' OR '1'='1"
        injected_url = f"{url}/search?query={payload}"
        response = requests.get(injected_url)
        content_sql = response.text

        if "error" in content_sql.lower():
            print(Colorate.Color(Colors.light_green, " [+] SQL               > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] SQL               > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_SQL", True))

    try:
        payload = "<script>alert('XSS');</script>"
        injected_url = f"{url}/search?query={payload}"
        response = requests.get(injected_url)
        content_xss = response.text

        if "<script>alert('XSS');</script>" in content_xss:
            print(Colorate.Color(Colors.light_green, " [+] XSS               > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] XSS               > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, "Error:_IN_XSS"))

    sensitive_keywords = ["password", "credit card", "social security", "private key"]

    for keyword in sensitive_keywords:
        kw = Colorate.Color(Colors.reset, keyword, True)
        if keyword in content.lower():
            print(Colorate.Color(Colors.light_green, " [+] Sensitive=TRUE    > kw: " + kw))
        else:
            print(Colorate.Color(Colors.light_red, " [-] Sensitive=FALSE   > kw: " + kw))
            
    try:
        payload = "ping -c 1 example.com"
        injected_url = f"{url}/search?query={payload}"
        response = requests.get(injected_url, timeout=5)
        if response.status_code == 200 and "1 packets transmitted, 1 received" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] RCE               > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] RCE               > FALSE"))
    except requests.exceptions.Timeout:
        print(Colorate.Color(Colors.light_red, " [-] RCE               > FALSE[TIMEOUT]"))
        
    try:
        directory_traversal_url = f"{url}/../"
        response = requests.get(directory_traversal_url)
        if "root directory" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] Traversal         > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] Traversal         > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_TRV"))
        
    try:
        cmd_injection_payload = "; echo 'test'"
        cmd_injection_url = f"{url}?param={cmd_injection_payload}"
        response = requests.get(cmd_injection_url)
        if "test" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] Command Inject    > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] Command Inject    > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_CMDINJECT"))
        
    try:
        serialized_data = '{"username": "attacker", "role": "admin"}'
        payload = f"?data={serialized_data}"
        vulnerable_url = f"{url}/deserialize{payload}"
        response = requests.get(vulnerable_url)
        if "execution_error" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] Deserialization   > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] Deserialization   > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_DSRLZTN"))
        
    try:
        redirect_url = f"{url}/redirect?url=https://www.google.com/"
        response = requests.get(redirect_url)

        if "https://www.google.com/" in response.url:
            print(Colorate.Color(Colors.light_green, " [+] Open Redirect     > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] Open Redirect     > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_OPNRDRCT"))
        
    try:
        file_payload = open("m/file.file", "rb")
        files = {"file": file_payload}
        upload_url = f"{url}/upload"
        response = requests.post(upload_url, files=files)

        if "File uploaded successfully" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] File              > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] File              > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_FLPLD"))
    
    try:
        xxe_payload = '<?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE foo [<!ELEMENT foo ANY ><!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>'
        xxe_url = f"{url}/xxe"
        headers = {"Content-Type": "application/xml"}
        response = requests.post(xxe_url, data=xxe_payload, headers=headers)

        if "root:x:" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] XXE               > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] XXE               > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_XXE"))
    
    try:
        csrf_payload = '<img src="https://www.google.com/" />'
        csrf_url = f"{url}/change-settings"
        headers = {"Content-Type": "application/xml"}
        response = requests.post(csrf_url, data=csrf_payload, headers=headers)

        if "settings updated" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] CSRF              > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] CSRF              > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_CSRF"))
        
    security_misconfigurations = check_security_misconfigurations(url)
    for misconfiguration in security_misconfigurations:
        misconfig_txt = Colorate.Color(Colors.dark_red, " Error_IN_MSCNFGRTN", True)
        if "Error" in misconfiguration:
            print(misconfig_txt)
        else:
            print(Colorate.Color(Colors.light_green, " [+] misconfig         > TRUE"))
    
    try:
        ssrf_payload = "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"
        ssrf_url = f"{url}/fetch?url={ssrf_payload}"
        response = requests.get(ssrf_url)

        if "admin" in response.text:
            print(Colorate.Color(Colors.light_green, " [+] SSRF              > TRUE"))
        else:
            print(Colorate.Color(Colors.light_red, " [-] SSRF              > FALSE"))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_IN_SSRF"))
        
    authentication_issues = check_broken_authentication(url)
    for issue in authentication_issues:
        issue_txt = Colorate.Color(Colors.dark_red, " Error:_THCHCK", True)
        if "Error" in issue:
            print(issue_txt)
        else:
            print(Colorate.Color(Colors.light_green, f" [+] BrokenAuth        > TRUE"))
            
    try:
        num_requests = 5
        for _ in range(num_requests):
            response = requests.get(url)
            status_code = response.status_code
            print(Colorate.Color(Colors.cyan, " Response: " + status_code, True))
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_SNDRQSTS"))

def invalidsh(url, input_value):
    try:
        validation_url = f"{url}/validate?input={input_value}"
        response = requests.get(validation_url)
        if "validation_failed" in response.text:
            col_in = Colorate.Color(Colors.cyan, input_value, True)
            idkfr = Colorate.Color(Colors.light_green, "]", True)
            print(Colorate.Color(Colors.light_green, " [+] brokenInput       > TRUE [" + col_in + idkfr))
        else:
            pass
    except Exception as e:
        print(Colorate.Color(Colors.dark_red, " Error:_NVLDTDNPT"))
        
def check_broken_authentication(url):
    issues = []

    try:

        default_credentials_payload = "/admin"
        default_credentials_url = f"{url}/{default_credentials_payload}"
        response = requests.get(default_credentials_url)
        if "login" in response.text:
            issues.append("Default Credentials Found")

        weak_password_payload = "/login"
        weak_password_url = f"{url}/{weak_password_payload}"
        response = requests.post(weak_password_url, data={"username": "admin", "password": "password"})
        if "invalid credentials" in response.text:
            issues.append("Weak Password Policy")

        session_fixation_payload = "/login"
        session_fixation_url = f"{url}/{session_fixation_payload}"
        response = requests.get(session_fixation_url)
        if "sessionid" in response.cookies:
            issues.append("Session Fixation Vulnerability")

    except Exception as e:
        issues.append("Error checking Broken Authentication")

    return issues

def check_security_misconfigurations(url):
    misconfigurations = []

    try:
        directory_listing_payload = "/.git/config"
        directory_listing_url = f"{url}/{directory_listing_payload}"
        response = requests.get(directory_listing_url)
        if "repository" in response.text:
            misconfigurations.append("Directory Listing Enabled")

        debug_mode_payload = "/?debug=true"
        debug_mode_url = f"{url}/{debug_mode_payload}"
        response = requests.get(debug_mode_url)
        if "debug information" in response.text:
            misconfigurations.append("Debug Mode Enabled")

        admin_panel_payload = "/admin"
        admin_panel_url = f"{url}/{admin_panel_payload}"
        response = requests.get(admin_panel_url)
        if "login" in response.text:
            misconfigurations.append("Exposed Admin Panel")

    except Exception as e:
        misconfigurations.append("Error checking misconfigurations")

    return misconfigurations

def lookup():
    useripaddress = input(Colorate.Color(Colors.red, " ♣ IP > ", True))
    clear_cmd()
    hidecursor()
    ping_time = get_wifi_ip_ping_time()
    cmd_title(f"GUTZ V1 (User: {pcuser}) | IP Lookup | IP: {useripaddress} | Ping: {ping_time}ms")
    if str(ping_time) == "None":
        cmd_title(f"GUTZ V1 (User: {pcuser}) | IP Lookup | IP: {useripaddress} | error_checking_ping")
       
    print()

    ipapi_response = requests.get(f"https://ipapi.co/{useripaddress}/json/")
    ipapi_data = ipapi_response.json()

    ip_api_response = requests.get(f"http://ip-api.com/json/{useripaddress}")
    ip_api_data = ip_api_response.json()

    userip = ipapi_data.get('ip', '')

    usercity = ipapi_data.get('city', '')
    useregion = ipapi_data.get('region', '')
    usercountry = ipapi_data.get('country_name', '')

    userlat = str(ip_api_data.get('lat', ''))
    userlon = str(ip_api_data.get('lon', ''))
    usertime = ip_api_data.get('timezone', '')
    userpostal = ip_api_data.get('zip', '')
    userisp = ipapi_data.get('org', '')
    userasn = ipapi_data.get('asn', '')
    usercountrycode = ipapi_data.get('country_code', '')
    usercurrency = ipapi_data.get('currency', '')
    userlanguage = ipapi_data.get('languages', '')
    usercalling = ipapi_data.get('country_calling_code', '')

    print("   Ip Address     |", userip)
    print("   City           |", usercity)
    print("   Region         |", useregion)
    print("   Country        |", usercountry)
    print()
    print("   Latitude       |", userlat)
    print("   Longitude      |", userlon)
    print("   Timezone       |", usertime)
    print("   Posta Code     |", userpostal)
    print("   ISP            |", userisp)
    print("   ASN            |", userasn)
    print("   Country Code   |", usercountrycode)
    print()
    print("   Currency       |", usercurrency)
    print("   Language       |", userlanguage)
    print("   Calling Code   |", usercalling)
    print("   GOOGLE Maps    | https://maps.google.com/?q=" + userlat + "," + userlon)
    print()
    input(Colorate.Color(Colors.gray, " Press enter to go back"))
    main_menu()

login_tui()