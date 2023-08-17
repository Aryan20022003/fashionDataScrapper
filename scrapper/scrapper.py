# designing a web scrapper using beautiful soup and selenium
import requests
import os
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def scrapperRunner(url_template: str, maxPage: int, file_name: str, response: str):
    # for pageNo in range[1, maxPage + 1]:
    #     url = url_template.format(pageNo=pageNo)
    # response=requests.get(url)
    # write response.content to file
    # with open('response.html','w') as file:
    #     file.write(response.content.decode('utf-8'))
    # read response.content from file
    # with open("response.html", "r") as file:
    #     response = file.read()

    # print(response)
    webContents = BeautifulSoup(response, "html.parser").find_all(
        "div", class_="product-collection-block"
    )
    # print(webContents)
    # webContents=BeautifulSoup(response.content,'html.parser').find_all('div',class_='product_group product-like-container')

    # print(len(webContents))

    # make a csv file and write the data to it , it have the following columns
    with open(file_name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "mediaHeading",
                "description",
                "productTile",
                "image",
                "price",
                "vendor",
            ]
        )  # write header

    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)

        for product in webContents:
            title = product.find(
                "a", class_="product-title main_p_title main_p_title_1"
            )
            if title is not None:
                title = title.text.strip()
            else:
                continue

            summary = product.find("div", class_="product-summary")
            if summary is not None:
                summary = summary.text.strip()
            else:
                summary = ""
            # print(title,summary)
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
                writer.writerow(
                    [title, summary, itemTitle, image, itemPrice, itemVendor]
                )

        print(os.path.getsize(file_name))
    return True


def main():
    url_template = "https://www.vogue.in/vogue-closet/?order_by=recent&occasion={occasion}&product-type=bags,clothing,costume-jewellery,fine-jewellery,shoes&page_no={pageNo}"

    for tag in tags:
        pageNo = 1
        url = url_template.format(pageNo=pageNo, occasion=tag)
        response = requests.get(url).content.decode("utf-8")

        maxPage = BeautifulSoup(response, "html.parser").find(
            "div", class_="pagination"
        )

        if maxPage is not None:
            maxPage = int(maxPage.find_all("a")[-2].text.strip())
        else:
            maxPage = 1

        for pageNo in range(1, maxPage + 1):
            print(pageNo)
            url = url_template.format(pageNo=pageNo, occasion=tag)
            response = requests.get(url).content.decode("utf-8")
            # print(response)
            file_name = f"{tag}.csv"
            scrapperRunner(url_template, maxPage, file_name, response)
            print(f"Done with {tag} page {pageNo}")
            # break
        # break


main()
