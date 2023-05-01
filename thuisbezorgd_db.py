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

    html = driver.execute_script(
        "return document.getElementsByTagName('html')[0].innerHTML"
    )
    soups = BeautifulSoup(html, "html.parser")
    soups = soups.find("section", {"data-qa": f"restaurant-list-{status}-section"})
    soups = soups.findAll("li", {"class": "_2ro375"})

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
        "names": names,
        "ratings": ratings,
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

    status = ["open", "pre-order", "closed"]
    df = DataFrame()
    for s in status:
        df = concat(
            [df, restaurants_status(cuisine=cuisine, status=s, driver=driver)],
            ignore_index=True,
        )

    df.to_sql(f"{cuisine}", con=engine, if_exists="replace", index=False)
