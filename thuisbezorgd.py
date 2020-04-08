import sys
import time
import json
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from thuisbezorgd_helper import restaurants



db = "thuisbezorgd.db"
if os.path.isfile(db):
    os.remove(db)

chrome_path = r"/Users/Jeff1/PycharmProjects/NewProject/web_scraping/chromedriver"
website = "https://www.thuisbezorgd.nl/en/"
driver = webdriver.Chrome(chrome_path)
driver.get(website)

search_bar = driver.find_element_by_id("imysearchstring")
search_bar.click()

NKI_address = "Plesmanlaan 121, 1066 CX Amsterdam"
search_bar.send_keys(NKI_address)

time.sleep(2)
search_bar.send_keys(Keys.ENTER)

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
