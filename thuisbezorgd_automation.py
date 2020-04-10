from selenium.webdriver.common.keys import Keys
import time


def thuisbezorgd(address, driver):

    website = "https://www.thuisbezorgd.nl/en/"
    driver.get(website)

    # click the search bar in order to get rid of any autofilled address
    search_bar = driver.find_element_by_id("imysearchstring")
    search_bar.click()

    # insert the address
    search_bar.send_keys(address)

    # hit the enter key
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)

    # click away the "ok" button for cookies
    time.sleep(2)
    cookies = "/html/body/div[5]/section/article/button"
    driver.find_element_by_xpath(cookies).click()

    # maximize the window
    time.sleep(2)
    driver.maximize_window()

    # load the information of restaurants
    time.sleep(2)
    plain_text = driver.page_source

    return plain_text