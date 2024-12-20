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

fout = open("successnumbers", "a")

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

f = open("msg", "r", encoding="utf8")
successn = open("successnumber", "w")
message = f.read()
f.close()
message2 = ""
with open("mu") as f2:
    for i in f2.readlines():
        message2 += i

f2.close()

print(style.YELLOW + '\nThis is your message-')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)

contact_file_path = "fboaes2024"  # Update with the path to your contact file
attachment_path = "/home/varun/programs/whatsappmessagesend_pc/fisat_channel.jpg"  # Update with the correct path


total_number = 1  # Since you are sending to a single contact

delay = 10

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

print('Once your browser opens up sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
wait = WebDriverWait(driver, 600)
input(style.MAGENTA + "After logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

# Define a function to send a message to a specific contact
def send_message_to_contact(contact_name):
    search_box = None  # Initialize search_box outside the try block to make it accessible in the finally block
    try:
        # Search for the contact
        search_box = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
        # Clear the search box using ActionChains
        search_box.clear()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.ENTER)
        sleep(1)

        # Attach the image
        attachment_button = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach" or @aria-label="Attach"]'))
        )
        attachment_button.click()
        print("Clicked attachment button.")

        document_input = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
        document_input.send_keys(attachment_path)
        sleep(2)
        # Message to be sent
        multiline_message = [
            """From classroom news to campus events, it’s all here!  Follow our WhatsApp Channel to stay ahead with FISAT.\n\nhttps://whatsapp.com/channel/0029Va9Ciik6mYPNN8bzrY3r
            """
        ]
        message_text = "\n".join(multiline_message)
        # Type the message into the message input box
        
        
        

        # Add the caption
        # Add the caption using the specified XPath
        caption_box = WebDriverWait(driver, delay).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-autocomplete='list'][contenteditable='true']"))
        )
        
        for line in message_text.split("\n"):
            caption_box.send_keys(line, Keys.SHIFT, Keys.ENTER)
        sleep(3)
    
        # Send the link to the caption box
        #caption_box.send_keys("""From classroom news to campus events, it’s all here!  Follow our WhatsApp Channel to stay ahead with FISAT.\n\nhttps://whatsapp.com/channel/0029Va9Ciik6mYPNN8bzrY3r""")
        # Send the image with the caption
        send_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
        send_button.click()

        sleep(5)

        success = open("ess", "a+")
        success.write(contact_name + "\n")
        success.close()

        print(style.GREEN + 'Message sent to: ' + contact_name + style.RESET)

    except Exception as e:
        failed = open("esf", "a+")
        failed.write(contact_name + "\n")
        failed.close()
        print(style.RED + 'Failed to send message to ' + contact_name + ': ' + str(e) + style.RESET)
    finally:
        # Ensure search box is cleared
        if search_box:
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()

# Read contact names from the file
with open(contact_file_path, "r") as contacts_file:
    for i, contact in enumerate(contacts_file.readlines()):
        if i < 2068:
            continue
        print(f"send to {i} number")
        if i == 3500:
            break
        contact = contact.strip()
        print(style.YELLOW + 'Sending message to ' + contact + '.' + style.RESET)
        send_message_to_contact(contact)

# Close the browser when done
driver.quit()
