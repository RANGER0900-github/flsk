import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from src.email_scraper import EmailScraper  # Import EmailScraper class
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

running_code = False  # Flag to track if code is running


# Function to sign up with Spotify using a generated email address
def sign_up_with_spotify():
  global running_code
  running_code = True  # Set flag to indicate code is running
  try:
    # Initialize the Chrome driver with options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-browser-side-navigation")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "--ignore-certificate-errors")  # Ignore certificate errors
    chrome_options.add_argument("--ignore-ssl-errors")  # Ignore SSL errors

    # Add additional arguments to handle the close button for cookies
    chrome_options.add_argument(
        "--disable-web-security")  # Disable web security
    chrome_options.add_argument(
        "--allow-running-insecure-content")  # Allow running insecure content

    driver = webdriver.Chrome(ChromeDriverManager().install(),
                              options=chrome_options)

    # Generate a temporary email address
    scraper = EmailScraper(file_path=None)
    email, _ = scraper._EmailScraper__scrape()

    # Navigate to Spotify signup page
    driver.get("https://www.spotify.com/in-en/signup")
    time.sleep(5)  # wait for page to fully load

    # Handle close button for cookies if available
    try:
      close_button = driver.find_element(
          By.CSS_SELECTOR, "#onetrust-close-btn-container button")
      close_button.click()
    except:
      pass  # If close button is not found, continue without clicking

    # Enter email address
    email_input = driver.find_element(By.NAME, "username")
    email_input.send_keys(email)

    # Click next button until redirection to step 1 occurs
    while True:
      try:
        button = driver.find_element(By.CLASS_NAME, "Button-sc-qlcn5g-0")
        button.click()
        WebDriverWait(driver, 1).until(EC.url_contains("#step=1"))
        break  # Break out of the loop if redirection to step 1 occurs
      except:
        continue  # Continue clicking if redirection doesn't occur

    # Enter password
    password = "JAI-SHREE-RAM"
    password_input = driver.find_element(By.NAME, "new-password")
    password_input.send_keys(password)

    # Click next button until redirection to step 2 occurs
    while True:
      try:
        button = driver.find_element(By.CLASS_NAME, "Button-sc-qlcn5g-0")
        button.click()
        WebDriverWait(driver, 1).until(EC.url_contains("#step=2"))
        break  # Break out of the loop if redirection to step 2 occurs
      except:
        continue  # Continue clicking if redirection doesn't occur

    # Enter name
    name_input = driver.find_element(By.NAME, "displayName")
    name_input.send_keys("RAM BHAKT")

    # Enter year of birth
    year_input = driver.find_element(By.NAME, "year")
    year_input.send_keys("1995")

    # Select month
    month_select = driver.find_element(By.NAME, "month")
    driver.execute_script(
        "arguments[0].click();",
        month_select)  # Click to activate the select dropdown
    driver.find_element(By.CSS_SELECTOR,
                        'option[value="3"]').click()  # Select March (value=3)

    # Enter day
    day_input = driver.find_element(By.NAME, "day")
    day_input.send_keys("7")

    # Select gender
    gender_radio = driver.find_element(By.ID, "gender_option_male")
    driver.execute_script("arguments[0].click();", gender_radio)

    # Click next button
    next_button = driver.find_element(By.CLASS_NAME, "Button-sc-qlcn5g-0")
    next_button.click()

    # Click next button until redirection to step 3 occurs
    while True:
      try:
        button = driver.find_element(By.CLASS_NAME, "Button-sc-qlcn5g-0")
        button.click()
        WebDriverWait(driver, 1).until(EC.url_contains("#step=3"))
        break  # Break out of the loop if redirection to step 3 occurs
      except:
        continue  # Continue clicking if redirection doesn't occur

    # Click sign up button
    signup_button = driver.find_element(
        By.CSS_SELECTOR,
        'button[data-testid="submit"][data-encore-id="buttonPrimary"]')
    signup_button.click()

    # Wait for {specified} seconds before closing the browser
    time.sleep(9)

    # Close the browser
    driver.quit()

    # Return email and password
    return email, password
  except Exception as e:
    print(f"An error occurred: {e}")
    return None, None
  finally:
    running_code = False  # Reset flag after code execution


# Root route to prompt user to visit /signup
@app.route('/')
def root():
  return 'Please visit /signup'


# Endpoint for signing up with Spotify
@app.route('/signup')
def signup():
  global running_code
  if running_code:
    return 'Running your code...'  # Display message if code is already running
  else:
    email, password = sign_up_with_spotify(
    )  # Perform sign up with Spotify using a generated email address
    if email and password:
      try:
        # Save account details to accounts.txt
        with open("accounts.txt", "a+") as used_emails_file:
          used_emails_file.write(f"{email}:{password}\n")
        print("Account details written to accounts.txt")
        return f"{email}:{password}"
      except Exception as e:
        print(f"Error writing to accounts.txt: {e}")
        return f"Error creating your account{e}"
    else:
      return "Failed to sign up with Spotify"


# Entry point of the script
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000) 