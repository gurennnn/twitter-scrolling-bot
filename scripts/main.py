""" Main script for building the bot, scrolling and scraping tweets """

# import libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
from utils import *

# setup the driver
url = 'https://twitter.com/search?q=programming&src=typed_query'
driver = webdriver.Chrome()
driver.get(url)
driver.maximize_window()

# wait a bit after screen is maximized for login
time.sleep(5)
login(driver)

# initialize lists
usernames = []
texts = []
ids = set()

# scrolling condition
scrolling = True

while scrolling:
    # locate tweets that are loaded
    time.sleep(3)
    tweets = driver.find_elements_by_xpath('//article[@role="article"]')
    for tweet in tweets:
        username, text = get_username_and_text(tweet)
        id = ''.join([username, text])
        # check if the current tweet wasn't already retrieved
        if id not in ids:
            ids.add(id)
            usernames.append(username)
            texts.append(text)
    # scroll down after scraping the current content
    last_height = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    new_height = driver.execute_script('return document.body.scrollHeight')
    # condition 1 when we reach the limit of the desired content
    # condition 2 for reaching the end of the page
    if (len(usernames) > 50) or (last_height == new_height): # quit scrolling
        scrolling = False

# wait after content is scraped and quit
time.sleep(1)
driver.quit()

# create pandas dataframe and export it in a csv file
df = pd.DataFrame({
    'username': usernames,
    'text': texts
})
df.to_csv('./data/tweets.csv', index=False)