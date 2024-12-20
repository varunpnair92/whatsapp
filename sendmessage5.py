from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from urllib.parse import quote
import os
import time

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"

class style:
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

with open("successnumbers", "a") as fout, open("msg", "r", encoding="utf8") as f, open("mu") as f2, open("c3", "r") as f3:
    message = f.read().strip()
    message2 = f2.read().strip()
    numbers = [line.strip() for line in f3.read().splitlines() if line.strip()]

print(style.YELLOW + '\nThis is your message:')
print(style.GREEN + message)
print("\n" + style.RESET)

message = quote(message)
total_number = len(numbers)
print(style.RED + 'We found ' + str(total_number) + ' numbers in the file' + style.RESET)

delay = 30
s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)

print('Once your browser opens up, sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
wait = WebDriverWait(driver, 600)
input(style.MAGENTA + "AFTER logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

def accept_alert_if_present(driver):
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(style.RED + f"Unexpected alert present: {alert_text}. Accepting it." + style.RESET)
        alert.accept()
        return True
    except NoAlertPresentException:
        return False

def send_message_to_number(driver, number, message, delay):
    url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
    for attempt in range(3):  # Retry up to 3 times
        try:
            driver.get("about:blank")  # Open a blank page first to ensure a fresh start
            driver.get(url)
            print(style.BLUE + f"Attempt {attempt + 1}: Opened URL: {url}" + style.RESET)

            # Wait until the chat is loaded
            WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, '//div[@title="Attach"]'))
            )

            # Click attachment button
            attachment_button = WebDriverWait(driver, delay).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@title="Attach"]')))
            attachment_button.click()
            print("Clicked attachment button.")
            time.sleep(1)

            # Upload document
            document_input = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
            document_input.send_keys("/home/varun/programs/whatsappmessagesend_pc/FISATEXAM.jpeg")
            print("Attached document.")
            time.sleep(1)
            
            # Click send button
            send_icon = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="send"]')))
            send_icon.click()
            print("Message sent.")
            time.sleep(2)
            
            return True
        except UnexpectedAlertPresentException:
            print(style.RED + "Unexpected alert detected. Accepting it." + style.RESET)
            accept_alert_if_present(driver)
            time.sleep(5)  # Wait a bit before retrying
        except Exception as e:
            print(style.RED + f"Error while sending message: {e}" + style.RESET)
            accept_alert_if_present(driver)
            time.sleep(5)  # Introduce a small delay before retrying

    return False

for idx, number in enumerate(numbers):
    number = number.strip()
    if not number:
        continue

    print(style.YELLOW + '{}/{} => Sending message to {}.'.format((idx + 1), total_number, number) + style.RESET)

    sent = send_message_to_number(driver, number, message, delay)
    # if sent:
    #     fout.write(number + "\n")
    # else:
    #     print(style.RED + 'Failed to send message to ' + number + style.RESET)
    #     with open("foundersfail", "a+") as failed:
    #         failed.write(number + "\n")

driver.quit()
