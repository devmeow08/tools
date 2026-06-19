import os
import hashlib
import subprocess
import json
import requests
import base64

# --------------------------
# ⚠️ SETTINGS (LINK LANG ANG MAKIKITA NILA)
# --------------------------
# 🔴 LINK NG IYONG "SECRET / PRIVATE REPOSITORY" (DITO NAKA-TAGO ANG data.json)
# HIWALAY ITO SA REPO KUNG SAAN NAKA-STORE ANG main.py at loader.py
GITHUB_FILE_URL = "https://raw.githubusercontent.com/devmeow08/mysms.py/refs/heads/main/data.json?token=GHSAT0AAAAAAEAMFA3R6HDP55ECF4HL5PRW2RVEAUQ"
GITHUB_API_URL  = "https://api.github.com/repos/devmeow08/mysms.py/contents/data.json"
# --------------------------

# 🆔 KUMUHA NG UNIQUE ID NG DEVICE
def get_device_id():
    try:
        info = {}
        for prop in ["ro.product.model", "ro.product.brand", "ro.serialno"]:
            res = subprocess.check_output(["getprop", prop], text=True, stderr=subprocess.DEVNULL).strip()
            info[prop] = res if res else "UnknownDevice"

        unique_string = f"{info['ro.product.model']}-{info['ro.product.brand']}-{info['ro.serialno']}-MY_SECRET_SALT_987"
        return hashlib.md5(unique_string.encode()).hexdigest()
    except:
        return hashlib.md5(os.urandom(20)).hexdigest()

# 🔑 HAKBANG 1: KUNIN MUNA ANG TOKEN MULA SA JSON FILE (NASA IBANG REPO)
def get_secret_token():
    try:
        # Buksan ang file sa kabilang repo (kailangan ng raw link)
        res = requests.get(GITHUB_FILE_URL, timeout=15)
        if res.status_code == 200:
            data = res.json()
            return data.get("SECURE_TOKEN", None)
        return None
    except:
        return None

# 📖 HAKBANG 2: GAMITIN ANG TOKEN PARA BASAHIN ANG BUONG DATA
def load_server_data(secret_token):
    try:
        headers = {
            "Authorization": f"token {secret_token}",
            "Accept": "application/json"
        }
        response = requests.get(GITHUB_FILE_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            full_data = response.json()
            # ⚠️ TANGGALIN ANG TOKEN SA LAMAN PARA HINDI MAHAHALATA
            if "SECURE_TOKEN" in full_data:
                del full_data["SECURE_TOKEN"]
            return full_data
        else:
            print("❌ HINDI MAPASOK ANG SERVER!")
            return None
    except:
        print("❌ WALANG INTERNET!")
        return None

# 💾 ISULAT ANG ID PABALIK SA KABILANG REPO
def register_user_to_server(user_key, device_id, max_allowed, secret_token):
    headers = {
        "Authorization": f"token {secret_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Kunin ang kasalukuyang laman at SHA code
    get_response = requests.get(GITHUB_API_URL, headers=headers)
    if get_response.status_code != 200:
        return False

    file_data = get_response.json()
    sha_hash = file_data["sha"]
    current_content = base64.b64decode(file_data["content"]).decode("utf-8")
    data = json.loads(current_content)

    # Siguraduhing may pwesto ang key
    if user_key not in data:
        data[user_key] = [max_allowed, []]

    # Kung nandito na siya, okay lang
    if device_id in data[user_key][1]:
        return True

    # ✅ Kung may puwang pa
    if len(data[user_key][1]) < max_allowed:
        data[user_key][1].append(device_id)
        new_content = json.dumps(data, indent=2)
        encoded_content = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")

        update_data = {
            "message": "Auto Update User",
            "content": encoded_content,
            "sha": sha_hash
        }
        update_response = requests.put(GITHUB_API_URL, headers=headers, json=update_data)
        return update_response.status_code in [200, 201]
    
    return False

# 🛡️ PANGUNAHING CHECKER
def check_access(user_input_key):
    device_id = get_device_id()

    # 1. Kunin muna ang Token mula sa kabilang repo
    SECURE_TOKEN = get_secret_token()
    if not SECURE_TOKEN:
        return False, "TOKEN_NOT_FOUND"

    # 2. Kunin ang lahat ng Keys at Data mula sa kabilang repo
    server_data = load_server_data(SECURE_TOKEN)
    if not server_data:
        return False, "SERVER_ERROR"

    # 3. Tama ba ang Key?
    if user_input_key not in server_data:
        return False, "INVALID_KEY"

    # 4. Kunin ang Limit at Listahan
    max_users = server_data[user_input_key][0]
    registered_ids = server_data[user_input_key][1]

    # 5. Naka-rehistro na ba?
    if device_id in registered_ids:
        return True, "ACCESS_GRANTED"

    # 6. Wala pa, subukang ipasok
    else:
        if register_user_to_server(user_input_key, device_id, max_users, SECURE_TOKEN):
            return True, "NEW_USER"
        else:
            return False, "LIMIT_FULL"
