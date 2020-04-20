import sys

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import time
from termcolor import colored


def restaurants_status(cuisine, status, html):
    """ This function gets all the information of a cuisine according to the
    status ("open", "preorder", or "closed") of restaurants.

    :param cuisine: str, cuisine shown on the site.
    :param status: str, status of retaurants: "open", "preorder", or "closed".
    :param html: str, source of current page.
    :return: DataFrame, dataframe that stores information of restaurants under a certain status.
    """

    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find("div", {"class": f"js-restaurant-list-{status}"})

    kitchens = soup.findAll("div", {"class": "kitchens"})
    kitchens = [kitchen.text.strip() for kitchen in kitchens]
    filter = np.array([cuisine in style for style in kitchens])

    names = soup.findAll("a", {"class": "restaurantname"})
    names = np.array([name.text.strip() for name in names])[filter]

    ratings = soup.findAll("span", {"class": "rating-total"})
    ratings = np.array([rating.text.strip("(").strip(")") for rating in ratings])[
        filter
    ]

    deliver_time = soup.findAll(
        "div", {"class": "avgdeliverytime avgdeliverytimefull open"}
    )
    if len(deliver_time) == 0 or status == "closed":
        deliver_time = "not available"
    else:
        deliver_time = np.array([time.text for time in deliver_time])[filter]

    deliver_cost = soup.findAll("div", {"class": "delivery-cost js-delivery-cost"})
    if len(deliver_cost) == 0 or status == "closed":
        deliver_cost = "not available"
    else:
        deliver_cost = np.array([cost.text for cost in deliver_cost])[filter]

    min_order = soup.findAll("div", {"class": "min-order"})
    if len(min_order) == 0 or status == "closed":
        min_order = "not available"
    else:
        min_order = np.array([order.text for order in min_order])[filter]

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

    status = ["open", "preorder", "closed"]
    data = pd.DataFrame()
    for s in status:
        data = data.append(
            restaurants_status(cuisine=cuisine, status=s, html=html), ignore_index=True
        )

    engine = create_engine("sqlite:///thuisbezorgd.db")
    data.to_sql(f"{cuisine}", con=engine, if_exists="replace", index=False)
