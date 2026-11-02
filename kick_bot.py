import time
import random
import string
import requests
import re  # مكتبة التعبيرات النمطية
from camoufox.sync_api import Camoufox
from recognizer.agents.playwright import SyncChallenger

# ⚠️ تنبيه: البيانات مكتوبة مباشرة هنا (الريبو عام). يُفضل تغييرها لاحقاً لأسباب أمنية.
USERNAME = "mryassin46"
PASSWORD = "Ya14$$99$$"
TG_TOKEN = "9183636445:AAFPxvhZZlQBE1mFA8Yde09Ilp4OhJPQ76I"
TG_CHAT_ID = "8734064592"

STREAM_URL = "https://kick.com/3li_boltx" 
HOME_URL = "https://kick.com/" 

SESSION_DURATION = 5.25 * 60 * 60 
last_tg_update_id = 0 

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

def check_telegram_commands():
    global last_tg_update_id
    if not TG_TOKEN or not TG_CHAT_ID: return None
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/getUpdates?offset={last_tg_update_id + 1}&timeout=1"
        response = requests.get(url, timeout=5).json()
        
        if response.get("ok") and response.get("result"):
            for update in response["result"]:
                last_tg_update_id = update["update_id"]
                if "message" in update and "text" in update["message"]:
                    text = update["message"]["text"]
                    chat_id = str(update["message"]["chat"]["id"])
                    if chat_id == str(TG_CHAT_ID) and text.strip() == "!points":
                        return True
    except: pass
    return False

def is_channel_live(page):
    try:
        if page.locator('video').count() > 0 or page.locator('text="LIVE"').count() > 0:
            return True
        return False
    except:
        return False

def generate_random_comment():
    comments = [
        "مستوى البث خرافي!", "تسلم يا باشا", "محتوى قوي جداً", "أحلى بث في كيك",
        "استمر يا وحش", "بث جامد جداً", "تسلم إيدك", "كمل يا بطل", "منورين الشات", "لايف ممتاز",
        "3li_BoltxLogoBoltx", "KEKW", "HYPERCLAP", "KEKLEO", "Bwop", "collectiblesCLEAN"
    ]
    chosen = random.choice(comments)
    emotes_list = ["3li_BoltxLogoBoltx", "KEKW", "HYPERCLAP", "KEKLEO", "Bwop", "collectiblesCLEAN"]
    if chosen in emotes_list:
        return chosen 
    else:
        return f"{chosen} {''.join(random.choices(string.ascii_lowercase, k=3))}"

