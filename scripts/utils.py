""" Script containing utility functions used in the main scripts """

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

def login(driver, username_or_email, password):
    """
    Login to twitter
        Parameters:
            driver (selenium.webdriver.chrome.webdriver.WebDriver): driver on the twitter login page
    """
    # locate username input box
    username_input = driver.find_element_by_xpath('//input[@name="text"]')
    # send username
    username_input.send_keys(f'{username_or_email}') # type username
    # click next
    driver.find_elements_by_xpath('//div[@role="button"]')[2].click()
    # locate password input box
    try:
        password_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
        # send password
        password_input.send_keys(f'{password}') # type password
        # login
        driver.find_elements_by_xpath('//div[@role="button"]')[2].click()
    except:
        print('Slow internet connexion, try again !!!')

def get_username_and_text(tweet):
    """
    Get username and text for the current tweet
        Parameters:
            tweet (selenium.webdriver.remote.webelement.WebElement): tweet box
    """
    try :
        username = tweet.find_element_by_xpath('.//span[contains(text(), "@")]').text
        text = " ".join(tweet.find_element_by_xpath('.//div[@lang]').text.split())
    except :
        username = 'user'
        text = 'text'
    return username, text
