# Importing necessary libraries :
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import pandas as pd
import re
from time import sleep
from unidecode import unidecode

# Defining a class for scraping information from the website:
class Scraper():
    def __init__(self, url) -> None:
        # Initializing the class with the URL and basic page URL:
        self.url = url
        self.page_basic_url = url + "/fr/occasion/"
        # Initializing a dictionary to store the scraped information:
        self.params = dict(name=[], brand=[], price=[], mileage=[], date=[], city=[
        ], body_type=[], fuel=[], fiscal_horsepower=[], gearbox=[], transmission=[], color=[], safety_equipement=[],
            exterior_equipment=[], interior_equipment=[], functional_equipment=[])
        # Setting the number of pages to scrape:
        self.pages_list = 279
        # Initializing the page number to start scraping:
        self.page_num = 1

    def main(self):
        # Looping through each page to scrape information:
        for i in range(self.pages_list):
            print(f"Page num : {self.page_num}")
            # Getting the URLs of all the cars on the current page:
            cars_url = self.get_car_urls()
            # Looping through each car URL to scrape its information:
            for car_url in cars_url:
                try:
                    self.get_car_info(car_url)
                except Exception as e:
                    # If there is an error, wait for 5 seconds and then continue to the next car URL:
                    print(e)
                    sleep(5)
                    continue
            # Incrementing the page number to move to the next page:
            self.page_num += 1
        # Returning the dictionary containing all the scraped information:
        return self.params

    def get_car_urls(self):
        # Initializing an empty list to store the URLs of all the cars on the current page:
        cars_urls = []
        # Getting the page URL:
        url = self.page_basic_url + str(self.page_num)
        response = requests.get(url)
        soup = bs(response.content, "lxml")
        # Selecting all_offers which contain the link:
        all_offers = soup.findAll("div", attrs={"class", "occasion-item"})
        # Looping through each offer to get the car URL:
        for offer in all_offers:
            # Getting the car URL:
            car_url = offer.find(
                "a", attrs={"class", "details-container"})["href"]
            # Adding the car URL to the list of car URLs:
            cars_urls.append(self.url + car_url)
        # Returning the list of car URLs:
        return cars_urls

    def get_car_info(self, car_url):
        response = requests.get(car_url)
        soup = bs(response.content, "lxml")

        # Get car name :
        title = soup.find("div", attrs={"class", "bloc-title"})
        try:
            car_name = unidecode(title.find("h3", attrs={"class", "page-title"}).text)
        except:
            car_name = np.nan
        try:
            brand = unidecode(title.find("img")["alt"])
        except:
            brand = np.nan
        self.params["name"].append(car_name)
        self.params["brand"].append(brand)
        # Get price / mileage / date_added / city :
        infos = soup.find("div", attrs={"class", "infos"})
        try:
            price = infos.find("div", attrs={"class", "small-price"}).span.text
        except:
            price = np.nan
        try:
            mileage = infos.find("ul").findAll("li")[0].span.text
        except:
            mileage = np.nan
        try:
            date = infos.find("ul").findAll("li")[1].span.text
        except:
            date = np.nan
        try:
            city = unidecode(infos.find("ul").findAll("li")[2].span.text)
        except:
            city = np.nan
        self.params["price"].append(price)
        self.params["mileage"].append(mileage)
        self.params["date"].append(date)
        self.params["city"].append(city)
        # Get body_type/fuel /fiscal_horsepower /gearbox /transmission/color
        try:
            tech_details = soup.find(
                "div", attrs={"class", "technical-details"})
        except:
            tech_details = None
        try:
            body_type = unidecode(re.sub(
                r'[^a-zA-Z0-9]+', '', tech_details.findAll("table")[0].td.text.strip()))
        except:
            body_type = np.nan
        try:
            fuel = unidecode(re.sub(r'[^a-zA-Z0-9]+', '', tech_details.findAll(
                "table")[1].td.text.strip()))
        except:
            fuel = np.nan
        try:
            fiscal_horsepower = re.search(
                r'\d+', tech_details.findAll("table")[2].td.text).group()
        except:
            fiscal_horsepower = np.nan
        try:
            gearbox = unidecode(re.sub(
                r'[^a-zA-Z0-9]+', '', tech_details.findAll("table")[3].td.text.strip()))
        except:
            gearbox = np.nan
        try:
            transmission = unidecode(re.sub(
                r'[^a-zA-Z0-9]+', '', tech_details.findAll("table")[4].td.text.strip()))
        except:
            transmission = np.nan
        try:
            color = unidecode(re.sub(r'[^a-zA-Z0-9]+', '', tech_details.findAll(
                "table")[5].td.text.strip()))
        except:
            color = np.nan
        self.params["body_type"].append(body_type)
        self.params["fuel"].append(fuel)
        self.params["fiscal_horsepower"].append(fiscal_horsepower)
        self.params["gearbox"].append(gearbox)
        self.params["transmission"].append(transmission)
        self.params["color"].append(color)

        #Safety equipment / Exterior equipment /Interior equipment /Functional equipment   
        def extract_features(td):
            return unidecode(re.sub(r'[^\w\sà-öù-ÿœ]+', '',td.text.strip()))
        try:
            details = soup.find("details").find("div",attrs={"class":"row"}).findAll("table")
        except:
            details = None
        try:
            safety_equipement = "/".join(list(map(extract_features,details[0].tbody.findAll("td"))))
        except:
            safety_equipement = np.nan
        try:
            exterior_equipment = "/".join(list(map(extract_features,details[1].tbody.findAll("td"))))
        except:
            exterior_equipment = np.nan
        try:
            interior_equipment = "/".join(list(map(extract_features,details[2].tbody.findAll("td"))))
        except:
            interior_equipment = np.nan
        try:
            functional_equipment = "/".join(list(map(extract_features,details[3].tbody.findAll("td"))))
        except:
            functional_equipment = np.nan
        self.params["safety_equipement"].append(safety_equipement)
        self.params["exterior_equipment"].append(exterior_equipment)
        self.params["interior_equipment"].append(interior_equipment)
        self.params["functional_equipment"].append(functional_equipment)


#Run scaper:
basic_url = "https://www.automobile.tn"
scaper = Scraper(basic_url)
params = scaper.main()
i = range(1, len(params["price"])+1)
df = pd.DataFrame(params,index=i)
df.to_csv("automobile_scraping.csv")
