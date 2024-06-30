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
f = open("c3", "r")
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
        for i in range(2):
            if not sent:
                driver.get(url)
                try:

                    print("Found send button.")

                except Exception as e:
                    print(
                        style.RED + f"\nFailed to send message to: {number}, retry ({i+1}/3)")
                    print(
                        "Make sure your phone and computer are connected to the internet.")
                    print("If there is an alert, please dismiss it." + style.RESET)
                    print("Error:", str(e))
                else:
                    

                    send_button_new = WebDriverWait(driver, delay).until(EC.element_to_be_clickable(
                        (By.XPATH, '//div[@title="Type a message"]')))
                    
                    send_button_new.send_keys(Keys.ENTER)
                    #sleep(1)
                    # send_icon = WebDriverWait(driver, 10).until(
                    # EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="send"]'))
                    # )

                    
                    # send_icon.click()

                    # text_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "selectable-text copyable-text iq0m558w g0rxnol2")))
                    # text_box.send_keys(message2+Keys.ENTER)
                    # send_button.send_keys(message2+Keys.ENTER)
                    print("Clicked send button.")
                    sleep(7)

                    # sent_confirmation = WebDriverWait(driver, 10).until(
                    #     EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Message sent"]')))

                    sent = True

                    print(style.GREEN + 'Message sent to: ' +
                          number + style.RESET)
                    success = open("foundersuccess", "a+")
                    success.write(number+"\n")
                    success.close()
            else:
                break
    except Exception as e:
        print(style.RED + 'Failed to send message to ' +
              number + str(e) + style.RESET)
        failed = open("founderfail", "a+")
        failed.write(number+"\n")
        failed.close()


# Close the browser when done
driver.quit()
