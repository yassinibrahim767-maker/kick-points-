import time
import random
import string
import os
import requests
from camoufox.sync_api import Camoufox
from recognizer.agents.playwright import SyncChallenger

USERNAME = os.environ.get("mryassin46")
PASSWORD = os.environ.get("Ya14$$99$$")
TG_TOKEN = os.environ.get("9183636445:AAFPxvhZZlQBE1mFA8Yde09Ilp4OhJPQ76I")
TG_CHAT_ID = os.environ.get("8734064592")

STREAM_URL = "https://kick.com/3li_boltx" 
LOGIN_URL = "https://kick.com/login"

SESSION_DURATION = 5.25 * 60 * 60 

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

def generate_random_comment():
    comments = ["مستوى البث خرافي!", "تسلم يا باشا", "محتوى قوي جداً", "أحلى بث في كيك"]
    return f"{random.choice(comments)} {''.join(random.choices(string.ascii_lowercase, k=3))}"

def run_session():
    print("بدء جلسة جديدة...")
    with Camoufox(headless="virtual", geoip=True, canvas_noise=False) as browser:
        page = browser.new_page()
        try:
            # التعديل هنا: غيرنا networkidle لـ domcontentloaded
            page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(3, 5))
            
            if page.locator('iframe[title*="reCAPTCHA"]').count() > 0:
                try: SyncChallenger(page).solve_recaptcha()
                except: pass
            
            page.fill('input[name="username"]', USERNAME)
            page.fill('input[name="password"]', PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_load_state("domcontentloaded", timeout=60000)
            time.sleep(random.uniform(3, 5))

            page.goto(STREAM_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(4, 7)) 
            
            if not is_channel_live(page):
                print("القناة أوفلاين حالياً.")
                send_telegram_message("💤 القناة أوفلاين. البوت هيستنى الساعة الجاية.")
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

                if random.random() < 0.1:
                    try:
                        chat_input = page.locator('input[id="chat-input"]').first
                        if chat_input.is_visible():
                            chat_input.fill(generate_random_comment())
                            chat_input.press('Enter')
                    except: pass

                time.sleep(random.uniform(3, 7))

            print("انتهت الجلسة.")
            send_telegram_message("⏸️ انتهت مدة الجلسة. جاري فحص إمكانية بدء جلسة جديدة...")

        except Exception as e:
            print(f"حدث خطأ: {e}")
            send_telegram_message(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_session()
