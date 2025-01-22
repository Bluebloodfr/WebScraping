import time
import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re

def gmaps(name, latitude, longitude):
    options = Options()
    options.headless = True  # Désactiver le mode headless pour voir la fenêtre
    driver = webdriver.Firefox(options=options)
    
    try:
        # Set window size
        driver.set_window_size(1920, 1080)

        # Open Google Maps with latitude and longitude
        driver.get(f"https://www.google.com/maps/place/{latitude},{longitude}")

        # Wait for the "Tout accepter" button and click it
        wait = WebDriverWait(driver, 30)  # Augmenter le délai d'attente
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Tout accepter')]")))
        accept_button.click()

        # Wait for the "À proximité" button and click it
        print("Waiting for 'À proximité' button...")
        nearby_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Rechercher à proximité de')]")))
        print("'À proximité' button found, clicking...")
        nearby_button.click()

        # Enter the name and press Enter
        print("Entering name directly into search box...")
        search_box = driver.switch_to.active_element  # Utiliser l'élément actif
        search_box.send_keys(name)
        search_box.send_keys(Keys.ENTER)

        # Wait for the first result and click it
        print("Waiting for the first result...")
        first_result = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class, 'hfpxzc')])[1]")))
        print("First result found, clicking...")
        first_result.click()

        # Wait for the reviews button to load and click it
        print("Waiting for reviews button...")
        reviews_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Avis')]")))
        print("Reviews button found, clicking...")
        reviews_button.click()

        # Wait for reviews to load
        print("Waiting for reviews to load...")
        time.sleep(5)  # Adjust the sleep time if necessary

        # Extract reviews
        reviews = []
        review_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'jftiEf')]")
        for review_element in review_elements:
            try:
                # Extract reviewer name
                reviewer = review_element.find_element(By.XPATH, ".//div[contains(@class, 'd4r55')]").text
                # Extract review text
                review_text = review_element.find_element(By.XPATH, ".//span[contains(@class, 'wiI7pd')]").text

                # Extract rating
                try:
                    rating_element = review_element.find_element(By.XPATH, ".//span[contains(@class, 'kvMYJc')]")
                    rating_text = rating_element.get_attribute('aria-label')
                    rating_match = re.search(r'(\d+)', rating_text)
                    if rating_match:
                        rating = int(rating_match.group(1))
                    else:
                        rating = None
                except:
                    rating = None

                reviews.append({'reviewer': reviewer, 'rating': f"{rating} stars", 'review': review_text})
            except Exception as e:
                print(f"Error extracting review: {e}")

        return reviews

    finally:
        driver.quit()

# Example usage
"""
name = "Gîte WAO: Gîte grande capacité"
latitude = 49.4462476499139
longitude = 5.00500130688476
"""

#Le Panoramic,49.52707,4.782625
name = "Le Panoramic"
latitude = 49.52707
longitude = 4.782625
reviews = gmaps(name, latitude, longitude)
print(reviews)