import network
import time 
import urequests 
import config

def get_external_ip():
    try:
        url = "http://checkip.amazonaws.com/"
        response = urequests.get(url)
        ip = response.text.strip()
        response.close()
        print("External IP:", ip)
        return ip
    except Exception as e:
        print("Error getting external IP:", e)
        return None

def read_wifi_config(filename="wifi.cfg"):
    '''
    Reads a Wi-Fi config file and returns (ssid, password).
    Expected file format:
      ssid=YourNetworkName
      password=YourPassword
    '''
    ssid = None
    password = None

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # skip empty lines and comments
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip().lower()
                value = value.strip()
                if key == 'ssid':
                    ssid = value
                elif key == 'password':
                    password = value
        if ssid is None or password is None:
            raise ValueError("SSID or password not found in config file")
        return ssid, password
    except Exception as e:
        print("Failed to read Wi-Fi config:", e)
        return None, None

def connect_wifi():
    settings = config.read_config_settings()

    WIFI_SSID = settings["ssid"]
    WIFI_PASSWORD = settings["password"]

    print(f"Connecting to {WIFI_SSID}...")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    max_wait = 10
    while max_wait > 0:
        if wlan.isconnected():
            break
        max_wait -= 1
        time.sleep(1)

    if wlan.isconnected():
        print('Connected to', WIFI_SSID)
        # print("Connection data:", wlan.ifconfig())
        return wlan
    else:
        print('Failed to connect to', WIFI_SSID)
        return None
