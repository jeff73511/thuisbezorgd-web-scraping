import pytest
from sqlalchemy import create_engine
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


@pytest.fixture()
def test_engine(tmpdir):
    """"""
    return create_engine(f"sqlite:///{tmpdir}/thuisbezorgd.db")


@pytest.fixture()
def driver():
    """"""
    driver = webdriver.Chrome(ChromeDriverManager().install())

    website = "https://www.thuisbezorgd.nl/en/"
    driver.get(website)

    # click the search bar in order to get rid of any autofilled address
    search_bar = driver.find_element_by_id("imysearchstring")
    search_bar.click()

    # insert the address
    NKI = "Plesmanlaan 121, 1066 CX Amsterdam"
    search_bar.send_keys(NKI)

    # hit the enter key
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)

    # click away "ok" for cookies
    time.sleep(2)
    cookies = "/html/body/div[5]/section/article/button"
    driver.find_element_by_xpath(cookies).click()

    return driver


@pytest.fixture()
def cuisines():
    """"""
    return ["Sushi", "Chinese", "Burgers", "Italian style pizza"]