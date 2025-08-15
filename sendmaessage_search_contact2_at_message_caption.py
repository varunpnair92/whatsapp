from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import quote
import os
from time import sleep

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"

class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(style.BLUE)
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****      This tool was built by Anirudh Bagri     ******")
print("*****           www.github.com/anirudhbagri         ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(style.RESET)

contact_file_path = "c3"  # contacts list
delay = 10

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

print('Once your browser opens up sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
WebDriverWait(driver, 600)  # wait for QR login
input(style.MAGENTA + "After logging into WhatsApp Web is complete and chats are visible, press ENTER..." + style.RESET)

# Caption text
caption_text = """Dear all
There will be an introductory session for the day scholars. Students who are staying nearby can attend the same as informed earlier. Students who had remitted college bus fee can travel in the college bus. Timing and details are given in website also. Students can join the programme by online also.

Details of college bus, Help line numbers are given in website

https://youtube.com/live/6oA3ABA9bkM?feature=share
"""

attachment_path = "/home/varun/programs/whatsappmessagesend_pc/BusRouteTiming.pdf"

def send_message_to_contact(contact_name):
    search_box = None
    try:
        # Search for the contact
        search_box = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        search_box.clear()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.ENTER)
        sleep(1)

        # Click the attachment button
        attachment_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach" or @aria-label="Attach"]'))
        )
        attachment_button.click()
        print("Clicked attachment button.")

        # Upload the file
        document_input = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime,application/pdf"]'))
        )
        document_input.send_keys(attachment_path)
        sleep(2)  # wait for preview to load

        # Type caption into the message box (after file upload)
        caption_box = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][contains(@data-tab,"6")]'))
        )
        for line in caption_text.split("\n"):
            if line.strip() == "":
                caption_box.send_keys(Keys.SHIFT, Keys.ENTER)  # line break
            else:
                caption_box.send_keys(line)
                caption_box.send_keys(Keys.SHIFT, Keys.ENTER)

        # Click send button
        send_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-label="Send"]'))
        )
        send_button.click()
        print(style.GREEN + f'Message + attachment sent to: {contact_name}' + style.RESET)

        sleep(2)

    except Exception as e:
        print(style.RED + f'Failed to send to {contact_name}: {e}' + style.RESET)
    finally:
        # Clear search box for next contact
        if search_box:
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()

# Loop through contacts
with open(contact_file_path, "r") as contacts_file:
    for i, contact in enumerate(contacts_file.readlines()):
        contact = contact.strip()
        if not contact:
            continue
        print(style.YELLOW + f'Sending to {contact}' + style.RESET)
        send_message_to_contact(contact)

driver.quit()
