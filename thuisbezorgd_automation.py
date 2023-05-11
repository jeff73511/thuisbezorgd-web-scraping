from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import undetected_chromedriver as uc
from undetected_chromedriver import Chrome


def find_web_element(
    driver,
    options: str,
    field_name: str,
    webdriver_timeout: float = 5,
    poll_frequency: float = 0.05,
) -> WebElement:
    """Find WebElement by a locator.

    :param driver: ChromeDriver.
    :param options: Attribute used to locate element on a web page.
    :param field_name: Value of a web element attribute.
    :param webdriver_timeout: Timeout in second until element exists (default 5).
    :param poll_frequency: How often to check element exists (default 0.05).
    :return: WebElement.
    """

    return WebDriverWait(
        driver,
        timeout=webdriver_timeout,
        poll_frequency=poll_frequency,
    ).until(lambda d: d.find_element(options, field_name))


def initiate_driver(address: str) -> Chrome:
    """This automation function opens the web browser, goes to
    the Thuisbezorgd website, fills in the location address, and
    returns the source of current page.

    :param address: location.
    :return: ChromeDriver.
    """

    options = uc.ChromeOptions()
    options.add_argument("--deny-permission-prompts")
    driver = uc.Chrome(options=options)
    driver.get("https://www.thuisbezorgd.nl/en/")
    driver.fullscreen_window()

    # Click away "ok" for cookies
    element = find_web_element(
        driver=driver,
        options=By.CSS_SELECTOR,
        field_name="._908LZ._1bx49._20B3B._4R7G3.YG2eu._2JFg2",
    )
    element.click()

    # Insert the address
    element = find_web_element(driver=driver, options=By.NAME, field_name="searchText")
    element.send_keys(address)

    # Click on suggestion
    element = find_web_element(
        driver=driver, options=By.CSS_SELECTOR, field_name="._2GljJ._2PIGg"
    )
    element.click()

    return driver


def click(driver: Chrome, options: str, field_name: str) -> None:
    """This automation function clicks one of cuisines on the website or
    the option, "show more".

    :param driver: ChromeDriver.
    :param options: Attribute used to locate element on a web page.
    :param field_name: Value of a web element attribute.
    """

    find_web_element(driver, options=options, field_name=field_name).click()


def scroll(driver: Chrome, amount: float = 250, direction: str = "down") -> None:
    """Scrolls up or down the pop-up screen from the "Show more" option.

    :param driver: ChromeDriver.
    :param amount: Amount of pixels to move.
    :param direction: Sroll "up" or "down" (default down).
    """

    pop_up = find_web_element(
        driver, options=By.XPATH, field_name="//div[@data-qa='modal-scroll-content']"
    )
    driver.execute_script(
        f"arguments[0].scrollTop += {amount if direction == 'down' else -amount}",
        pop_up,
    )
