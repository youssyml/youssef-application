#### IMPORTS ####
##### to random sleep during the script #####
import time
import random

##### to do some text treatment #####
import re

##### picke for storing objects to experiment without scrapping #####
import pickle

##### all selenium related imports #####
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://google.com/maps")

# the WebDriver we will use to wait for elements to load
wait = WebDriverWait(driver, 10)


def accept_conditions():
    """
    Clicks on the Accept all button when opening google maps
    """
    driver.find_element(By.XPATH, "//button[@jsname='b3VHJd']").click()
    time.sleep(random.random() * 5)


# find search input box, write Alan in it and click on search button
def search_for_location():
    """
    Finds the search box, writes Alan in it and clicks search
    """
    # finding the search box and writing Alan in it
    search_box = driver.find_element(By.XPATH, "//input[@id='searchboxinput']")
    search_box.send_keys("Alan")
    time.sleep(random.random() * 5)

    # Clicking on search and waiting for the list of matches loads
    driver.find_element(By.XPATH, "//button[@id='searchbox-searchbutton']").click()
    wait.until(ec.visibility_of_element_located((By.XPATH, "//a[@aria-label='Alan']")))


# Click on first result
def go_to_reviews():
    """
    Clicks on Alan to open its business page. Clicks on the reviews tab.
    Waits for the 1st review to load
    """
    driver.find_element(By.XPATH, "//a[@aria-label='Alan']").click()
    time.sleep(random.random() * 5)

    # Wait until the business page loads and click on the reviews tab
    wait.until(
        ec.visibility_of_element_located((By.XPATH, "//button[@data-tab-index='1']"))
    )
    driver.find_element(By.XPATH, "//button[@data-tab-index='1']").click()
    time.sleep(random.random() * 5)

    # waiting for first review to load
    wait.until(ec.visibility_of_element_located((By.XPATH, "//span[@class='wiI7pd']")))


# Get total number of reviews we expect
def get_total_reviews_count():
    """
    Gets the total number of reviews to scrap
    """
    total_reviews = driver.find_elements(By.XPATH, "//div[@class='jANrlb']//div")
    return int(re.findall("\d+", total_reviews[1].text)[0])


# Returns a sequence of all the review HTML elements for treatment
def get_all_reviews(total_reviews: int):
    """
    Scrolls through all the reviews to handle infinite loading
    Args
        The total count of reviews to scrap
    Returns
        A sequence of review HTML tags to be treated
    """
    # get the elemen on the page that needs to be scrolled
    scrollable_area = driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'm6QErb') and contains(@class, 'DxyBCb') and contains(@class, 'kA9KIf') and contains(@class, 'dS8AEf') and not(contains(@class,'ecceSd'))]",
    )

    reviews_len = 0
    scroll_counts = 0
    while reviews_len < total_reviews:
        scrollable_area.send_keys(Keys.ARROW_DOWN)
        scroll_counts += 1

        # sleep every 10 keys
        if scroll_counts % 10 == 0:
            print("Sleeping for a bit...")
            time.sleep(random.random())

        reviews = driver.find_elements(By.XPATH, "//div[@class='GHT2ce']")
        reviews_len = len(reviews)
        print(reviews_len)

        # click on all "More" buttons
        more_buttons = driver.find_elements(
            By.XPATH,
            "//button[contains(@class, 'w8nwRe') and contains(@class, 'kyuRq')]",
        )

        for mb in more_buttons:
            time.sleep(random.random())
            mb.click()

    return reviews


# Get reviews and process them to extract relevant information


# all scrapping logic
def main():
    accept_conditions()
    search_for_location()
    go_to_reviews()
    total_reviews_count = get_total_reviews_count()
    reviews = get_all_reviews(total_reviews_count)
    reviews = [review.get_attribute("innerHTML") for review in reviews]

    with open("data/reviews_raw.pickle", "wb") as f:
        pickle.dump(reviews, f)


if __name__ == "__main__":
    main()
