from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
items_id = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60 * 5

should_continue = True
while should_continue:
    cookie.click()
    if time.time() > timeout:
        items_price = []
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        for price in all_prices:
            element_price = price.text
            if element_price != "":
                price = int(element_price.split("-")[1].replace(",", "").strip())
                items_price.append(price)


        upgrades = {}
        for n in range(0, len(items_price)):
            upgrades[items_id[n]] = items_price[n]

        available_upgrade = {}

        money = int(driver.find_element(By.ID, "money").text.replace(",", ""))
        # if "," in money:
        #     money = int(money.replace(",", ""))
        print(f"money= {money}")

        for id, price in upgrades.items():
            print(f"money ={money}")
            print(f"price = {price}")
            if money > price:
                available_upgrade[price] = id
            print(available_upgrade)

        max_upgrade = max(available_upgrade)
        to_purchase_id = available_upgrade[max_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()
        timeout = time.time() + 5

    if time.time() > five_min:
        should_continue = False
        cookie_second = driver.find_element(By.ID, "cps").text
        print(cookie_second)
        driver.quit()
