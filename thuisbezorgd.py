import sys
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from thuisbezorgd_helper import restaurants
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait

db = "thuisbezorgd.db"
if os.path.isfile(db):
    os.remove(db)


website = "https://www.thuisbezorgd.nl/en/"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(website)

search_bar = driver.find_element_by_id("imysearchstring")
search_bar.click()

NKI_address = "Plesmanlaan 121, 1066 CX Amsterdam"
search_bar.send_keys(NKI_address)

time.sleep(2)
search_bar.send_keys(Keys.ENTER)

time.sleep(2)
driver.find_element_by_xpath("/html/body/div[5]/section/article/button").click()

wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Show more']"))).click()
wait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Dutch']"))).click()


driver.find_element_by_xpath("/html/body/div[8]/div/button").click()


# (1) choose a cuisine

# (2) if no
pop_up_content = driver.find_element_by_xpath("/html/body/div[8]/div/div[2]")
driver.execute_script("arguments[0].scrollTop = 200", pop_up_content)



# # (3) if no
# driver.execute_script("arguments[0].scrollTop = 400", scroll_down)

# (4) if no, close the windown
driver.find_element_by_xpath("/html/body/div[8]/div/button").click()


time.sleep(5)
plain_text = driver.page_source

with open("cuisine_dic.json") as json_file:
    cuisine_dic = json.load(json_file)

while True:
    cuisine = input("Enter a cuisine style (or 'last page'/'next page'/'exit'):")
    while True:
        try:
            if cuisine == "next page":
                driver.find_element_by_xpath(
                    "//*[@id='kitchen-types']/div/div/div[3]"
                ).click()

            elif cuisine == "last page":
                driver.find_element_by_xpath(
                    "//*[@id='kitchen-types']/div/div/div[1]"
                ).click()

            elif cuisine == "exit":
                break

            else:
                driver.find_element_by_xpath(
                    f"//*[@id='kitchen-types']/div/div/div[2]/div/a[{cuisine_dic[cuisine]}]"
                ).click()

                restaurants(cuisine=cuisine, html=plain_text)

            break

        except:
            print("Input is not correct! Try again.")
            cuisine = input(
                "Enter a cuisine style (or 'last page'/'next page'/'exit'):"
            )

    if cuisine == "exit":
        driver.quit()
        sys.exit()
