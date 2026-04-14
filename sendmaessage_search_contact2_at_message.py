from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os

# ================= CONFIG =================
CONTACT_FILE = "c3"
MESSAGE_FILE = "msg"
ATTACHMENT_PATH = "/Users/varun/programs/whatsapp/fcfs.jpeg"
CHROME_PROFILE = "/var/tmp/chrome_user_data"
# ==========================================

options = Options()
options.add_argument("--user-data-dir=" + CHROME_PROFILE)
options.add_argument("--profile-directory=Default")
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)

# Load message
with open(MESSAGE_FILE, "r", encoding="utf8") as f:
    MESSAGE = f.read()

# ================= FUNCTIONS =================

def open_whatsapp():
    driver.get("https://web.whatsapp.com")
    print("Waiting for login...")
    # Using the user's preferred input wait
    input("Login WhatsApp Web and press ENTER in this terminal...")

# 🔍 SEARCH CONTACT (PERFECT VERSION)
def search_contact(name):
    try:
        print(f"Searching: {name}")
        search_box = wait.until(EC.presence_of_element_located((
            By.XPATH, '//input[@aria-label="Search or start a new chat"]'
        )))
        search_box.click()
        search_box.send_keys(Keys.COMMAND + "a")
        search_box.send_keys(Keys.DELETE)
        search_box.send_keys(name)
        sleep(2)
        search_box.send_keys(Keys.ENTER)
        sleep(2)
        
        # confirm chat open
        wait.until(EC.presence_of_element_located((
            By.XPATH, '//span[@data-icon="plus-rounded"] | //span[@data-icon="attach-menu-plus"] | //div[@title="Attach"]'
        )))
        print("✅ Opened via search")
        return True
    except Exception as e:
        print("❌ Search failed:", e)
        return False

# 📱 UNSAVED NUMBER
def open_unsaved_number(number):
    try:
        number = number.strip()
        if len(number) == 10 and number.isdigit():
            number = "91" + number
        print(f"Opening number: {number}")
        driver.get(f"https://web.whatsapp.com/send?phone={number}")
        wait.until(EC.presence_of_element_located((
            By.XPATH, '//div[@title="Type a message"]'
        )))
        print("✅ Opened via number")
        return True
    except Exception as e:
        print("❌ Number failed:", e)
        return False

# 🔥 CLICK ATTACH BUTTON
def click_attach():
    try:
        selectors = [
            '//span[@data-icon="plus-rounded"]',
            '//span[@data-icon="attach-menu-plus"]',
            '//div[@title="Attach"]'
        ]
        btn = None
        for xpath in selectors:
            try:
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                if btn: break
            except: continue
        if not btn: return False
        
        btn.click()
        print("✅ Attach menu opened")
        sleep(2)
        return True
    except:
        return False

# 🔥 SEND MESSAGE WITH DIALOG KILLER
def send_message():
    try:
        # STEP 1: Open attachment menu
        if not click_attach(): return

        # STEP 2: Trigger Document flow to allow captions
        try:
            document_btn = wait.until(EC.presence_of_element_located((
                By.XPATH, "//button[@aria-label='Document'] | //span[text()='Document']/ancestor::button"
            )))
            driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", document_btn)
            sleep(2)
        except Exception as e:
            print(f"❌ Could not trigger Document button: {e}")

        # STEP 3: Inject the file
        try:
            doc_input = wait.until(EC.presence_of_element_located((
                By.XPATH, "//input[@type='file' and @accept='*']"
            )))
            print(f"Uploading: {ATTACHMENT_PATH}")
            doc_input.send_keys(ATTACHMENT_PATH)
            
            # --- 🛡️ DIALOG KILLER (Mac Only) ---
            # Automatically closes the native file browser window if it opened
            os.system("osascript -e 'tell application \"System Events\" to key code 53'")
            
            print("✅ File injected & Window disposed.")
        except Exception as fe:
            print(f"❌ Injection failed: {fe}")
            return

        # STEP 4: Wait for Preview and Type Caption
        print("Waiting for preview screen...")
        sleep(5)
        try:
            caption = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[@contenteditable='true']"
            )))
            caption.click()
            sleep(1)
            for line in MESSAGE.split("\n"):
                ActionChains(driver)\
                    .send_keys(line)\
                    .key_down(Keys.SHIFT)\
                    .send_keys(Keys.ENTER)\
                    .key_up(Keys.SHIFT)\
                    .perform()
            print("✅ Caption typed")
        except Exception as ce:
            print(f"⚠️ Caption box not found: {ce}")
        
        # STEP 5: Click Send
        print("Clicking send button...")
        send_selectors = ["//div[@aria-label='Send']", "//button[@aria-label='Send']", "//span[@data-icon='send']"]
        for sel in send_selectors:
            try:
                send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, sel)))
                send_btn.click()
                print("✅ SENT")
                return
            except: continue
        
        # Fallback to Enter key
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        print("✅ SENT (Fallback)")
        sleep(3)
    except Exception as e:
        print("❌ Send failed:", e)

# ================= MAIN =================

open_whatsapp()

with open(CONTACT_FILE, "r") as f:
    contacts = f.readlines()

for i, contact in enumerate(contacts):
    contact = contact.strip()
    if not contact: continue

    print(f"\n===== {i+1}: {contact} =====")
    if search_contact(contact) or open_unsaved_number(contact):
        send_message()
    else:
        print("❌ Failed to open chat:", contact)

print("\n--- DONE ---")
driver.quit()