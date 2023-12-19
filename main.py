import os
import time

import keyboard
from thuisbezorgd_db import restaurants
from thuisbezorgd_automation import initiate_driver, click, scroll
from sqlalchemy import create_engine
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    db = "thuisbezorgd.db"
    if os.path.isfile(db):
        os.remove(db)

    engine = create_engine("sqlite:///thuisbezorgd.db")
    NKI = "Plesmanlaan 121, 1066 CX Amsterdam"
    driver = initiate_driver(address=NKI)

    favorites, clicked = [], ""
    while True:
        try:
            option = input("Enter a cuisine, 'All', 'Show more', or 'Exit': ").capitalize()

            if option == "Exit":
                driver.quit()
                break
            elif option == "All":
                restaurants(cuisine=option, driver=driver, engine=engine)
                driver.quit()
                break
            else:
                if option in favorites:
                    print(f"You already hit {option}! Try something else!")
                    continue
                elif option != "Show more":
                    if clicked:
                        click(
                            driver,
                            options=By.XPATH,
                            field_name=f"//div[@class='_3wa4B' and text()='{clicked}']",
                        )
                        clicked = ""
                    click(
                        driver,
                        options=By.XPATH,
                        field_name=f"//div[@class='_3wa4B' and text()='{option}']",
                    )
                    clicked = option
                    restaurants(cuisine=option, driver=driver, engine=engine)
                    favorites.append(option)
                    continue
                else:
                    if clicked:
                        click(
                            driver,
                            options=By.XPATH,
                            field_name=f"//div[@class='_3wa4B' and text()='{clicked}']",
                        )
                        clicked = ""
                    click(
                        driver,
                        options=By.XPATH,
                        field_name=f"//span[@class='ygmw2' and text()='{option}']",
                    )
                    print(
                        "Press up or down arrow key to scroll, 'x' to close the pop-up, or hit 'ENTER' to type a "
                        "cuisine "
                    )
                    while True:
                        if keyboard.is_pressed("up"):
                            scroll(driver, direction="up")
                        elif keyboard.is_pressed("down"):
                            scroll(driver)
                        elif keyboard.is_pressed("x"):
                            click(
                                driver,
                                options=By.XPATH,
                                field_name="//span[@data-qa='cuisine-filter-modal-header-action-close']",
                            )
                            break
                        elif keyboard.is_pressed("enter"):
                            while True:
                                try:
                                    time.sleep(1)
                                    option = input("Enter a cuisine: ").capitalize()
                                    if option in favorites:
                                        print(
                                            f"You already hit {option}! Try something else!"
                                        )
                                        continue
                                    else:
                                        click(
                                            driver,
                                            options=By.XPATH,
                                            field_name=f"//div[@class='_3wa4B' and starts-with(text(), '{option}')]",
                                        )
                                        clicked = option
                                        restaurants(
                                            cuisine=option, driver=driver, engine=engine
                                        )
                                        favorites.append(option)
                                        break
                                except Exception:
                                    print("\033[91mWrong input! Try again!!\033[0m")
                            break
        except Exception:
            print("\033[91mWrong input! Try again!!\033[0m")
