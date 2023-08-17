## Web Scraper for Vogue Closet

This script is designed to scrape product information from the `Vogue Closet` website based on specific occasion tags. The product details are then stored in separate CSV files named after the occasion tags.

### Requirements:
- `requests`
- `BeautifulSoup`
- `os`
- `csv`
- `time`

### Features:
- Scrape products based on occasion tags (e.g. brunch, casual-wear, christmas, etc.)
- Extract the following product details:
    - Media Heading
    - Description
    - Product Title
    - Image URL
    - Price
    - Vendor
- Store the extracted details in separate CSV files for each occasion tag in the `data/` directory.

### How to Use:
1. Clone this repository:
```
git clone https://github.com/Aryan20022003/fashionDataScrapper.git
```

2. Navigate to the repository's root directory:
```
cd fashionDataScrapper/
```

3. Install required packages:
```
pip install requests beautifulsoup4
```

4. Run the script:
```
python scraper.py
```

5. Once executed, the script will start fetching product details for each tag and save them in separate CSV files under the `data/` directory.

### Structure:
The main structure of the script is broken down into two main functions:

- `scrapperRunner(file_name: str, response: str)`: This function parses the HTML content of a page, extracts product details, and appends them to a CSV file named after the occasion tag.

- `main()`: This is the main driver function. It loops through each occasion tag, fetches the webpage content, and invokes the `scrapperRunner` function to scrape and save product details.

### Note:
Remember to respect `robots.txt` and terms of use for any website you're scraping. Use this script responsibly and ensure you're not violating any terms or overloading the server with rapid requests.

### Future Enhancements:
1. Add proxy support to bypass request restrictions.
2. Add error logging to track failed requests or parsing issues.

### Contributing:
Feel free to fork this repository, make improvements, and create a pull request. We welcome any feedback and contributions.
