import unittest
from unittest.mock import patch, Mock, mock_open
import requests
from ebayscraper import EbayScraper  # Импортируйте модуль правильно


class TestEbayScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_url = "https://www.example.com"

    def test_fetch_html_success(self):
        with patch("ebayscraper.requests.get") as mock_get:
            mock_response = mock_get.return_value
            mock_response.text = "<html><body>Mock HTML Content</body></html>"
            scraper = EbayScraper(self.test_url)
            html_content = scraper.fetch_html()
            self.assertEqual(
                html_content, "<html><body>Mock HTML Content</body></html>"
            )
            mock_get.assert_called_once_with(self.test_url)

    def test_fetch_html_failure(self):
        with patch("ebayscraper.requests.get") as mock_get:
            mock_get.side_effect = requests.RequestException("Mock HTTPError")
            scraper = EbayScraper(self.test_url)
            html_content = scraper.fetch_html()
            self.assertIsNone(html_content)

    def test_parse_html_success(self):
        mock_html = """
        <html>
        <body>
        <h1 class="x-item-title__mainTitle">Mock Title</h1>
        <div class="ux-image-carousel-item image-treatment active image">
            <img src="mock_image_url" alt="Mock Image">
        </div>
        <div class="x-price-primary">
            <span class="ux-textspans">EUR 100.00</span>
        </div>
        <h2 class="d-stores-info-categories__container__info__section__title">
            <span class="ux-textspans ux-textspans--BOLD">Mock Seller</span>
        </h2>
        <div class="ux-labels-values__values-content">
            <span class="ux-textspans ux-textspans--BOLD">EUR 10.00</span>
        </div>
        </body>
        </html>
        """
        scraper = EbayScraper(self.test_url)
        scraper.parse_html(mock_html)
        expected_data = {
            "title": "Mock Title",
            "photo_url": "mock_image_url",
            "item_url": self.test_url,
            "price": "EUR 100.00",
            "seller": "Mock Seller",
            "shipping_price": "EUR 10.00",
        }
        self.assertEqual(scraper.data, expected_data)

    def test_parse_html_error(self):
        mock_html = "<html><body>Invalid HTML Content</body></html>"
        scraper = EbayScraper(self.test_url)
        scraper.parse_html(mock_html)
        self.assertEqual(
            scraper.data["title"], "N/A"
        )  # or another default value you set

    def test_to_json(self):
        scraper = EbayScraper(self.test_url)
        scraper.data = {
            "title": "Mock Title",
            "photo_url": "mock_image_url",
            "item_url": self.test_url,
            "price": "EUR 100.00",
            "seller": "Mock Seller",
            "shipping_price": "EUR 10.00",
        }
        with patch("builtins.open", mock_open()) as mock_file:
            scraper.to_json(file_path="mock_output.json")
            mock_file.assert_called_once_with("mock_output.json", "w")
            mock_file().write.assert_called_once_with(
                '{\n    "title": "Mock Title",\n    "photo_url": "mock_image_url",\n    "item_url": "https://www.example.com",\n    "price": "EUR 100.00",\n    "seller": "Mock Seller",\n    "shipping_price": "EUR 10.00"\n}'
            )

    def test_scrape(self):
        mock_html = """
        <html>
        <body>
        <h1 class="x-item-title__mainTitle">Mock Title</h1>
        <div class="ux-image-carousel-item image-treatment active image">
            <img src="mock_image_url" alt="Mock Image">
        </div>
        <div class="x-price-primary">
            <span class="ux-textspans">EUR 100.00</span>
        </div>
        <h2 class="d-stores-info-categories__container__info__section__title">
            <span class="ux-textspans ux-textspans--BOLD">Mock Seller</span>
        </h2>
        <div class="ux-labels-values__values-content">
            <span class="ux-textspans ux-textspans--BOLD">EUR 10.00</span>
        </div>
        </body>
        </html>
        """
        with patch.object(EbayScraper, "fetch_html", return_value=mock_html):
            scraper = EbayScraper(self.test_url)
            scraper.scrape()
            expected_data = {
                "title": "Mock Title",
                "photo_url": "mock_image_url",
                "item_url": self.test_url,
                "price": "EUR 100.00",
                "seller": "Mock Seller",
                "shipping_price": "EUR 10.00",
            }
            self.assertEqual(scraper.data, expected_data)


if __name__ == "__main__":
    unittest.main()
