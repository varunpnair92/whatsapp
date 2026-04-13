from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

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
    input("Login WhatsApp Web and press ENTER...")


# 🔍 SEARCH CONTACT (NEW INPUT BASED)
def search_contact(name):
    try:
        print(f"Searching: {name}")

        search_box = wait.until(EC.presence_of_element_located((
            By.XPATH, '//input[@aria-label="Search or start a new chat"]'
        )))

        search_box.click()
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        search_box.send_keys(name)

        sleep(2)

        search_box.send_keys(Keys.ENTER)
        sleep(2)

        # confirm chat open
        wait.until(EC.presence_of_element_located((
            By.XPATH, '//span[@data-icon="attach-menu-plus"] | //span[@data-icon="plus-rounded"] | //div[@title="Attach"]'
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


# 🔥 CLICK ATTACH BUTTON (ENHANCED)
def click_attach():
    try:
        print("Opening attachment menu...")
        selectors = [
            '//*[@id="main"]/footer/div[1]/div/span/div/div/div/div[1]/div/span/button',
            '//span[@data-icon="plus-rounded"]',
            '//span[@data-icon="attach-menu-plus"]',
            '//div[@title="Attach"]',
            '//button[@title="Attach"]'
        ]
        
        btn = None
        for xpath in selectors:
            try:
                btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                if btn: break
            except: continue
            
        if not btn: raise Exception("Attach button not found")
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        sleep(1)
        try: btn.click()
        except: driver.execute_script("arguments[0].click();", btn)
        
        print("✅ Attach button clicked")
        sleep(2)  # Wait for menu to open
        return True
    except Exception as e:
        print(f"❌ Failed to click attach: {e}")
        return False


# 🔥 SEND MESSAGE WITH DOCUMENT (FINAL REFINED)

def send_message():
    try:
        # STEP 1: Open attachment menu
        if not click_attach():
            return

        # STEP 2: Find the 'Document' button and trigger the file input injection
        print("Locating Document button and triggering input injection...")
        try:
            # Re-check for the button in the menu
            document_btn = wait.until(EC.presence_of_element_located((
                By.XPATH, "//button[@aria-label='Document'] | //span[text()='Document']/ancestor::button"
            )))
            
            # Using JS to trigger the click logic to ensure the <input accept="*"> is created
            driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", document_btn)
            print("✅ Document injection triggered via JavaScript")
            sleep(2)
        except Exception as e:
            print(f"❌ Could not trigger Document button: {e}")
            # Fallback to looking for the input if it's already there
            pass

        # STEP 3: Find the document-specific file input and inject the file
        print("Locating document file input (accept='*')...")
        try:
            # We specifically look for accept="*" which is the document flow
            doc_input = wait.until(EC.presence_of_element_located((
                By.XPATH, "//input[@type='file' and @accept='*']"
            )))
            print(f"Uploading: {ATTACHMENT_PATH}")
            doc_input.send_keys(ATTACHMENT_PATH)
            print("✅ File injected into document input")
        except Exception as fe:
            print(f"❌ Document input not found after trigger: {fe}")
            return

        # STEP 4: Wait for the document preview screen to appear
        print("Waiting for document preview screen...")
        sleep(6)

        # STEP 5: Type the caption message in the preview screen
        print("Typing caption message...")
        try:
            # Use a selector that targets the preview screen's caption box
            caption = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[@contenteditable='true']"
            )))
            caption.click()
            sleep(1)
            # Clear any default text if necessary (though usually empty)
            for line in MESSAGE.split("\n"):
                ActionChains(driver)\
                    .send_keys(line)\
                    .key_down(Keys.SHIFT)\
                    .send_keys(Keys.ENTER)\
                    .key_up(Keys.SHIFT)\
                    .perform()
            print("Caption typed")
        except Exception as ce:
            print(f"⚠️ Caption box not found: {ce}")
        sleep(2)

        # STEP 6: Click the send button (circular blue button in preview)
        print("Clicking send button...")
        send_selectors = [
            "//div[@aria-label='Send']",
            "//button[@aria-label='Send']",
            "//span[@data-icon='send']",
            "//span[@data-icon='wds-ic-send-filled']"
        ]
        sent = False
        for sel in send_selectors:
            try:
                send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, sel)))
                send_btn.click()
                print(f"✅ Sent successfully using selector: {sel}")
                sent = True
                break
            except Exception:
                continue
        if not sent:
            print("⚠️ Send button not found, falling back to ENTER key")
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            print("✅ Sent via Enter key fallback")
        sleep(3)
    except Exception as e:
        print("❌ Send failed:", e)

# ================= MAIN =================

open_whatsapp()

with open(CONTACT_FILE, "r") as f:
    contacts = f.readlines()

for i, contact in enumerate(contacts):
    contact = contact.strip()

    if not contact:
        continue

    print(f"\n===== {i+1}: {contact} =====")

    opened = search_contact(contact)

    if not opened:
        opened = open_unsaved_number(contact)

    if opened:
        send_message()
    else:
        print("❌ Completely failed:", contact)

driver.quit()