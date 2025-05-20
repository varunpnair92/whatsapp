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

# Configure Chrome options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

# Start ChromeDriver
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service, options=options)

# Print welcome message
print("\033[34m**********************************************************")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****           www.github.com/varunpnair92        ******")
print("**********************************************************\033[0m")

# Load student data from CSV
student_records = []
with open("student_data_2025.csv", "r") as f:
    for line in f.readlines():
        sdata = line.strip().split(",")
        if len(sdata) == 5:
            student_id, name, dob, password, phone_number = sdata
            student_records.append((student_id, name, dob.replace("-", ""), password.strip(), phone_number.strip()))

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')
WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
)
input("\033[35mAfter logging into WhatsApp Web is complete and your chats are visible, press ENTER...\033[0m")

# Function to send message to a contact
def send_message(contact_number):
    try:
        # Find student record for this contact
        student_record = next((rec for rec in student_records if rec[4] == contact_number), None)
        if not student_record:
            print(f"\033[31mNo matching student record found for {contact_number}\033[0m")
            return

        student_id, name, dob, password, phone_number = student_record

        # Compose personalized message
        personalized_message = [
            f"Dear {name},",
            "Greetings from FISAT!",
            "You are requested to upload the normalized KEAM score and session percentile of KEAM 2025 for further processing of your application for the B.Tech programme in FISAT using the link given below.",
            "",
            "http://btech-admission.fisat.ac.in/markentry",
            "",
            f"User ID: {student_id}",
            f"Password: {dob} or {password}",
            "",
            "Team FISAT.",
            "Helpline Number: 9446741786"
        ]

        # Search for contact
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        # Clear previous content using ActionChains
        ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        sleep(0.5)
        search_box.send_keys(contact_number)
        sleep(2)
        search_box.send_keys(Keys.ENTER)
        sleep(1)

        # Locate message box
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][contains(@data-tab, "1")]'))
        )

        # Send message with line breaks
        for line in personalized_message:
            message_box.send_keys(line)
            message_box.send_keys(Keys.SHIFT, Keys.ENTER)
        message_box.send_keys(Keys.ENTER)

        print(f"\033[32mMessage sent to {contact_number}\033[0m")
        sleep(1)

    except Exception as e:
        print(f"\033[31mFailed to send message to {contact_number}: {e}\033[0m")

# Read contact numbers from file and send messages
with open("cbse2025", "r") as contacts_file:
    for i, contact in enumerate(contacts_file.readlines()):
        if i < 0:
            continue
        if i == 2500:
            break
        contact = contact.strip()
        print(f"send to {i} number")
        print(f"Sending message to {contact}...")
        send_message(contact)

# Close the browser
driver.quit()
