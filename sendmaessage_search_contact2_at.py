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

contact_file_path = "fisatallmathews2025"  # Update with the path to your contact file
attachment_path = "/path/to/your/attachment/file.jpg"  # Update with the correct path


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


        # #attach message
        # # Copy message
        # message_box = WebDriverWait(driver, delay).until(
        #     EC.presence_of_element_located((By.XPATH, '//div[@title="Type a message"]')))
        # message_text = message_box.get_attribute("title")

        # # Send the extracted message
        # message_box.clear()  # Clear existing message, if any
        # message_box.send_keys("""Dear parent,
        # FISAT is organising a discussion on "Student's Emotional Wellbeing". Kindly make it convienent to attend the same.\n""")

        

        # Send message with attachment 1
        #this old methos work upto 22-11-2024
        # attachment_button = WebDriverWait(driver, delay).until(
        #     EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
        #new method implemted on 23-11-2024
        attachment_button = WebDriverWait(driver, delay).until(
        EC.element_to_be_clickable((By.XPATH, '//button[@title="Attach" or @aria-label="Attach"]'))
        )
        attachment_button.click()
        print("Clicked attachment button.")

        document_input = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
        document_input.send_keys(
                        "/home/varun/programs/whatsappmessagesend_pc/VIDYARAMBHAM 2025.pdf")
        sleep(2)
        # send_button_new = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(
        #                 (By.XPATH, '//div[@title="Type a message"]')))
        # send_button_new.send_keys(Keys.ENTER)
        try:
            # Wait for the send button to be clickable
            send_button = WebDriverWait(driver, delay).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and @aria-label="Send"]'))
            )
            send_button.click()
            print("Attachment sent successfully.")
        except Exception as e:
            print("Failed to click the send button:", e)


        sleep(15)
        

        # # Send message with attachment2
        # attachment_button = WebDriverWait(driver, delay).until( 
        #EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
        #arts ios the best jaikaiiiiisiisiiiiiikgyikfgylcarts is the bst in ktge world is the bewst intg attachment_button.click()
        # print("Clicked attachment button.")

        # document_input = WebDriverWait(driver, delay).until(
        #                 EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
        # document_input.send_keys(
        #                 "/home/user/whatsappmessagesend_pc/FISATS2.jpeg")
        # sleep(1)
        # send_button_new = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(
        #                 (By.XPATH, '//div[@title="Type a message"]')))
        # send_button_new.send_keys(Keys.ENTER)
        # sleep(2)


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
    
    for i,contact in enumerate(contacts_file.readlines()):
        if i<561:
            continue
        print(f"send to {i} number")
        if i==3000:
            break
        print(style.YELLOW + 'Sending message to ' + contact + '.' + style.RESET)
        print(contact)
        send_message_to_contact(contact)

# Close the browser when done
driver.quit()
