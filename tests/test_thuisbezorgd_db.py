from thuisbezorgd_db import restaurants
from thuisbezorgd_automation import initiate_driver, click
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By


def test_restaurants(cuisines, test_engine, address):
    """"""
    driver = initiate_driver(address=address)

    clicked = ""
    for c in cuisines:
        if clicked:
            click(
                driver,
                options=By.XPATH,
                field_name=f"//div[@class='_3wa4B' and text()='{clicked}']",
            )
        click(
            driver,
            options=By.XPATH,
            field_name=f"//div[@class='_3wa4B' and text()='{c}']",
        )
        clicked = c
        restaurants(cuisine=c, driver=driver, engine=test_engine)
        soups = BeautifulSoup(driver.page_source, "html.parser")
        amount = soups.find("h3", {"data-qa": "sidebar-result-counter"}).text

        assert len(pd.read_sql_table(c, con=test_engine)) == int(
            amount[: amount.index(" ")]
        ), f"Error occurred for {c}"
