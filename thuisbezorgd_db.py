import sys

from bs4 import BeautifulSoup
from itertools import compress
import pandas as pd
from sqlalchemy import create_engine
import time
from termcolor import colored


def restaurants_status(cuisine, status, html):
    """ This function gets all the information of a cuisine according to the
    status ("open", "preorder", or "closed") of restaurants.

    :param cuisine: str, cuisine shown on the site.
    :param status: str, status of retaurants: "open", "pre-order", or "closed".
    :param html: str, source of current page.
    :return: DataFrame, dataframe that stores information of restaurants under a certain status.
    """

    soups = BeautifulSoup(html, "html.parser")
    soups = soups.findAll(
        "div", {"class": f"js-restaurant restaurant restaurant__{status}"}
    )

    kitchens, names, ratings, deliver_time, deliver_cost, min_order = [], [], [], [], [], []
    for soup in soups:
        kitchen = soup.find("div", {"class": "kitchens"}).text.strip()
        kitchens.append(kitchen)

        name = soup.find("a", {"class": "restaurantname"}).text.strip()
        names.append(name)

        rating = soup.find("span", {"class": "rating-total"}).text.strip("(").strip(")")
        ratings.append(rating)

        if status != "closed":
            time = soup.find(
                "div", {"class": "avgdeliverytime avgdeliverytimefull open"}
            ).text.strip()
            deliver_time.append(time)

            cost = soup.find(
                "div", {"class": "delivery-cost js-delivery-cost"}
            ).text.strip()
            deliver_cost.append(cost)

            order = soup.find("div", {"class": "min-order"}).text.strip()
            min_order.append(order)

        else:
            deliver_time.append("Closed for delivery")
            deliver_cost.append("Closed for delivery")
            min_order.append("Closed for delivery")

    if cuisine!= "All":
        get = [cuisine in style for style in kitchens]
        names = list(compress(names, get))
        ratings = list(compress(ratings, get))
        deliver_time = list(compress(deliver_time, get))
        deliver_cost = list(compress(deliver_cost, get))
        min_order = list(compress(min_order, get))

    result = {
        "names": names,
        "ratings": ratings,
        "deliver_time": deliver_time,
        "deliver_cost": deliver_cost,
        "min_order": min_order,
        "status": status,
    }

    return pd.DataFrame(result)


def restaurants(cuisine, html):
    """ This function stores all the information of restaurants of a cuisine
    in a data base.

    :param cuisine: str, cuisine shown on the site.
    :param html: str, source of current page.
    """

    message = f"Now scraping {cuisine}... \n"
    for wrd in message:
        print(colored(wrd, "green"), end="")
        sys.stdout.flush()
        time.sleep(0.1)

    status = ["open", "pre-order", "closed"]
    data = pd.DataFrame()
    for s in status:
        data = data.append(
            restaurants_status(cuisine=cuisine, status=s, html=html), ignore_index=True
        )

    engine = create_engine("sqlite:///thuisbezorgd.db")
    data.to_sql(f"{cuisine}", con=engine, if_exists="replace", index=False)
