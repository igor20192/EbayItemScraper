import requests
from bs4 import BeautifulSoup
import json
import logging


class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.data = {}
        self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("ebay_scraper.log"), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def fetch_html(self):
        try:
            self.logger.info(f"Fetching HTML for URL: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            self.logger.info("HTML fetched successfully.")
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching the HTML from {self.url}: {e}")
            return None

    def parse_html(self, html):
        try:
            self.logger.info("Parsing HTML.")
            soup = BeautifulSoup(html, "html.parser")
            self.data["title"] = soup.find(
                "h1", class_="x-item-title__mainTitle"
            ).get_text(strip=True)

            img_tag = soup.find(
                "div", class_="ux-image-carousel-item image-treatment active image"
            ).find("img")
            self.data["photo_url"] = img_tag["src"] if img_tag else "N/A"

            self.data["item_url"] = self.url

            price_div = soup.find("div", class_="x-price-primary")
            price_tag = (
                price_div.find("span", class_="ux-textspans") if price_div else None
            )
            self.data["price"] = price_tag.get_text(strip=True) if price_tag else "N/A"

            seller_div = soup.find(
                "h2", class_="d-stores-info-categories__container__info__section__title"
            )
            seller_tag = (
                seller_div.find("span", class_="ux-textspans ux-textspans--BOLD")
                if seller_div
                else None
            )
            self.data["seller"] = (
                seller_tag.get_text(strip=True) if seller_tag else "N/A"
            )

            shipping_div = soup.find("div", class_="ux-labels-values__values-content")
            shipping_tag = (
                shipping_div.find("span", class_="ux-textspans ux-textspans--BOLD")
                if shipping_div
                else None
            )
            self.data["shipping_price"] = (
                shipping_tag.get_text(strip=True) if shipping_tag else "N/A"
            )
            self.logger.info("HTML parsed successfully.")
        except AttributeError as e:
            self.logger.exception(f"Error parsing the HTML: {e}")

    def to_json(self, file_path=None):
        json_data = json.dumps(self.data, indent=4)
        if file_path:
            try:
                self.logger.info(f"Saving data to JSON file: {file_path}")
                with open(file_path, "w") as file:
                    file.write(json_data)
                self.logger.info("Data saved to JSON file successfully.")
            except IOError as e:
                self.logger.error(f"Error saving JSON to file: {e}")
        else:
            self.logger.info("Printing JSON data to console.")
            print(json_data)

    def scrape(self):
        html = self.fetch_html()
        if html:
            self.parse_html(html)
            self.to_json(file_path="ebayscraper.json")


# Usage example:
if __name__ == "__main__":
    ebay_url = "https://www.ebay.com/itm/154723387946?itmmeta=01J2GXZ216JB76QMPTBRHEEECP&hash=item24063b8a2a:g:2NwAAOSw~ddfjxIu&itmprp=enc%3AAQAJAAAA0Lp6dUGagrfO93WeRwZeeXRWLasf7ztAQo7wyUCk6ajQqUGupKhFYn02%2BvK2tXQtpQfmzFNc6%2BisWCUMRmrIOUCQhKCr3p9O5O6dFFbhZT2Dg9b5Ir6XVTt%2FJBDgESrUi912axCwNXinQF%2BO6gzRg61r7tO5Q%2BL74pZXzgd7wGsgDo6MLA5Zvevq7qPHBfAFJODLnf7dmupl2yI6YRzYZG%2BXsdlyClvz2dQrB6E5uIqUjUGbPu8D6PCsNiCDK7a5QdjKJsgBZ1WS7zZBdlu72FQ%3D%7Ctkp%3ABk9SR9Sg_J2UZA"  # Replace with the actual item URL
    scraper = EbayScraper(ebay_url)
    scraper.scrape()
