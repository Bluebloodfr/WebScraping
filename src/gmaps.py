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
import streamlit as st

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
                rating = int(rating_match.group(1))
            else:
                rating = None

            # Extract review text
            text = review_element.find_element(By.XPATH, ".//div[contains(@class, 'MyEned')]").text

            reviews.append({'reviewer': reviewer, 'date': date, 'rating': f"{rating} stars", 'text': text})
        except Exception as e:
            print(f"Error extracting review: {e}")

    # Close the driver
    driver.quit()

    # Convert to DataFrame
    df_reviews = pd.DataFrame(reviews)
    return df_reviews

def get_gmaps_reviews_by_name(name, latitude, longitude, debug=False):

    options = Options()
    options.headless = True
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
        short_wait = WebDriverWait(driver, 2)
        try:
            first_result = short_wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(@class, 'hfpxzc')])[1]")))
            print("First result found, clicking...")
            first_result.click()
        except:
            if debug: st.write("")

        # Wait for the reviews button to load and click it
        print("Waiting for reviews button...")
        reviews_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Avis')]")))
        print("Reviews button found, clicking...")
        reviews_button.click()

        # Wait for reviews to load
        print("Waiting for reviews to load...")
        time.sleep(1)  # Adjust the sleep time if necessary

        # Scroll to load more reviews
        try:
            scrollable_div_center = driver.find_element(
                By.CSS_SELECTOR,
                "div.bJzME.Hu9e2e.tTVLSc div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde"
            )
            for _ in range(3):
                driver.execute_script("arguments[0].scrollBy(0, 500)", scrollable_div_center)
                time.sleep(1)
        except:
            print("Middle reviews container not found, skipping scroll.")

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

# https://www.google.com/maps/place/?q=place_id:ChIJdUyx15R95kcRj85ZX8H8OAU
# Exemple d'utilisation
# place_id = 'ChIJdUyx15R95kcRj85ZX8H8OAU'  # Chateau de Versailles
# reviews_df = get_gmaps_reviews(place_id)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.expand_frame_repr', False)
# print(reviews_df)
# print(reviews_df.head())