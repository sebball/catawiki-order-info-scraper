import accountInfo
import cwCtrls
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import logging
import re
import time

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')

# Set up browser and log into catawiki
targetValue = 24776079
driver = webdriver.Firefox()
driver.get('https://catawiki.com')
cwCtrls.agreeCookies(webDriver=driver)
cwCtrls.signIn(webDriver=driver, accountInfo=accountInfo.eva)

# Create empty dictionary  which will contain all further order information. The dictionary will be filled with
# dictionaries of information about each order with the order number acting as the key for each dictionary
orderInfoDict = {}

# Starting at page 1 the while loop will go to the sold lots page and extract the order numbers from the page. These
# will be stored as keys in order_info_dict with the values being new dictionaries containing the title text and the
# country.  After all orders have been extracted from the loop the lowest ordder number will be assigned to lowestNumber
# and if this is lower than targetValue the loop will stop. Other wise it will continue to the next page.
lowestNumber = 9999999999
pageNumber = 1
while lowestNumber > targetValue:
    cwCtrls.goToSoldLots(webDriver=driver, page=pageNumber)
    time.sleep(5)
    #Add the order numbers and lot titles as series of nested dictionaries ie {ordernum:{'title': actualtitle}}
    cwCtrls.addNumsTitles(webDriver=driver, info_dictionary=orderInfoDict)
    # Assign the lowest order number value to LowestNumber so loop stops if needed
    lowestNumber = min(orderInfoDict.keys())
    pageNumber += 1

# There are likely to be a number of order numbers lower than the target orderInfoDict. Now we loop through the keys
# and delete those with a lower value in order to make sure we only have the desired orders in the dictionary
keys_to_check = list(orderInfoDict)
for order_num in keys_to_check:
    print(len(orderInfoDict))
    if order_num < targetValue:
        del orderInfoDict[order_num]
print(len(orderInfoDict), orderInfoDict)

# Loop through the order numbers in orderInfoDict and add order information to the corresponding dictionary
orderNumbers = list(orderInfoDict.keys())
for orderNumber in orderNumbers:
    driver.get(f"https://www.catawiki.com/en/fulfilment/seller/orders/{orderNumber}")
    time.sleep(3)
    # Order Status
    orderInfoDict[orderNumber]['Order Status'] = driver.find_element(by=By.XPATH, value='//p[@data-testid="order-'
                                                                                        'details-status"]').text
    # Date paid
    orderInfoDict[orderNumber]["Date Paid"] = driver.find_element(by=By.XPATH, value='//td[@class="u-p-r'
                                                                                     '-xs u-no-wrap"]').text
    # Shipment Date
    try:
        orderInfoDict[orderNumber]["Date Shipped"] = driver.find_element(by=By.XPATH, value='//table[@data-testid="orde'
                                                                                            'r-events"]/tbody/tr[2]/td'
                                                                                            '[1]').text
    except NoSuchElementException:
        orderInfoDict[orderNumber]["Date Shipped"] = "Not yet shipped"

    # Reference Tag
    orderInfoDict[orderNumber]["Reference Tag"] = driver.find_element(by=By.XPATH, value='//div[@class="fu-lot-label"]/'
                                                                                         'div[@class="u-font-size-xs-ti'
                                                                                         'ght u-color-secondary u-word-'
                                                                                         'break-all"]').text
    # Item Price
    orderInfoDict[orderNumber]["Item Price"] = driver.find_element(by=By.XPATH, value='//dd[@data-testid="order-summary'
                                                                                      '-items"]').text

    # Shipping Price
    orderInfoDict[orderNumber]["Shipping Price"] = driver.find_element(by=By.XPATH, value='//dd[@data-testid="order-su'
                                                                                          'mmary-items"]').text

    # Go to auction page
    auction_link = driver.find_element(by=By.XPATH, value='//a[@class="c-link main"]').get_attribute('href')
    driver.get(auction_link)
    time.sleep(1)

    # Auction name
    auction_name = driver.find_element(by=By.XPATH, value='//a[@class="c-breadcrumbs__item c-breadcrumbs__item'
                                                          '--last"]').text
    orderInfoDict[orderNumber]["Auction Name"] = auction_name

    # Auction end date
    auction_end = driver.find_element(by=By.XPATH, value='//th[@class="u-color-secondary be-bid-history__unit-col '
                                                         'be-bid-history__time"]/span[1]')
    orderInfoDict[orderNumber]["Auction End Date"] = auction_end.text

    print(orderInfoDict)















