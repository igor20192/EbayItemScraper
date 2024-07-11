# Ebay Item Scraper

Ebay Item Scraper is a Python project for scraping item details from eBay listings. It fetches the HTML content of an eBay item page, parses the relevant details such as title, image URL, price, seller, and shipping price, and saves this data to a JSON file.

## Features

- Fetches HTML content from a given eBay item URL.
- Parses item details including title, image URL, price, seller, and shipping price.
- Saves the parsed data to a JSON file.
- Provides logging of the scraping process.
- Includes unit tests to ensure the reliability of the scraper.

## Requirements

- Python 3.7 or higher
- `requests` library
- `beautifulsoup4` library
- `unittest` library (for testing)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/igor20192/EbayItemScraper.git
    cd EbayItemScraper
    ```

2. Install the required libraries:
    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

1. Update the `ebay_url` variable in the script with the URL of the eBay item you want to scrape:
    ```python
    ebay_url = "https://www.ebay.com/itm/154723387946"
    ```

2. Run the scraper:
    ```bash
    python ebayscraper.py
    ```

3. The scraped data will be saved to `ebayscraper.json`.

## Example

```python
if __name__ == "__main__":
    ebay_url = "https://www.ebay.com/itm/154723387946"  # Replace with the actual item URL
    scraper = EbayScraper(ebay_url)
    scraper.scrape()
```

## Logging

Logs are saved to ebay_scraper.log and also printed to the console. The logging configuration can be adjusted in the setup_logger method of the EbayScraper class.

## Running Tests

```bash
python -m unittest test_ebayscraper.py 
```

## Project Structure

```bash
ebay-item-scraper/
├── ebayscraper.py        # Main scraper script
├── test_ebayscraper.py   # Unit tests
├── ebay_scraper.log      # Log file
├── ebayscraper.json      # Output JSON file
└── README.md             # Project information
```
## Contributing

This project is licensed under the MIT License. See the LICENSE file for details.