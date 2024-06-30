from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import os
from time import sleep

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

# Suppressing unnecessary logs
os.environ["WDM_LOG_LEVEL"] = "0"

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

def click_phone_number_link(driver, phone_number):
    try:
        phone_number_link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(., '9495669595')]")))
        phone_number_link.click()
        print(f"Clicked on phone number link: {phone_number}")
    except Exception as e:
        print(style.RED + f"Failed to click on phone number link: {phone_number}. Error: {e}" + style.RESET)

def send_message_to_number(driver, number, message):
    try:
        url = f'https://web.whatsapp.com/send?phone={number}&text={message}'
        driver.get(url)
        send_button_new = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//div[@title="Type a message"]')))
        send_button_new.send_keys(Keys.ENTER)
        sleep(1)
        send_icon = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="send"]')))
        send_icon.click()
        sleep(6)
        print(style.GREEN + 'Message sent to: ' + number + style.RESET)
        with open("successnumber", "a+") as success:
            success.write(number + "\n")
    except Exception as e:
        print(style.RED + 'Failed to send message to ' + number + ' Error: ' + str(e) + style.RESET)
        with open("failednumber", "a+") as failed:
            failed.write(number + "\n")

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

print(style.YELLOW + '\nThis is your message-')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)

numbers = []
f = open("c3", "r")
for line in f.read().splitlines():
    if line.strip() != "":
        numbers.append(line.strip())
f.close()
total_number = len(numbers)
print(style.RED + 'We found ' + str(total_number) + ' numbers in the file' + style.RESET)

delay = 10
s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)
print('Once your browser opens up sign in to web WhatsApp')
driver.get('https://web.whatsapp.com')
wait = WebDriverWait(driver, 600)
input(style.MAGENTA + "AFTER logging into WhatsApp Web is complete and your chats are visible, press ENTER..." + style.RESET)

for number in numbers:
    number = number.strip()
    if number == "":
        continue
    print(style.YELLOW + f'Sending message to {number}.' + style.RESET)
    click_phone_number_link(driver, number)
    send_message_to_number(driver, number, message)

driver.quit()
