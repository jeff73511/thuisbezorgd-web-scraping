import time

from bs4 import BeautifulSoup
from pandas import DataFrame, concat
from undetected_chromedriver import Chrome
from sqlalchemy import Engine


def restaurants_status(cuisine: str, status: str, driver: Chrome) -> DataFrame:
    """Gets all the information of a cuisine according to the
    status ("open", "preorder", or "closed") of restaurants.

    :param cuisine: Cuisine shown on the site.
    :param status: Status of restaurants: "open", "pre-order", or "closed".
    :param driver: ChromeDriver.
    :return: A dataframe that stores information of restaurants under a certain status.
    """

    html = driver.page_source
    soups = BeautifulSoup(html, "html.parser")
    soups = soups.find("section", {"data-qa": f"restaurant-list-{status}-section"})

    try:
        soups = soups.findAll("li", {"class": "_2ro375"})
    except AttributeError as e:
        if str(e) == "'NoneType' object has no attribute 'findAll'":
            return DataFrame()
        else:
            raise

    names, ratings, deliver_time, deliver_cost, min_order = [], [], [], [], []
    for soup in soups:
        name = soup.find("h3", {"data-qa": "restaurant-info-name"}).text
        names.append(name)

        try:
            rating = soup.find("b", {"data-qa": "restaurant-rating-score"}).text
        except AttributeError:
            rating = "No rating available"
        ratings.append(rating)

        if status != "closed":
            eta = soup.find("div", {"data-qa": "shipping-time-indicator-content"}).text
            deliver_time.append(eta)

            cost = soup.find(
                "div", {"data-qa": "delivery-costs-indicator-content"}
            ).text
            cost = cost.replace("\xa0", " ")
            deliver_cost.append(cost)

            order = soup.find("div", {"data-qa": "mov-indicator-content"}).text
            min_order.append(order)

        else:
            deliver_time.append("Closed for delivery")
            deliver_cost.append("Closed for delivery")
            min_order.append("Closed for delivery")

    result = {
        "cuisine": cuisine,
        "name": names,
        "rating": ratings,
        "deliver_time": deliver_time,
        "deliver_cost": deliver_cost,
        "min_order": min_order,
        "status": status,
    }

    return DataFrame(result)


def restaurants(cuisine: str, driver: Chrome, engine: Engine) -> None:
    """Stores all the information of restaurants of a cuisine
    in a database.

    :param cuisine: Cuisine shown on the site.
    :param driver: ChromeDriver.
    :param engine: A central object that provides connectivity to a database.
    """

    # Scroll down to the bottom of the page
    # Set the amount of pixels to scroll by in each step
    scroll_step = 250
    scroll_from = 0

    while True:
        new_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(scroll_from, new_height, scroll_step):
            driver.execute_script(f"window.scrollTo({scroll_from}, {i});")
            time.sleep(0.1)

        old_height = new_height
        scroll_from = old_height
        new_page_height = driver.execute_script("return document.body.scrollHeight")
        if old_height == new_page_height:
            break

    status = ["open", "pre-order", "closed"]
    df = concat(
        [restaurants_status(cuisine, s, driver) for s in status], ignore_index=True
    )

    if df.empty:
        raise ValueError("Something went wrong with the restaurant list")

    df.to_sql(f"{cuisine}", con=engine, if_exists="replace", index=False)
