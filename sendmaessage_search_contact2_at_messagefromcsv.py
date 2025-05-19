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

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

service = Service('./chromedriver')
driver = webdriver.Chrome(service=service, options=options)

print("\033[34m**********************************************************")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****           www.github.com/anirudhbagri         ******")
print("**********************************************************\033[0m")

# Load student data
student_records = []
with open("stt.csv", "r") as f:
    for line in f.readlines():
        sdata = line.strip().split(",")
        if len(sdata) == 4:
            student_id, name, dob, phone_number = sdata
            student_records.append((student_id, name, dob, phone_number.strip()))

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
)
input("\033[35mAfter logging into WhatsApp Web is complete and your chats are visible, press ENTER...\033[0m")

def send_message(contact_number):
    try:
        # Find the student record for this contact
        student_record = next((rec for rec in student_records if rec[3] == contact_number), None)
        if not student_record:
            print(f"\033[31mNo matching student record found for {contact_number}\033[0m")
            return
        
        student_id, name, dob, phone_number = student_record
        
        # Prepare multiline message as a list of lines
        personalized_message = [
            f"Dear {name},",
            "Greetings from FISAT!",
            "You are requested to upload the normalized KEAM score and session percentile of KEAM 2025 for further processing of your application for the B.Tech programme in FISAT using the link given below.",
            "",
            "http://btech-admission.fisat.ac.in/markentry",
            "",
            f"User ID: {student_id}",
            f"Password: {dob}",
            "",
            "Team FISAT.",
            "Helpline Number: 9446741786"
        ]

        # Search for the contact
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.clear()
        search_box.send_keys(contact_number)
        sleep(2)
        search_box.send_keys(Keys.ENTER)
        sleep(2)
        
        # Find the message input box
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][contains(@data-tab, "1")]'))
        )
        
        # Send message line by line with SHIFT+ENTER for line breaks
        for line in personalized_message:
            message_box.send_keys(line)
            message_box.send_keys(Keys.SHIFT, Keys.ENTER)
        # Press ENTER to send the message
        message_box.send_keys(Keys.ENTER)
        
        print(f"\033[32mMessage sent to {contact_number}\033[0m")
        sleep(3)

    except Exception as e:
        print(f"\033[31mFailed to send message to {contact_number}: {e}\033[0m")

# Send messages to all contacts
with open("c3", "r") as contacts_file:
    for i, contact in enumerate(contacts_file.readlines()):
        if i == 2500:  # Safety limit to avoid sending too many messages
            break
        contact = contact.strip()
        print(f"Sending message to {contact}...")
        send_message(contact)

# Close the browser when done
driver.quit()
