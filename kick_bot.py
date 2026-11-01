import time
import random
import string
import os
import requests
from camoufox.sync_api import Camoufox
from recognizer.agents.playwright import SyncChallenger

USERNAME = os.environ.get("KICK_USERNAME")
PASSWORD = os.environ.get("KICK_PASSWORD")
TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

STREAM_URL = "https://kick.com/3li_boltx" 
LOGIN_URL = "https://kick.com/login"

# أقصى مدة للجلسة (5 ساعات و 20 دقيقة) 
SESSION_DURATION = 5.33 * 60 * 60 

def send_telegram_message(message):
    if not TG_TOKEN or not TG_CHAT_ID: return
    try:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                      json={"chat_id": TG_CHAT_ID, "text": message}, timeout=5)
    except: pass

def is_channel_live(page):
    try:
        if page.locator('video').count() > 0 or page.locator('text="LIVE"').count() > 0:
            return True
        return False
    except:
        return False

def run_session():
    print("بدء جلسة جديدة...")
    with Camoufox(headless="virtual", geoip=True) as browser:
        page = browser.new_page()
        try:
            page.goto(LOGIN_URL, wait_until="networkidle")
            time.sleep(random.uniform(2, 4))
            
            if page.locator('iframe[title*="reCAPTCHA"]').count() > 0:
                try: SyncChallenger(page).solve_recaptcha()
                except: pass
            
            page.fill('input[name="username"]', USERNAME)
            page.fill('input[name="password"]', PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")
            time.sleep(random.uniform(3, 5))

            page.goto(STREAM_URL, wait_until="domcontentloaded")
            time.sleep(random.uniform(4, 7)) 
            
            if not is_channel_live(page):
                print("القناة أوفلاين حالياً.")
                send_telegram_message("💤 القناة أوفلاين. البوت هيستنى الساعة الجاية عشان يفحص تاني.")
                return 
                
            print("القناة لايف! البوت بدأ يتفرج...")
            send_telegram_message(f"✅ القناة لايف! البوت بدأ يتفرج ويجمع نقاط.")
            
            end_time = time.time() + SESSION_DURATION
            check_counter = 0
            
            while time.time() < end_time:
                check_counter += 1
                if check_counter >= 60:
                    if not is_channel_live(page):
                        print("القناة قفلت أثناء الجلسة.")
                        send_telegram_message("🔴 القناة قفلت. البوت هيستنى الساعة الجاية.")
                        break 
                    check_counter = 0
                
                try:
                    page.mouse.move(random.randint(100, 800), random.randint(100, 400))
                except: pass

                time.sleep(random.uniform(3, 7))

            print("انتهت الجلسة.")
            send_telegram_message("⏸️ انتهت مدة الجلسة. جاري فحص إمكانية بدء جلسة جديدة...")

        except Exception as e:
            print(f"حدث خطأ: {e}")
            send_telegram_message(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_session()
