import os
from thuisbezorgd_db import restaurants
from thuisbezorgd_automation import initiate_driver, click_option, scroll, click_x
from termcolor import colored
from sqlalchemy import create_engine


if __name__ == "__main__":
    db = "thuisbezorgd.db"
    if os.path.isfile(db):
        os.remove(db)

    engine = create_engine("sqlite:///thuisbezorgd.db")
    NKI = "Plesmanlaan 121, 1066 CX Amsterdam"
    driver = initiate_driver(address=NKI)

    favorite = []
    while True:
        try:
            option = input("Enter a cuisine (or 'All'), 'Show more', or 'Exit': ")
            option = option.capitalize()

            if option == "Exit":
                driver.quit()
                break
            else:
                if option in favorite:
                    print(f"You already hit {option}! Try something else!")
                    continue

                click_option(driver, option)

                if option != "Show more":
                    restaurants(cuisine=option, driver=driver, engine=engine)
                    favorite.append(option)
                    continue
                else:
                    while True:
                        try:
                            option_show_more = input(
                                "Enter a cuisine, 'scroll (up/down)', or 'x': "
                            )

                            if option_show_more == "x":
                                click_x(driver)
                                break
                            elif option_show_more in ("scroll up", "scroll down"):
                                scroll(driver, option_show_more)
                            else:
                                if option_show_more in favorite:
                                    print(
                                        f"You already hit {option_show_more}! Try something else!"
                                    )
                                    continue
                                click_option(driver, option, option_show_more)
                                restaurants(cuisine=option, driver=driver, engine=engine)
                                favorite.append(option_show_more)
                                break

                        except Exception:
                            print(colored("Incorrect input! Try again!", "red"))

        except:
            print(colored("Incorrect input! Try again!", "red"))