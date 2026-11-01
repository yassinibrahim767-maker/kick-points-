import time
import random
import string
import requests
from camoufox.sync_api import Camoufox
from recognizer.agents.playwright import SyncChallenger

# ⚠️ تنبيه: البيانات مكتوبة مباشرة هنا (الريبو عام). يُفضل تغييرها لاحقاً لأسباب أمنية.
USERNAME = "mryassin46"
PASSWORD = "Ya14$$99$$"
TG_TOKEN = "9183636445:AAFPxvhZZlQBE1mFA8Yde09Ilp4OhJPQ76I"
TG_CHAT_ID = "8734064592"

STREAM_URL = "https://kick.com/3li_boltx" 
LOGIN_URL = "https://kick.com/login"

SESSION_DURATION = 5.25 * 60 * 60 

def send_telegram_message(message):
    if not TG_TOKEN or not TG_CHAT_ID: return
    try:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                      json={"chat_id": TG_CHAT_ID, "text": message}, timeout=5)
    except: pass

def send_telegram_photo(photo_path, caption=""):
    if not TG_TOKEN or not TG_CHAT_ID: return
    try:
        with open(photo_path, "rb") as f:
            requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendPhoto", 
                          data={"chat_id": TG_CHAT_ID, "caption": caption}, 
                          files={"photo": f}, timeout=10)
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
            print("جاري فتح صفحة تسجيل الدخول...")
            page.goto(LOGIN_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(5, 8))  # زيادة وقت الانتظار عشان الكابتشا تحل نفسها
            
            # فحص الكابتشا
            if page.locator('iframe[title*="reCAPTCHA"]').count() > 0:
                print("تم اكتشاف كابتشا! جاري محاولة الحل...")
                try: 
                    SyncChallenger(page).solve_recaptcha()
                    time.sleep(3)
                except Exception as e: 
                    print(f"فشل حل الكابتشا: {e}")
            
            print("جاري البحث عن خانة اسم المستخدم...")
            try:
                # استنى أطول شوية (30 ثانية) عشان الكابتشا تحل نفسها
                page.wait_for_selector('input[name="username"]', timeout=30000)
                print("✅ ظهرت خانة الإسم! جاري إدخال البيانات...")
                page.fill('input[name="username"]', USERNAME)
                page.fill('input[name="password"]', PASSWORD)
                
                print("جاري الضغط على زر تسجيل الدخول...")
                page.click('button[type="submit"]')
                page.wait_for_load_state("domcontentloaded", timeout=60000)
                time.sleep(random.uniform(5, 8))
                
                # التأكد من نجاح الدخول
                if page.locator('input[name="username"]').count() > 0:
                    print("⚠️ تحذير: يبدو أن تسجيل الدخول لم ينجح (ما زالت خانة الاسم موجودة).")
                    send_telegram_message("⚠️ البوت فشل في تسجيل الدخول. يرجى التحقق من البيانات.")
                else:
                    print("✅ تم تسجيل الدخول بنجاح!")

            except Exception as fill_error:
                print("❌ فشل في العثور على خانة الاسم أو ظهرت كابتشا!")
                print("جاري تصوير الشاشة وإرسالها لتليجرام...")
                page.screenshot(path="captcha_error.png")
                send_telegram_photo("captcha_error.png", "❌ البوت عجز عن تسجيل الدخول. دي صورة الشاشة عشان تشوف السبب.")
                print("--- محتوى الصفحة (أول 1000 حرف) للتحليل ---")
                print(page.content()[:1000])
                print("------------------------------------------")
                raise fill_error

            print("جاري الانتقال إلى القناة...")
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
