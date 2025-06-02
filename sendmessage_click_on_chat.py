from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re

# === CONFIG ===
CHROMEDRIVER_PATH = './chromedriver'  # Update path if needed
CHAT_NAME = 'Varunettan'  # Replace with the name of the chat where numbers are pasted
WAIT_TIME = 20

# === SETUP SELENIUM ===
options = Options()
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")
options.add_argument("--profile-directory=Default")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# === STEP 1: OPEN WHATSAPP WEB ===
driver.get("https://web.whatsapp.com")
WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
)
input("✅ After WhatsApp is fully loaded and chats are visible, press ENTER...")

# === STEP 2: OPEN THE CHAT WHERE NUMBERS ARE PASTED ===
search_box = WebDriverWait(driver, WAIT_TIME).until(
    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
)
search_box.clear()
search_box.send_keys(CHAT_NAME)
sleep(2)
search_box.send_keys(Keys.ENTER)
sleep(2)

# === STEP 3: EXTRACT NUMBERS FROM MESSAGE BUBBLES ===
message_bubbles = driver.find_elements(By.XPATH, "//div[contains(@class,'message-in')]//div[@class='_21Ahp']")
numbers = set()

for bubble in message_bubbles:
    text = bubble.text
    found = re.findall(r"\b\d{7,15}\b", text)  # Match numbers (7-15 digits)
    for number in found:
        number = number.strip().replace(" ", "").replace("-", "")
        if number:
            numbers.add(number)

print(f"📦 Found {len(numbers)} numbers in chat:\n{sorted(numbers)}")

# === STEP 4: SEARCH AND OPEN CHATS ===
for number in numbers:
    try:
        print(f"\n🔍 Searching for: {number}")
        # Click search and enter number
        search_box = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        )
        search_box.clear()
        sleep(0.5)
        search_box.send_keys(number)
        sleep(3)

        # Check for chat result
        result = driver.find_elements(By.XPATH, f"//span[@title='{number}']")
        if result:
            result[0].click()
            print(f"✅ Opened chat with {number}")
            sleep(3)
            driver.back()
            sleep(1)
        else:
            print(f"❌ Chat not found for: {number}")
    except Exception as e:
        print(f"⚠️ Error for {number}: {e}")

print("\n✅ DONE")
driver.quit()
