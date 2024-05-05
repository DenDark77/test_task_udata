import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

URL = 'https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html'

SCROLL_PAUSE_TIME = 2
wait = WebDriverWait(driver, 2)

# last_height = driver.execute_script("return document.body.scrollHeight")
# print(last_height)
driver.get(URL)


dict_items_list = []

def parse():

    items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cmp-category__item")))
    for i in range(0, len([i.text.split('\n') for i in items])):
        item = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cmp-category__item")))
        item[i].click()

        names = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cmp-product-details-main__desktop-only")))
        name_all = [element.text.split('\n') for element in names]

        description = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cmp-text")))
        driver.execute_script("window.scrollBy(0, 50);")

        action = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cmp-accordion__icon")))
        action.click()

        cals = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cmp-nutrition-summary__heading-primary")))
        cals_all = [element.text.split('\n') for element in cals]

        sec = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "secondarynutritions")))
        sec_all = [element.text.split('\n') for element in sec]

        dict_items = {
            "name": name_all[0][0],
            "details": {
                "description": description.text,
                "calories": cals_all[0][1],
                "fats": cals_all[0][6],
                "carbs": cals_all[0][11],
                "proteins": cals_all[0][16],
                "unsaturated_fats": sec_all[0][1] if sec_all[0][0] else None,
                "sugar": sec_all[0][4] if sec_all[0][0] else None,
                "salt": sec_all[0][7] if sec_all[0][0] else None,
                "portion": sec_all[0][10] if sec_all[0][0] else None,
            }
        }
        dict_items_list.append(dict_items)

        driver.back()
        print(dict_items)
    driver.quit()
    save_to_json(dict_items_list)

def save_to_json(data_list):
    with open("inventory_data.json", "w") as json_file:
        json.dump(data_list, json_file)


if __name__ == "__main__":
    parse()
