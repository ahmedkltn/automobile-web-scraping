## Project Description

This project is a web scraper written in Python using BeautifulSoup and requests libraries. The purpose of the scraper is to extract information from a car sales website. The scraped data includes various details about each car such as its name, brand, price, mileage, date, city, body type, fuel type, fiscal horsepower, gearbox, transmission, color, safety equipment, exterior equipment, interior equipment, and functional equipment.
## Code Structure

The code is organized into the following sections:

- **Scraper Class**: This section defines the Scraper class and its constructor. The constructor initializes several variables such as the website URL to be scraped, the basic page URL, a dictionary to store the scraped information, the number of pages to scrape, and the page number to start scraping.

- **Main Method**: This section contains the main method that starts the scraping process. For each page, it calls the get_car_urls method to retrieve the URLs of all the cars on that page. Then, for each car URL, it calls the get_car_info method to extract the car's information and add it to the dictionary of scraped information.

- **get_car_urls Method**: This section defines the get_car_urls method that retrieves the URLs of all the cars on a given page.

- **get_car_info Method**: This section defines the get_car_info method that scrapes information from a car's URL, including its name, brand, price, mileage, date, city, body type, fuel type, fiscal horsepower, gearbox, transmission, color, safety equipment, exterior equipment, interior equipment, and functional equipment. If an error occurs during scraping, the method waits for five seconds before continuing to the next car URL.

- **Error Handling**: This section describes how the scraper handles errors during scraping.

- **Returned Data**: This section explains the format of the dictionary that contains all the scraped information.

## Usage

To use this scraper, simply instantiate the Scraper class and call the main method. The scraped data will be returned in a dictionary format.
