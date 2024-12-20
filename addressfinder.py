from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

# Set up Chrome options
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")

# Function to automate Google search and extract the address
def extract_address_from_google(query):
    # Set up the Chrome driver (make sure you have chromedriver installed)
    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s, options=options)

    # Open Google
    driver.get('https://www.google.com')

    # Locate the search bar, type the query, and perform the search
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    input()

    # Wait for the results to load (you can increase this time if needed)
    time.sleep(3)

    try:
        # Locate the address element based on the CSS selector for the div containing the address
        address_element = driver.find_element(By.CSS_SELECTOR, "div.sXLaOe")

        # Extract the text (address) from the element
        address = address_element.text
        print(f"Address found: {address}")
    
    except Exception as e:
        print(f"Error while extracting address: {e}")

    # Close the browser window
    driver.quit()

# Search query
query = "Bhavans Varuna Vidyalaya,Thrikkakara address"

# Call the function to extract the address
extract_address_from_google(query)
