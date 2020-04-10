import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from thuisbezorgd_db import restaurants
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from thuisbezorgd_automation import thuisbezorgd


db = "thuisbezorgd.db"
if os.path.isfile(db):
    os.remove(db)

driver = webdriver.Chrome(ChromeDriverManager().install())
NKI = "Plesmanlaan 121, 1066 CX Amsterdam"
plain_text = thuisbezorgd(NKI, driver)

record = []
while True:

    try:
        cuisine = input(
            "Choose a cuisine style or, enter 'All', 'Show more', or 'exit':"
        )

        if cuisine not in ["Show more", "exit"]:
            if cuisine in record:
                print(f"You already hit {cuisine}! Try something else!")
                continue
            else:
                wait(driver, 2).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//span[@class='swiper-slide__context'][text()='{cuisine}']",
                        )
                    )
                ).click()
                restaurants(cuisine=cuisine, html=plain_text)
                record.append(cuisine)

        elif cuisine == "Show more":
            wait(driver, 2).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//span[@class='swiper-slide__context'][text()='{cuisine}']",
                    )
                )
            ).click()
            pop_up = driver.find_element_by_xpath("/html/body/div[8]/div/div[2]")
            driver.execute_script(f"arguments[0].scrollTop = 0", pop_up)

            i = 0
            while True:
                i = i + 1
                height = 200 * ((i % 3))
                scroll = "scroll down"
                if height == 0:
                    scroll = "scroll up"

                try:
                    cuisine = input(
                        f"Choose a cuisine style, or enter '{scroll}' or 'x':"
                    )
                    if cuisine == "x":
                        driver.find_element_by_xpath(
                            "/html/body/div[8]/div/button"
                        ).click()
                        break

                    elif cuisine == scroll:
                        driver.execute_script(
                            f"arguments[0].scrollTop = {height}", pop_up
                        )
                        continue

                    else:
                        if cuisine in record:
                            print(f"You already hit {cuisine}! Try something else!")
                            i = i - 1
                            continue
                        wait(driver, 2).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    f"//span[@class='tv-chip__inner-content'][text()='{cuisine}']",
                                )
                            )
                        ).click()
                        restaurants(cuisine=cuisine, html=plain_text)
                        record.append(cuisine)
                        break
                except:
                    i = i - 1
                    print("Incorrect input! Try again!")

        else:
            driver.quit()
            break

    except:
        print("Incorrect input! Try again!")