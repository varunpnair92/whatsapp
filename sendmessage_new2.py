from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from urllib.parse import quote
import os

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

# message2 = f2.read()
f2.close()

print(style.YELLOW + '\nThis is your message-')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)
# message2 = quote(message2)

# message=""

numbers = []
f = open("parent1", "r")
for line in f.read().splitlines():
    if line.strip() != "":
        numbers.append(line.strip())
f.close()
total_number = len(numbers)
print(style.RED + 'We found ' + str(total_number) +
      ' numbers in the file' + style.RESET)
delay = 10

s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

#driver = webdriver.Chrome('./chromedriver', options=options)
#driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

print('Once your browser opens up sign in to web whatsapp')
driver.get('https://web.whatsapp.com')
wait = WebDriverWait(driver, 600)
input(style.MAGENTA + "AFTER logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

# ... (previous code)

# Loop through numbers and send messages
# ... (previous code)

# Loop through numbers and send messages
# ... (previous code)

# Loop through numbers and send messages
# ... (previous code)

# ... (previous code)

for idx, number in enumerate(numbers):
    number = number.strip()
    if number == "":
        continue
    print(style.YELLOW + '{}/{} => Sending message to {}.'.format((idx+1),
          total_number, number) + style.RESET)
    try:
        url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
        fout.write(number + "\n")
        sent = False
        attached = False

        for i in range(1):  # Retry up to 3 times
            driver.get(url)

            try:
                # Wait for the chat window to open
                # chat_window = WebDriverWait(driver, delay).until(
                #     EC.presence_of_element_located((By.XPATH, '//div[@class="_3u328 copyable-text selectable-text"]')))
                
                attachment_button = WebDriverWait(driver, delay).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
                attachment_button.click()
                print("Chat window opened.")
            except Exception as e:
                print(style.RED + f"\nFailed to open chat window for: {number}, retry ({i+1}/3)")
                print("Error:", str(e))
                continue

            try:
                # Attach the document
                attachment_button = WebDriverWait(driver, delay).until(
                        EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
                attachment_button.click()
                print("Clicked attachment button.")

                document_input = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                document_input.send_keys(
                        "/home/user/whatsapp_indepndent_latest_use_this/FISATNEW.jpeg")
                sleep(1)
                attached=True
                print("Attached document.")
                # document_input.send_keys(message2+Keys.ENTER)
                # Send the message

                # working part
                # send_button = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(
                #     (By.XPATH, '//span[@data-icon="send"]')))
                # send_button.click()

                send_button_new = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@title="Type a message"]')))
                # sleep(2)
                send_button_new.send_keys(Keys.ENTER)
                # send_button_new.send_keys(Keys.ENTER)
                sleep(1)
                # send_icon = WebDriverWait(driver, 10).until(
                #         EC.presence_of_element_located(
                #             (By.CSS_SELECTOR, 'span[data-icon="send"]'))
                #     )

                #     # Click the send icon
                # send_icon.click()
                sleep(4)
                sent = True
                print(style.GREEN + 'Message sent to: ' + number + style.RESET)
                success = open("successtnew", "a+")
                success.write(number+"\n")
                success.close()
            except Exception as e:
                if attached:
                    print(style.GREEN + 'Message sent to: ' + number + style.RESET)
                    success = open("successtnew", "a+")
                    success.write(number+"\n")
                    success.close()
                else:
                    print(style.RED + 'Failed to send message to ' + number + str(e) + style.RESET)
                    failed = open("failedtnew", "a+")
                    failed.write(number+"\n")
                    failed.close()
    except Exception as e:
        print(style.RED + f'Error processing {number}: {str(e)}' + style.RESET)

# ... (remaining code)

# Close the browser when done
driver.quit()
