import socket
import platform
import psutil
import requests
import datetime
import subprocess
import json

def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "cpu": platform.processor(),
        "ram": str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)) + " GB",
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "software": get_installed_software()
    }

def get_installed_software():
    try:
        command = [
            "powershell",
            "-Command",
            """
            $paths = @(
                'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',
                'HKLM:\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',
                'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'
            )
            $apps = foreach ($path in $paths) {
                Get-ItemProperty $path -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName } |
                Select-Object DisplayName, DisplayVersion, InstallDate
            }
            $apps | ConvertTo-Json
            """
        ]

        output = subprocess.check_output(command, stderr=subprocess.DEVNULL).decode("utf-8", errors="ignore")
        software_items = json.loads(output)

        if isinstance(software_items, dict):
            software_items = [software_items]

        software_list = []
        for item in software_items:
            software_list.append({
                "name": item.get("DisplayName", "Unknown"),
                "version": item.get("DisplayVersion", "N/A"),
                "installed_on": item.get("InstallDate", "")
            })

        return software_list

    except Exception as e:
        print("❌ Software fetch failed:", e)
        return []

# ✅ Send system info to FastAPI server
def register_system(info):
    try:
        response = requests.post("http://localhost:8000/register_system/", json=info)
        print(response.json())
    except Exception as e:
        print("❌ Failed to register:", e)

if __name__ == "__main__":
    system_info = get_system_info()
    register_system(system_info)
