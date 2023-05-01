from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import time
import undetected_chromedriver as uc


def find_web_element(
        driver,
        options: str,
        field_name: str,
        webdriver_timeout: float = 5,
        poll_frequency: float = 0.05,
) -> WebElement:
    """Find WebElement by a locator.
    Args:
        options: Attribute used to locate element on a web page.
        field_name: Value of a web element attribute.
    Returns:
        A Selenuim WebElement.
    """

    return WebDriverWait(
        driver,
        timeout=webdriver_timeout,
        poll_frequency=poll_frequency,
    ).until(lambda d: d.find_element(options, field_name))


def initiate_driver(address):
    """This automation function opens the web browser, goes to
    the thuisbezorgd website, fills in the location address, and
    returns the source of current page.

    :param address: str, location.
    :return: str, source of current page.
    """

    options = uc.ChromeOptions()
    options.add_argument('--deny-permission-prompts')
    driver = uc.Chrome(options=options)
    driver.get("https://www.thuisbezorgd.nl/en/")

    # Click away "ok" for cookies
    element = find_web_element(driver=driver, options=By.CSS_SELECTOR,
                               field_name="._908LZ._1bx49._20B3B._4R7G3.YG2eu._2JFg2")
    element.click()

    # Insert the address
    element = find_web_element(driver=driver, options=By.NAME, field_name="searchText")
    element.send_keys(address)

    # Click on suggestion
    element = find_web_element(driver=driver, options=By.CSS_SELECTOR, field_name="._2GljJ._2PIGg")
    element.click()

    # # load the information of restaurants
    # time.sleep(2)
    # plain_text = driver.page_source

    return driver


def click_option(driver, option=None, option_show_more=None):
    """This automation function clicks one of cuisines on the website or
    the option, "show more".

    :param driver: WebDriver, web driver to drive the browser.
    :param option: str, cuisine shown on the site or "show more".
    :param option_show_more: str, cuisine shown on the site in the pop up screen.
    """

    find_web_element(driver, options=By.XPATH, field_name=f"//div[@class='_3wa4B' and text()='{option}']").click()


def scroll(driver, option_show_more):
    """This automation function scrolls up or down the pop up screen
    from the "show more" option.

    :param driver: WebDriver, web driver to drive the browser.
    :param option_show_more: str, "sroll up" or "scroll down".
    """

    time.sleep(2)
    scroll_option = {"scroll up": "0", "scroll down": "arguments[0].scrollHeight"}

    pop_up = wait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='tv-popup__content']"))
    )
    driver.execute_script(
        f"arguments[0].scrollTop = {scroll_option[option_show_more]}", pop_up
    )


def click_x(driver):
    """This automation function closes the pop up screen from the
    "show more" option.

    :param driver: WebDriver, web driver to drive the browser.
    """

    time.sleep(2)
    wait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='tv-icon']"))
    ).click()
