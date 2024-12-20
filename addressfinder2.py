import csv
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
#options.add_argument("--headless")  # Enables headless mode (uncomment if needed)

# Function to automate Google search and extract the address
def extract_address_from_google(query, driver):
    # Open Google (if not already opened)
    if driver.current_url != 'https://www.google.com':
        driver.get('https://www.google.com')

    # Locate the search bar, type the query, and perform the search
    search_box = driver.find_element(By.NAME, 'q')
    search_box.clear()  # Clear the search box before typing the new query
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load (you can increase this time if needed)
    time.sleep(3)

    try:
        # Locate the address element based on the CSS selector
        address_element = driver.find_element(By.CSS_SELECTOR, "div.sXLaOe")

        # Extract the text (address) from the element
        address = address_element.text
        print(f"Address found: {address}")
        return address
    
    except Exception as e:
        print(f"Error while extracting address: {e}")
        return None

# Function to process the CSV file
def process_csv(input_file, output_file):
    # Set up the Chrome driver (make sure you have chromedriver installed)
    s = Service('./chromedriver')
    driver = webdriver.Chrome(service=s, options=options)

    # Open Google initially
    driver.get('https://www.google.com')

    # Read the CSV file
    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Open a new CSV file for writing the results
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        for row in rows:
            if len(row) > 1:
                name = row[0]
                address = row[1]
                # Append "address" to the second column
                query = address + " address"
                
                # Call the function to get the full address from Google
                extracted_address = extract_address_from_google(query, driver)
                
                # If the address was found, write it to the 4th column
                if extracted_address:
                    row.append(extracted_address)
                else:
                    row.append("Address not found")
                
            # Write the row to the new CSV file
            writer.writerow(row)

    # Close the browser window after processing
    driver.quit()

# Input CSV file path
input_file = 'schools.csv'  # Replace with your input CSV file path
output_file = 'output.csv'  # Output file where the results will be stored

# Process the CSV file
process_csv(input_file, output_file)
