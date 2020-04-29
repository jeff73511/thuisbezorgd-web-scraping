from thuisbezorgd_db import restaurants
from thuisbezorgd_automation import click_option
from bs4 import BeautifulSoup
import pandas as pd
import time

def test_restaurants(cuisines, driver, test_engine):
    """"""
    html = driver.page_source
    for c in cuisines:
        click_option(driver, option=c)
        restaurants(cuisine=c, html=html, engine=test_engine)

        time.sleep(2)
        soups = BeautifulSoup(driver.page_source, "html.parser")
        restaurant_amount = soups.find("span", {"class": "restaurant-amount"}).text

        assert len(pd.read_sql_table(c, con=test_engine)) == int(restaurant_amount), f"Error occured for {c}"
