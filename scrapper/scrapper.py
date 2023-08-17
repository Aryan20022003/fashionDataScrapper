# designing a web scrapper using beautiful soup and selenium

import requests
import os
import csv
import time
from bs4 import BeautifulSoup

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

    webContents = BeautifulSoup(response, "html.parser").find_all(
        "div", class_="product-collection-block"
    )

    if not os.path.isfile(full_path):
        with open(full_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "mediaHeading",
                "description",
                "productTile",
                "image",
                "price",
                "vendor",
            ])

    with open(full_path, mode="a", newline="") as file:
        writer = csv.writer(file)

        for product in webContents:
            title = product.find("a", class_="product-title main_p_title main_p_title_1")
            if title:
                title = title.text.strip()
            else:
                continue

            summary = product.find("div", class_="product-summary")
            summary = summary.text.strip() if summary else ""

            productLists = product.find_all("div", class_="product-block")
            for item in productLists:
                image = item.find("img")
                if not image:
                    continue

                image = image["src"]
                itemTitle = item["data-title"]
                itemPrice = item["data-price"]
                itemVendor = item.get("data-vendor", "vogue")
                writer.writerow([title, summary, itemTitle, image, itemPrice, itemVendor])

        print(os.path.getsize(full_path))
    return True


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537"
    }
    
    url_template = "https://www.vogue.in/vogue-closet/?order_by=recent&occasion={occasion}&product-type=bags,clothing,costume-jewellery,fine-jewellery,shoes&page_no={page}"

    for tag in tags:
        page = 1
        url = url_template.format(page=page, occasion=tag)
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to retrieve {url}, status code: {response.status_code}")
            continue

        maxPage = BeautifulSoup(response.content, "html.parser").find("div", class_="pagination")
        if maxPage:
            maxPage = int(maxPage.find_all("a")[-2].text.strip())
        else:
            maxPage = 1

        for page in range(1, maxPage + 1):
            url = url_template.format(page=page, occasion=tag)
            try:
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    print(f"Failed to retrieve {url}, status code: {response.status_code}")
                    continue
                
                file_name = f"{tag}.csv"
                scrapperRunner(file_name, response.content.decode("utf-8"))
                print(f"Done with {tag} page {page}")
                
                # time.sleep(5)  # wait for 5 seconds between requests
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                continue


if __name__ == "__main__":
    main()
