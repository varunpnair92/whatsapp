from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

# Configure Chrome options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

# Start ChromeDriver
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service, options=options)

# Welcome message
print("\033[34m**********************************************************")
print("*****  THANK YOU FOR USING WHATSAPP BULK MESSENGER  ******")
print("*****           www.github.com/varunpnair92        ******")
print("**********************************************************\033[0m")

# Load student data
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
input("\033[35mAfter logging into WhatsApp Web and your chats are visible, press ENTER to start sending...\033[0m")

def send_message(contact_number):
    try:
        # Find student record
        student_record = next((rec for rec in student_records if rec[4] == contact_number), None)
        if not student_record:
            print(f"\033[31mNo student record for {contact_number}. Skipping...\033[0m")
            return

        student_id, name, dob, password, phone_number = student_record

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
        # Clear previous search
        ActionChains(driver).click(search_box).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        sleep(0.5)

        search_box.send_keys(contact_number)
        sleep(2)
        search_box.send_keys(Keys.ENTER)
        sleep(1)

        # Sometimes ENTER opens chat directly, but sometimes need to click first chat option
        try:
            first_chat = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@role="option"]'))
            )
            first_chat.click()
            sleep(1)
        except:
            pass  # If no chat option or ENTER opened chat, continue

        # Verify message box appeared (contact found)
        try:
            message_box = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
        except:
            print(f"\033[33mContact {contact_number} not found or chat not opened. Skipping...\033[0m")
            return

        # Focus message box and send message
        message_box.click()
        sleep(0.5)
        for line in personalized_message:
            message_box.send_keys(line)
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            sleep(0.1)
        message_box.send_keys(Keys.ENTER)

        print(f"\033[32mMessage sent to {contact_number}\033[0m")
        sleep(1)

    except Exception as e:
        print(f"\033[31mError sending to {contact_number}: {e}\033[0m")

# Read contacts and send messages
with open("cbse2025", "r") as contacts_file:
    for i, contact in enumerate(contacts_file.readlines()):
        if i < 153:  # adjust if you want to skip headers or initial rows
            continue
        if i == 2500:  # limit number of messages
            break
        contact = contact.strip()
        print(f"Sending message to {contact} ({i})...")
        send_message(contact)

# Close browser
driver.quit()
