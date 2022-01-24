import account_info
import cw_ctrls
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import logging
import re
import time

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

# Set up browser and log into catawiki
target_value = 24776079
driver = webdriver.Firefox()
driver.get('https://catawiki.com')
cw_ctrls.agreeCookies(webDriver=driver)
cw_ctrls.signIn(webDriver=driver, accountInfo=account_info.eva)

# Create empty dictionary  which will contain all further order information. The dictionary will be filled with
# dictionaries of information about each order with the order number acting as the key for each dictionary
order_info_dict = {}

# Starting at page 1 the while loop will go to the sold lots page and extract the order numbers from the page. These
# will be stored as keys in order_info_dict with the values being new dictionaries containing the title text and the
# country.  After all orders have been extracted from the loop the lowest ordder number will be assigned to lowest_number
# and if this is lower than target_value the loop will stop. Other wise it will continue to the next page.
lowest_number = 9999999999
page_number = 1
while lowest_number > target_value:
    cw_ctrls.go_sold_lots(webDriver=driver, page=page_number)
    time.sleep(5)
    #Add the order numbers and lot titles as series of nested dictionaries ie {ordernum:{'title': actualtitle}}
    cw_ctrls.add_nums_titles(webDriver=driver, info_dictionary=order_info_dict)
    # Assign the lowest order number value to LowestNumber so loop stops if needed
    lowest_number = min(order_info_dict.keys())
    page_number += 1

# There are likely to be a number of order numbers lower than the target order_info_dict. Now we loop through the keys
# and delete those with a lower value in order to make sure we only have the desired orders in the dictionary
keys_to_check = list(order_info_dict)
for order_num in keys_to_check:
    print(len(order_info_dict))
    if order_num < target_value:
        del order_info_dict[order_num]
print(len(order_info_dict), order_info_dict)

# Loop through the order numbers in order_info_dict and add order information to the corresponding dictionary
order_num_list = list(order_info_dict.keys())
for order_number in order_num_list:
    driver.get(f"https://www.catawiki.com/en/fulfilment/seller/orders/{order_number}")
    time.sleep(3)
    # Order Status
    order_info_dict[order_number]['Order Status'] = driver.find_element(by=By.XPATH, value='//p[@data-testid="order-'
                                                                                        'details-status"]').text
    # Date paid
    order_info_dict[order_number]["Date Paid"] = driver.find_element(by=By.XPATH, value='//td[@class="u-p-r'
                                                                                     '-xs u-no-wrap"]').text
    # Shipment Date
    try:
        order_info_dict[order_number]["Date Shipped"] = driver.find_element(by=By.XPATH, value='//table[@data-testid="orde'
                                                                                            'r-events"]/tbody/tr[2]/td'
                                                                                            '[1]').text
    except NoSuchElementException:
        order_info_dict[order_number]["Date Shipped"] = "Not yet shipped"

    # Reference Tag
    order_info_dict[order_number]["Reference Tag"] = driver.find_element(by=By.XPATH, value='//div[@class="fu-lot-label"]/'
                                                                                         'div[@class="u-font-size-xs-ti'
                                                                                         'ght u-color-secondary u-word-'
                                                                                         'break-all"]').text
    # Item Price
    order_info_dict[order_number]["Item Price"] = driver.find_element(by=By.XPATH, value='//dd[@data-testid="order-summary'
                                                                                      '-items"]').text

    # Shipping Price
    order_info_dict[order_number]["Shipping Price"] = driver.find_element(by=By.XPATH, value='//dd[@data-testid="order-su'
                                                                                          'mmary-items"]').text

    # Go to auction page
    auction_link = driver.find_element(by=By.XPATH, value='//a[@class="c-link main"]').get_attribute('href')
    driver.get(auction_link)
    time.sleep(1)

    # Auction name
    auction_name = driver.find_element(by=By.XPATH, value='//a[@class="c-breadcrumbs__item c-breadcrumbs__item'
                                                          '--last"]').text
    order_info_dict[order_number]["Auction Name"] = auction_name

    # Auction end date
    auction_end = driver.find_element(by=By.XPATH, value='//th[@class="u-color-secondary be-bid-history__unit-col '
                                                         'be-bid-history__time"]/span[1]')
    order_info_dict[order_number]["Auction End Date"] = auction_end.text

    print(order_info_dict)















