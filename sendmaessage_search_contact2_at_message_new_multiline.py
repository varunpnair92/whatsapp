from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import os
from time import sleep

# Selenium WebDriver options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

os.environ["WDM_LOG_LEVEL"] = "0"

# ANSI escape sequences for colored console output
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

# Display the initial message
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

# Read message from file
f = open("msg", "r", encoding="utf8")
message = f.read()
f.close()

print(style.YELLOW + '\nThis is your message-')
print(style.GREEN + message)
print("\n" + style.RESET)

# Define the paths to your contact file and attachment
contact_file_path = "csdmq"  # Update with the path to your contact file
attachment_path = "/home/varun/programs/whatsappmessagesend_pc/INDUCTION.jpeg"  # Update with the correct path

delay = 10

# Initialize WebDriver
s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

print('Once your browser opens up sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
wait = WebDriverWait(driver, 600)
input(style.MAGENTA + "After logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

# Function to send a message to a contact
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

        # Message to be sent
        multiline_message = [
            """Dear student,\nThis WhatsApp group was created to make college uniforms available to students as soon as possible.\nPlease join the WhatsApp group using the following Link.\n\nhttps://chat.whatsapp.com/I9tDesRKrOQKjdANWKZZDX\n\nFISAT.
            """
        ]
        message_text = "\n".join(multiline_message)
        # Type the message into the message input box
        message_box = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][contains(@data-tab, "1")]')))
        
        for line in message_text.split("\n"):
            message_box.send_keys(line, Keys.SHIFT, Keys.ENTER)
        sleep(3)
        # Attach the image
        attachment_button = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
        attachment_button.click()
        print("Clicked attachment button.")

        document_input = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
        document_input.send_keys(attachment_path)
        sleep(2)

        # Send the message and attachment
        send_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
        send_button.click()

        sleep(5)
        
        # Log success
        with open("ess", "a+") as success:
            success.write(contact_name + "\n")

        print(style.GREEN + 'Message sent to: ' + contact_name + style.RESET)

    except Exception as e:
        # Log failure
        with open("esf", "a+") as failed:
            failed.write(contact_name + "\n")
        print(style.RED + f'Failed to send message to {contact_name}: {str(e)}' + style.RESET)
    finally:
        if search_box:
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()

# Read contact names from the file
with open(contact_file_path, "r") as contacts_file:
    for i, contact in enumerate(contacts_file.readlines()):
        if i < 0:
            continue
        print(f"Sending to {i} number")
        if i == 2500:
            break
        print(style.YELLOW + 'Sending message to ' + contact.strip() + '.' + style.RESET)
        send_message_to_contact(contact.strip())

# Close the browser when done
driver.quit()
