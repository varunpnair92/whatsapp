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

contact_file_path = "fboaes"  # Update with the path to your contact file

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
        sleep(2)

        

        # Copy message
        message_box = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//div[@title="Type a message"]')))
        message_text = message_box.get_attribute("title")

        # Send the extracted message
        message_box.clear()  # Clear existing message, if any
        message_lines = [
            "FBOAES Election",
            "",
            "The voting module will be open for four hours from 11.00 a.m. to 3.00 p.m. Voting can be done through Weblink or the FBOAES app on a mobile device or any system.",
            "",
            "Weblink for voting is https://esmembers.fboa.net/",
            "",
            "Link to download Android app: https://play.google.com/store/apps/details?id=com.fbunion.society.Y2023&pli=1",
            "Link to download the IOS app:",
            "",
            "https://apps.apple.com/us/app/fboaes/id1586935729",
            "",
            "Guidelines for the voting",
            "",
            "Access the Weblink from a mobile or laptop.",
            "Enter the mobile number registered with FBOAES",
            "Wait for OTP. OTP will be sent to mobile and to the registered email ID",
            "Enter the OTP received and log in.",
            "Click on the voting button.",
            "Select the candidates for Managing Committee -Women",
            "Click SAVE/ SAVE as a draft",
            "",
            "Select the candidates for Managing Committee - General",
            "Click SAVE/SAVE as a draft.",
            "",
            "Press /click the SUBMIT button. A message to confirm the details will appear. Confirm and SUBMIT",
            "",
            "Voting is online and can be done through a mobile or any system.",
            "We have enabled 50 computers at FISAT additionally.",
            "",
            "If you encounter any problems related to User ID, OTP, or similar issues, please forward them to fboaes@gmail.com.",
            "",
            "5.Helpline",
            "We understand that you may encounter certain situations where you need help. To ensure that we can provide timely and practical support, we have opened a dedicated helpdesk for your assistance",
            "Sri Shinto, +91 85477 04139, FISAT",
            "Sri Sino Varghese, +91 9446719306, FISAT",
            "Sri Rajesh TR, +91 97451 00749, FISAT",
            "Sri Jithesh +91 98474 10018, FISAT",
            "Sri Radhakrishnan, +91 92499 75537, FBOA Office",
            "",
            "Election Commissioners",
            "Sri K R Subramanian, Chief Presiding Officer, 9446934469",
            "Sri C J Augustine, Joint Presiding Officer, 97462 60490"
        ]

        # Join the message lines with new lines
        message_text = "\n".join(message_lines)

        # Send the modified message
        for line in message_text.split("\n"):
            message_box.send_keys(line, Keys.SHIFT, Keys.ENTER)


        send_button_new = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@title="Type a message"]')))
        send_button_new.send_keys(Keys.ENTER)
        success = open("founderssucess", "a+")
        success.write(contact_name + "\n")
        success.close()
        sleep(1)

        print(style.GREEN + 'Message sent to: ' + contact_name + style.RESET)

    except Exception as e:
        failed = open("foundersfail", "a+")
        failed.write(contact_name + "\n")
        failed.close()
        print(style.RED + 'Failed to send message to ' + contact_name + ': ' + str(e) + style.RESET)
    finally:
        # Ensure search box is cleared
        if search_box:
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()

# Read contact names from the file
with open(contact_file_path, "r") as contacts_file:
    for contact in contacts_file.readlines():
        print(style.YELLOW + 'Sending message to ' + contact + '.' + style.RESET)
        print(contact)
        send_message_to_contact(contact)

# Close the browser when done
driver.quit()
