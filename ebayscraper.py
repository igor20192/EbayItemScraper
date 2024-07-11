import requests
from bs4 import BeautifulSoup
import json
import logging


class EbayScraper:
    """
    A web scraper class for extracting data from eBay product pages.

    Attributes:
        url (str): The URL of the eBay product page.
        data (dict): A dictionary to store scraped data.
        logger (logging.Logger): Logger instance for logging messages.

    Methods:
        setup_logger(): Initializes logging configuration.
        fetch_html(): Fetches HTML content from the specified URL.
        parse_html(html): Parses HTML content to extract title, image URL, price, seller, and shipping price.
        to_json(file_path=None): Converts scraped data to JSON format and saves to a file or prints to console.
        scrape(): Executes the scraping process by fetching HTML, parsing it, and saving data to JSON.
    """

    def __init__(self, url):
        """
        Initializes EbayScraper instance with a given URL.

        Args:
            url (str): The URL of the eBay product page.
        """
        self.url = url
        self.data = {}
        self.setup_logger()

    def setup_logger(self):
        """
        Sets up logging configuration for the scraper.
        """
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler("ebay_scraper.log"), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def fetch_html(self):
        """
        Fetches HTML content from the specified URL.

        Returns:
            str or None: HTML content of the page if successful, None if an error occurs.
        """
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
        """
        Parses HTML content to extract relevant data: title, image URL, price, seller, and shipping price.

        Args:
            html (str): HTML content of the eBay product page.
        """
        try:
            self.logger.info("Parsing HTML.")
            soup = BeautifulSoup(html, "html.parser")

            # Extract title
            title_tag = soup.find("h1", class_="x-item-title__mainTitle")
            self.data["title"] = title_tag.get_text(strip=True) if title_tag else "N/A"

            img_div = soup.find(
                "div", class_="ux-image-carousel-item image-treatment active image"
            )
            img_tag = img_div.find("img") if img_div else None
            self.data["photo_url"] = (
                img_tag["src"] if img_tag and "src" in img_tag.attrs else "N/A"
            )

            # Item URL
            self.data["item_url"] = self.url

            # Extract price
            price_div = soup.find("div", class_="x-price-primary")
            price_tag = (
                price_div.find("span", class_="ux-textspans") if price_div else None
            )
            self.data["price"] = price_tag.get_text(strip=True) if price_tag else "N/A"

            # Extract seller
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

            # Extract shipping price
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
        """
        Converts scraped data to JSON format and saves to a file or prints to console.

        Args:
            file_path (str, optional): File path to save the JSON data. If not provided, prints to console.
        """
        json_data = json.dumps(self.data, indent=4)
        if file_path:
            try:
                self.logger.info(f"Saving data to JSON file: {file_path}")
                with open(file_path, "w") as file:
                    file.write(json_data)
                self.logger.info("Data saved to JSON file successfully.")
            except IOError as e:
                self.logger.error(f"Error saving JSON to file: {e}")
            finally:
                logging.shutdown()  # Ensure logger is closed
        else:
            self.logger.info("Printing JSON data to console.")
            print(json_data)

    def scrape(self):
        """
        Executes the scraping process by fetching HTML, parsing it, and saving data to JSON.
        """
        html = self.fetch_html()
        if html:
            self.parse_html(html)
            self.to_json(file_path="ebayscraper.json")


# Usage example:
if __name__ == "__main__":
    ebay_url = (
        "https://www.ebay.com/itm/154723387946"  # Replace with the actual item URL
    )
    scraper = EbayScraper(ebay_url)
    scraper.scrape()
