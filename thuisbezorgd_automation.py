from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
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

    # click away "ok" for cookies
    time.sleep(2)
    cookies = "/html/body/div[5]/section/article/button"
    driver.find_element_by_xpath(cookies).click()

    # load the information of restaurants
    time.sleep(2)
    plain_text = driver.page_source

    return plain_text


def click_option(driver, option=None, option_show_more=None):

    time.sleep(2)
    dic = {"main": "swiper-slide__context", "pop_up": "tv-chip__inner-content"}

    if option_show_more == None:
        where = dic["main"]
        cuisine = option
    else:
        where = dic["pop_up"]
        cuisine = option_show_more

    wait(driver, 2).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//span[@class='{where}'][text()='{cuisine}']")
        )
    ).click()


def scroll(driver, option_show_more):

    time.sleep(2)
    scroll_option = {"scroll up": "0", "scroll down": "arguments[0].scrollHeight"}

    pop_up = wait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='tv-popup__content']"))
    )
    driver.execute_script(
        f"arguments[0].scrollTop = {scroll_option[option_show_more]}", pop_up
    )


def click_x(driver):

    time.sleep(2)
    wait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='tv-icon']"))
    ).click()
