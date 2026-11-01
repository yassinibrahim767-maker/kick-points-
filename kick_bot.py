import time
import random
import string
import os
import requests  # عشان نبعت لتليجرام
from camoufox.sync_api import Camoufox
from recognizer.agents.playwright import SyncChallenger

# سحب البيانات السرية
USERNAME = os.environ.get("KICK_USERNAME")
PASSWORD = os.environ.get("KICK_PASSWORD")
TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

# القناة اللي عايزين نتابعها
STREAM_URL = "https://kick.com/3li_boltx" 
LOGIN_URL = "https://kick.com/login"

SESSION_DURATION = 5.5 * 60 * 60 

COMMENTS = ["مستوى البث خرافي!", "تسلم يا باشا", "محتوى قوي جداً", "أحلى بث في كيك", "نقطة"]

def generate_random_comment():
    return f"{random.choice(COMMENTS)} {''.join(random.choices(string.ascii_lowercase, k=3))}"

# دالة إرسال رسالة لتليجرام
def send_telegram_message(message):
    if not TG_TOKEN or not TG_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": message}, timeout=5)
    except Exception as e:
        print(f"فشل إرسال رسالة تليجرام: {e}")

def run_session():
    print("بدء جلسة جديدة...")
    send_telegram_message("🚀 بدء جلسة جديدة على كيك وتجميع نقاط...")
    
    with Camoufox(headless="virtual", geoip=True) as browser:
        page = browser.new_page()
        
        try:
            # تسجيل الدخول
            page.goto(LOGIN_URL, wait_until="networkidle")
            time.sleep(random.uniform(2, 4))
            
            challenger = SyncChallenger(page, click_timeout=1000)
            if page.locator('iframe[title*="reCAPTCHA"]').count() > 0:
                try:
                    challenger.solve_recaptcha()
                    time.sleep(2)
                except: pass
            
            page.fill('input[name="username"]', USERNAME)
            page.fill('input[name="password"]', PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")
            time.sleep(random.uniform(3, 6))

            # فتح القناة
            page.goto(STREAM_URL, wait_until="domcontentloaded")
            print("تم فتح الاستريم بنجاح.")
            send_telegram_message(f"✅ تم فتح قناة {STREAM_URL.split('/')[-1]} بنجاح.")
            
            end_time = time.time() + SESSION_DURATION
            last_points_check = time.time()
            
            while time.time() < end_time:
                # --- حركة ماوس عشوائية ---
                try:
                    page.mouse.move(random.randint(100, 800), random.randint(100, 400))
                except: pass

                # --- التعليق العشوائي ---
                if random.random() < 0.12:
                    try:
                        chat_input = page.locator('input[id="chat-input"]').first
                        if chat_input.is_visible():
                            comment = generate_random_comment()
                            chat_input.fill(comment)
                            chat_input.press('Enter')
                            print(f"[{time.strftime('%H:%M:%S')}] تم التعليق: {comment}")
                    except: pass

                # --- قراءة النقاط وإرسالها كل ساعة ---
                if time.time() - last_points_check > 3600:  # كل 60 دقيقة
                    try:
                        # كيك بتعرض النقاط غالباً في عنصر بهذا الشكل (ممكن يتغير)
                        # هنحاول نقرا الرقم من الزرار اللي فيه كلمة Points
                        points_element = page.locator('button:has-text("Points")').first
                        if points_element.is_visible():
                            points_text = points_element.inner_text()
                            send_telegram_message(f"💰 تحديث النقاط: {points_text}")
                            print(f"تم إرسال النقاط: {points_text}")
                    except Exception as e:
                        print(f"لم نتمكن من قراءة النقاط: {e}")
                    
                    last_points_check = time.time()
                
                time.sleep(random.uniform(3, 7))

            print("انتهت الجلسة.")
            send_telegram_message("⏸️ انتهت جلسة الـ 5 ساعات. سيتم البدء في الجلسة التالية تلقائياً.")

        except Exception as e:
            print(f"حدث خطأ: {e}")
            send_telegram_message(f"❌ حدث خطأ في البوت: {e}")

if __name__ == "__main__":
    run_session()