def run_session():
    print("بدء جلسة جديدة...")
    with Camoufox(headless="virtual", geoip=True, canvas_noise=False) as browser:
        page = browser.new_page()
        try:
            print("جاري فتح الصفحة الرئيسية...")
            page.goto(HOME_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(3, 5))
            
            # 1. تسجيل الدخول
            print("جاري الضغط على زرار Log In...")
            try:
                page.locator('text="Log In"').first.click(timeout=10000)
            except: pass

            time.sleep(random.uniform(3, 5))
            
            if page.locator('iframe[title*="reCAPTCHA"]').count() > 0:
                print("تم اكتشاف كابتشا! جاري محاولة الحل...")
                try: 
                    SyncChallenger(page).solve_recaptcha()
                    time.sleep(3)
                except: pass
            
            print("جاري إدخال بيانات الدخول...")
            try:
                email_input = page.get_by_label("Email or Username")
                email_input.wait_for(state="visible", timeout=30000)
                email_input.fill(USERNAME)
                time.sleep(1)
                
                password_input = page.locator('input[type="password"]').first
                password_input.wait_for(state="visible", timeout=15000)
                password_input.fill(PASSWORD)
                
                print("✅ تم إدخال البيانات! جاري الضغط على زر الدخول...")
                page.locator('button:has-text("Log In")').last.click(timeout=10000)
                
                page.wait_for_load_state("domcontentloaded", timeout=60000)
                time.sleep(random.uniform(5, 8))
                
                if page.locator('input[type="password"]').count() == 0:
                    print("✅ تم تسجيل الدخول بنجاح!")
                else:
                    print("⚠️ تحذير: النافذة ما زالت مفتوحة.")
                    page.screenshot(path="login_failed.png")
                    send_telegram_photo("login_failed.png", "⚠️ فشل تسجيل الدخول.")

            except Exception as fill_error:
                print("❌ فشل في إدخال البيانات!")
                page.screenshot(path="login_error.png")
                send_telegram_photo("login_error.png", "❌ البوت عجز عن إدخال البيانات.")
                raise fill_error

            # 2. الدخول للقناة
            print("جاري الانتقال إلى القناة...")
            page.goto(STREAM_URL, wait_until="domcontentloaded", timeout=60000)
            time.sleep(random.uniform(4, 7)) 
            
            if not is_channel_live(page):
                print("القناة أوفلاين حالياً.")
                send_telegram_message("💤 القناة أوفلاين. البوت هيستنى الساعة الجاية.")
                return 
                
            print("القناة لايف! البوت بدأ يتفرج...")
            send_telegram_message(f"✅ القناة لايف! البوت بدأ يتفرج ويجمع نقاط. اكتب !points في أي وقت عشان تعرف نقاطك.")
            
            # 3. حلقة التفرج والتعليق والاستماع لتليجرام
            end_time = time.time() + SESSION_DURATION
            next_chat_time = time.time() + random.randint(10, 30)
            check_counter = 0
            last_tg_check = time.time()
            warned_about_end = False # متغير عشان نمنع تكرار رسالة التحذير
            
            while time.time() < end_time:
                # فحص الوقت المتبقي للتحذير (لو باقي 5 دقايق أو أقل)
                time_left = end_time - time.time()
                if time_left <= 300 and not warned_about_end:
                    print("اقترب انتهاء الجلسة، جاري إرسال تحذير...")
                    send_telegram_message("⏰ تنبيه: باقي 5 دقايق وتنتهي الجلسة الحالية. البوت هيفضل يشتغل عادي لحد آخر ثانية عشان مفيش نقط تضيع، وبعدها هتشتغل الجلسة اللي بعدها تلقائياً.")
                    warned_about_end = True

                check_counter += 1
                if check_counter >= 60:
                    if not is_channel_live(page):
                        print("القناة قفلت أثناء الجلسة.")
                        send_telegram_message("🔴 القناة قفلت. البوت هيستنى الساعة الجاية.")
                        break 
                    check_counter = 0
                
                # --- الاستماع لتليجرام ---
                if time.time() - last_tg_check >= 5:
                    if check_telegram_commands():
                        print("📩 وصل أمر !points! جاري إرسالها في الشات ومراقبة الرد لـ 15 ثانية...")
                        try:
                            chat_input = page.locator('input[id="chat-input"]').first
                            if chat_input.is_visible():
                                chat_input.fill("!points")
                                chat_input.press('Enter')
                                print("تم إرسال !points في الشات.")
                                
                                # نراقب الشات لمدة 15 ثانية
                                start_watch = time.time()
                                found_reply = False
                                
                                while time.time() - start_watch < 15:
                                    try:
                                        messages = page.locator('div[class*="chat-message"], div[class*="ChatMessage"], div[class*="message"]').all()
                                        
                                        if messages:
                                            recent_messages = messages[-5:] 
                                            for msg in recent_messages:
                                                text = msg.inner_text().strip()
                                                if "mryassin46" in text and ("نقطة" in text or "points" in text.lower()):
                                                    numbers = re.findall(r'\d+', text)
                                                    if numbers:
                                                        points_count = numbers[0]
                                                        send_telegram_message(f"💰 عدد نقاطك الحالي: {points_count}")
                                                        found_reply = True
                                                        break
                                        if found_reply:
                                            break
                                    except:
                                        pass
                                    time.sleep(2)
                                
                                if not found_reply:
                                    send_telegram_message("⚠️ مفيش رد ظهر في الشات فيه عدد نقاطك. جرب تاني بعد شوية.")
                                    
                        except Exception as e:
                            print(f"فشل تنفيذ أمر النقاط: {e}")
                            send_telegram_message(f"❌ حدث خطأ أثناء محاولة معرفة النقاط: {e}")
                    
                    last_tg_check = time.time()
                # --------------------------

                try:
                    page.mouse.move(random.randint(100, 800), random.randint(100, 400))
                except: pass

                # الكومنتات العادية
                if time.time() >= next_chat_time:
                    try:
                        chat_input = page.locator('input[id="chat-input"]').first
                        if chat_input.is_visible():
                            comment = generate_random_comment()
                            chat_input.fill(comment)
                            chat_input.press('Enter')
                            print(f"[{time.strftime('%H:%M:%S')}] 📤 تم إرسال رسالة للشات: {comment}")
                            
                            if random.random() < 0.20:
                                random_delay = random.randint(300, 420)
                            else:
                                random_delay = random.randint(150, 280)
                            
                            next_chat_time = time.time() + random_delay
                    except Exception as e:
                        print(f"فشل إرسال رسالة في الشات: {e}")
                        next_chat_time = time.time() + 10

                time.sleep(random.uniform(3, 7))

            print("انتهت الجلسة.")
            send_telegram_message("⏸️ انتهت مدة الجلسة. جاري فحص إمكانية بدء جلسة جديدة...")

        except Exception as e:
            print(f"حدث خطأ: {e}")
            send_telegram_message(f"❌ خطأ: {e}")

if __name__ == "__main__":
    run_session()
