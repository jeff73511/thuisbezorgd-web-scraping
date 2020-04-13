import os
from selenium import webdriver
from thuisbezorgd_db import restaurants
from webdriver_manager.chrome import ChromeDriverManager
from thuisbezorgd_automation import thuisbezorgd, click_option, scroll, click_x
from termcolor import colored


db = "thuisbezorgd.db"
if os.path.isfile(db):
    os.remove(db)

driver = webdriver.Chrome(ChromeDriverManager().install())
NKI = "Plesmanlaan 121, 1066 CX Amsterdam"
plain_text = thuisbezorgd(NKI, driver)

favorite = []
while True:

    try:
        option = input(
            "Enter a cuisine (or 'All'), 'Show more', or 'exit': "
        )  # exit or others (all, cuisine, show more) 2

        if option == "exit":  # exit
            driver.quit()
            break

        else:
            if option in favorite:  # check if already selected a cuisine
                print(f"You already hit {option}! Try something else!")
                continue

            else:
                click_option(driver, option)  # show more or others (all, cuisine) 2

            if option != "Show more":  # all or cuisine
                restaurants(cuisine=option, html=plain_text)
                favorite.append(option)
                continue

            else:  # in show more: x, scroll(up/down), or  cuisine 3
                while True:
                    try:
                        option_show_more = input(
                            "Enter a cuisine, 'scroll (up/down)', or 'x': "
                        )

                        if option_show_more == "x":  # x
                            click_x(driver)
                            break

                        elif option_show_more in ("scroll up", "scroll down"):  # scroll
                            scroll(driver, option_show_more)

                        else:  # cuisine
                            if option_show_more in favorite:  # check if already selected a cuisine
                                print(f"You already hit {option_show_more}! Try something else!")
                                continue

                            else:
                                click_option(driver, option, option_show_more)
                                restaurants(cuisine=option_show_more, html=plain_text)
                                favorite.append(option_show_more)
                                break

                    except:
                        print(colored("Incorrect input! Try again!", "red"))

    except:  # others cause error
        print(colored("Incorrect input! Try again!", "red"))