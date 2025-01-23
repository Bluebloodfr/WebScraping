import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_poi(driver, name):
    # Define waiting time
    long_wait = WebDriverWait(driver, 30)
    short_wait = WebDriverWait(driver, 2)

    # click "Tout accepter"
    accept_button = long_wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@aria-label, 'Tout accepter')]"))
    )
    accept_button.click()

    # click "À proximité"
    nearby_button = long_wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@aria-label, 'Rechercher à proximité de')]")
    ))
    nearby_button.click()

    # search the POI name
    search_box = driver.switch_to.active_element
    search_box.send_keys(name)
    search_box.send_keys(Keys.ENTER)

    try:
        # click first result
        first_result = long_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//a[contains(@class, 'hfpxzc')])[1]")
        ))
        first_result.click()

        # click reviews button
        reviews_button = short_wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@aria-label, 'Avis')]")
        ))
        reviews_button.click()

        try:
            scrollable_div_center = driver.find_element(
                By.CSS_SELECTOR, "div.bJzME.Hu9e2e.tTVLSc div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde"
            )
            for _ in range(3):
                driver.execute_script("arguments[0].scrollBy(0, 500)", scrollable_div_center)
        except Exception:
            print(Exception)
    except Exception:
            print(Exception)


def extract_review(driver):
    reviews = []
    review_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'jftiEf')]")
    for review_element in review_elements:
        reviewer = review_element.find_element(By.XPATH, ".//div[contains(@class, 'd4r55')]").text
        review_text = review_element.find_element(By.XPATH, ".//span[contains(@class, 'wiI7pd')]").text

        try:
            rating_element = review_element.find_element(By.XPATH, ".//span[contains(@class, 'kvMYJc')]")
            rating_text = rating_element.get_attribute('aria-label')
            rating_match = re.search(r'(\d+)', rating_text)
            if rating_match:
                rating = int(rating_match.group(1))
            else:
                rating = -1
        except:
            rating = -1

        reviews.append({'reviewer': reviewer, 'rating': rating, 'review': review_text })
    
    return reviews


def get_reviews(row):
    # Extract inputs
    name = row['nom']
    latitude = row['latitude']
    longitude = row['longitude']

    firefox_options = Options()
    firefox_options.add_argument("--headless") 
    driver = webdriver.Firefox(options=firefox_options)

    # service = Service('/Users/lmgiraud/bin/geckodriver')
    #driver = webdriver.Firefox(service=service, options=firefox_options)
    
    driver.get(f"https://www.google.com/maps/place/{latitude},{longitude}")
    find_poi(driver, name)
    reviews = extract_review(driver)

    driver.quit()
    return reviews
        

# https://www.google.com/maps/place/?q=place_id:ChIJdUyx15R95kcRj85ZX8H8OAU
# Exemple d'utilisation
# place_id = 'ChIJdUyx15R95kcRj85ZX8H8OAU'  # Chateau de Versailles
# reviews_df = get_gmaps_reviews(place_id)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.expand_frame_repr', False)
# print(reviews_df)
# print(reviews_df.head())