from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import re
import time
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')



def agreeCookies(webDriver):
    # select element of cookie agree button and press it
    cookieAgreeElem = webDriver.find_element_by_id('cookie_bar_agree_button')

    cookieAgreeElem.click()


def signIn(webDriver, accountInfo):
    """Sign in to catawiki. Takes the arguments webDriver, and accountInfo. accountInfo is a list with index 0 being
    the desired username and index 1 being the password"""
    # Set password depending on username
    username = accountInfo[0]
    password = accountInfo[1]

    # find element of sign in button and click it going to sign in page
    signinElem = webDriver.find_element_by_id('header-sign-in')
    signinElem.click()

    # find element of username field and fill in username
    usernameElem = webDriver.find_element_by_id('user_name')
    usernameElem.send_keys(username)

    # find element of password field and fill in password
    passwordElem = webDriver.find_element_by_id('password')
    passwordElem.send_keys(password)

    # click sign in button
    signinElem = webDriver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div/form/input[3]')
    signinElem.click()


def goToOfferedLots(webDriver, page=1):
    if page == 1:
        webDriver.get('https://www.catawiki.com/en/seller/offered-lots')
    elif page > 1:
        webDriver.get(f'https://www.catawiki.com/en/seller/offered-lots/?page={page}')


def go_sold_lots(webDriver, page=1):
    if page == 1:
        webDriver.get('https://www.catawiki.com/en/fulfilment/seller/orders?archived=false&page=1&per_page=25')
    if page > 0:
        webDriver.get(f'https://www.catawiki.com/en/fulfilment/seller/orders?archived=false&page={page}&per_page=25')



def add_nums_titles(webDriver, info_dictionary):
    """Intended for use when on a 'Sold Lots' page. Passed a dictionary the function will add a new dictionary for each
     order on the page. The parent key of this dictionary will be the order number and the dictionary will contain one
     key 'Title text' which contains the title of the catawiki lot."""
    lotElems = webDriver.find_elements(By.CLASS_NAME, 'fu-lot-link')
    country_elems = webDriver.find_elements(By.XPATH, '//tr[@class="fu-seller-order-list-table__row"]/td[6]/div[2]')
    for i, elem in enumerate(lotElems):
        # Links to the order page are in the href attribute. Order numbers need to be extracted from this string.
        elemOrderLink = (elem.get_attribute('href'))
        elemOrderNum = int(''.join(filter(str.isdigit, elemOrderLink)))

        # This is the title of each lot corresponding to the order number
        elemTitleText = elem.text

        #This is the country ordered from
        country = country_elems[i].text

        # Add order number as key to the order information dictionary, and the other information as keys to that dictionary
        info_dictionary[elemOrderNum] = {"Title text": elemTitleText, "Country": country}

