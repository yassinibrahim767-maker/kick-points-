import time
import random
import string
import os
from camoufox.sync_api import Camoufox
from recognizer.agents.playwright import SyncChallenger

# سحب بيانات الدخول من إعدادات GitHub السرية
USERNAME = os.environ.get("KICK_USERNAME")
PASSWORD = os.environ.get("KICK_PASSWORD")

STREAM_URL = "https://kick.com/ali_botex"
LOGIN_URL = "https://kick.com/login"

# مدة الجلسة (5 ساعات و 30 دقيقة) - أقل من حد جيت هاب بـ 30 دقيقة
SESSION_DURATION = 5.5 * 60 * 60 

COMMENTS = [
    "مستوى البث خرافي!", "تسلم يده عليك يا باشا", "شوف يا علي",
    "مصر معاك", "محتوى قوي جداً", "لايف ماراثون", "نقطة", "أحلى بث في كيك"
]

def generate_random_comment():
    base = random.choice(COMMENTS)
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    return f"{base} {suffix}"

def run_session():
    print("بدء جلسة جديدة...")
    # headless="virtual" مهم جداً عشان يشتغل على لينكس بتاع جيت هاب
    with Camoufox(headless="virtual", geoip=True) as browser:
        page = browser.new_page()
        
        try:
            # تسجيل الدخول
            page.goto(LOGIN_URL, wait_until="networkidle")
            time.sleep(random.uniform(2, 4))
            
            # محاولة حل reCAPTCHA لو ظهرت
            challenger = SyncChallenger(page, click_timeout=1000)
            if page.locator('iframe[title*="reCAPTCHA"]').count() > 0:
                try:
                    challenger.solve_recaptcha()
                    time.sleep(2)
                except:
                    pass
            
            page.fill('input[name="username"]', USERNAME)
            time.sleep(random.uniform(0.5, 1.5))
            page.fill('input[name="password"]', PASSWORD)
            page.click('button[type="submit"]')
            page.wait_for_load_state("networkidle")
            time.sleep(random.uniform(3, 6))

            # فتح القناة
            page.goto(STREAM_URL, wait_until="domcontentloaded")
            print("تم فتح الاستريم بنجاح. البوت يتفرج الآن...")
            
            # حساب وقت النهاية
            end_time = time.time() + SESSION_DURATION
            
            while time.time() < end_time:
                try:
                    page.mouse.move(random.randint(100, 800), random.randint(100, 400))
                except:
                    pass

                # إرسال تعليق بنسبة 12% من الوقت
                if random.random() < 0.12:
                    try:
                        chat_input = page.locator('input[id="chat-input"]').first
                        if chat_input.is_visible():
                            comment = generate_random_comment()
                            chat_input.fill(comment)
                            chat_input.press('Enter')
                            print(f"[{time.strftime('%H:%M:%S')}] تم التعليق: {comment}")
                            time.sleep(random.uniform(5, 10))
                    except:
                        pass
                
                time.sleep(random.uniform(3, 7))

            print("انتهت مدة الجلسة بنجاح. جاري الإغلاق...")

        except Exception as e:
            print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    run_session()
