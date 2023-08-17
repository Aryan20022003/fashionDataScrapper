import requests
import os
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

tags = [
    "brunch",
    "casual-wear",
    "christmas",
    "cocktail",
    "date-night",
    "diwali",
    "evening",
    "gym-wear",
    "lunch",
    "puja",
    "work-wear",
]

def scrapperRunner(file_name: str, response: str):
    full_path = "./data/" + file_name

    # Create the directory if it doesn't exist
    if not os.path.exists("./data/"):
        os.makedirs("./data/")
    
    webContents = BeautifulSoup(response, "html.parser").find_all("div", class_="product-collection-block")

    if not os.path.isfile(full_path):
        with open(full_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["mediaHeading", "description", "productTile", "image", "price", "vendor"])  # write header

    with open(full_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        for product in webContents:
            title = product.find("a", class_="product-title main_p_title main_p_title_1")
            if title is not None:
                title = title.text.strip()
            else:
                continue

            summary = product.find("div", class_="product-summary")
            if summary is not None:
                summary = summary.text.strip()
            else:
                summary = ""
            
            productLists = product.find_all("div", class_="product-block")
            for item in productLists:
                image = item.find("img")
                if image is not None:
                    image = image["src"]
                else:
                    continue
                itemTitle = item["data-title"]
                itemPrice = item["data-price"]
                itemVendor = item["data-vendor"] or "vogue"
                writer.writerow([title, summary, itemTitle, image, itemPrice, itemVendor])

        print(os.path.getsize(full_path))

def is_next_button_clickable(driver):
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "next-link"))
        )
        return next_button
    except TimeoutException:
        return None

def automaker(url: str, file_name: str):
    driver = webdriver.Chrome()
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "product-collection-block"))
    )

    while True:
        try:
            page_source = driver.page_source
            scrapperRunner(file_name, page_source)

            next_button = is_next_button_clickable(driver)
            if next_button:
                next_button.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
            else:
                break
        except NoSuchElementException:
            print("Next button not found. Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

    driver.quit()

def main():
    url_template1 = "https://www.vogue.in/vogue-closet/?order_by=recent&occasion={occasion}&product-type=bags,clothing,costume-jewellery,fine-jewellery,shoes&"

    for tag in tags:
        url = url_template1.format(occasion=tag)
        file_name = f"{tag}.csv"
        automaker(url, file_name)

main()
