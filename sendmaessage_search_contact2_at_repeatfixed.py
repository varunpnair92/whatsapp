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

os.environ["WDM_LOG_LEVEL"] = "0"

contact_file_path = "keem2025"
attachment_path = "/home/varun/programs/whatsappmessagesend_pc/KEAM.jpeg"
delay = 10

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

print('Once your browser opens up sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
input("After logging into WhatsApp Web is complete and your chats are visible, press ENTER...")

def send_message_to_contact(contact_name):
    try:
        # Clear the search box before entering the contact name
        search_box = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.clear()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        sleep(1)
        search_box.send_keys(contact_name.strip())
        search_box.send_keys(Keys.ENTER)
        sleep(2)

        # Check if the contact exists
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, '//span[@title="No chats found"]'))
            )
            print(f"Contact '{contact_name.strip()}' not found, skipping.")
            return  # Skip this contact if not found
        except:
            print(f"Contact '{contact_name.strip()}' found, sending message...")

        # Click the attachment button
        attachment_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach" or @aria-label="Attach"]'))
        )
        attachment_button.click()
        sleep(1)

        # Select the attachment file
        document_input = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        )
        document_input.send_keys(attachment_path)
        sleep(1)

        # Click the send button
        send_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-label="Send"]'))
        )
        send_button.click()
        print(f"Message sent to: {contact_name.strip()}")

        # Log the success
        with open("ess", "a+") as success:
            success.write(contact_name.strip() + "\n")

    except Exception as e:
        print(f"Failed to send message to {contact_name.strip()}: {e}")
        # Log the failure
        with open("esf", "a+") as failed:
            failed.write(contact_name.strip() + "\n")
    finally:
        # Clear the search box for the next contact
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        sleep(1)

# Read contacts and send messages
with open(contact_file_path, "r") as contacts_file:
    for i, contact in enumerate(contacts_file.readlines()):
        if i < 3648:
            continue
        if i == 5000:
            break
        print(f"Sending message to {contact.strip()}...")
        send_message_to_contact(contact)

# Close the browser when done
driver.quit()
