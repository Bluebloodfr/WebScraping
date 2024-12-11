import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import re

load_dotenv()
ROOT_DIR = os.getenv('ROOT_DIR')

##########################
####### GMAPS REVIEWS ####
##########################

def get_gmaps_reviews(place_id):
    # Configure Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run headless Firefox

    # Set up the Firefox driver
    service = Service('/Users/lmgiraud/bin/geckodriver')  # Update this path if necessary
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # Open Google Maps
    driver.get(f"https://www.google.com/maps/place/?q=place_id:{place_id}")

    # Wait for the "Tout accepter" button and click it
    wait = WebDriverWait(driver, 20)
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Tout accepter')]")))
    accept_button.click()

    # Wait for the reviews button to load and click it
    reviews_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Avis')]")))
    reviews_button.click()

    # Scroll to load more reviews
    for _ in range(5):  # Adjust the range for more reviews
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

    # Extract reviews
    reviews = []
    review_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'jftiEf')]")
    for review_element in review_elements:
        try:
            # Extract reviewer name
            reviewer = review_element.find_element(By.XPATH, ".//div[contains(@class, 'WNxzHc')]//div[contains(@class, 'd4r55')]").text

            # Extract date of review
            date = review_element.find_element(By.XPATH, ".//span[contains(@class, 'rsqaWe')]").text

            # Extract rating
            rating_element = review_element.find_element(By.XPATH, ".//span[contains(@class, 'kvMYJc')]")
            rating_text = rating_element.get_attribute('aria-label')
            rating_match = re.search(r'(\d+)', rating_text)
            if rating_match:
                rating = float(rating_match.group(1))
            else:
                rating = None

            # Extract review text
            text = review_element.find_element(By.XPATH, ".//div[contains(@class, 'MyEned')]").text

            reviews.append({'reviewer': reviewer, 'date': date, 'rating': rating, 'text': text})
        except Exception as e:
            print(f"Error extracting review: {e}")

    # Close the driver
    driver.quit()

    # Convert to DataFrame
    df_reviews = pd.DataFrame(reviews)
    return df_reviews

# https://www.google.com/maps/place/?q=place_id:ChIJdUyx15R95kcRj85ZX8H8OAU
# Exemple d'utilisation
place_id = 'ChIJdUyx15R95kcRj85ZX8H8OAU'  # Chateau de Versailles
reviews_df = get_gmaps_reviews(place_id)
print(reviews_df)