"""
Scraper for woolworths.com.au
"""

import datetime
import time
import urllib.parse

from bs4 import BeautifulSoup as soup
from selenium import webdriver

from utils import get_datetime_str


def get_product_objs(soup):
    # TODO: Scrape product url, image url, seperate quantity from price

    product_tile_soup = soup.find_all(
        'div', {'class': 'shelfProductTile-information'})

    obj_list = []

    for tile in product_tile_soup:
        product_name = tile.find(
            'h3', {'class': 'shelfProductTile-description'}).text.strip()
        availability = True
        if(tile.find('div', {'class': 'shelfProductTile-cupPrice'})):
            price = tile.find(
                'div', {'class': 'shelfProductTile-cupPrice'}).text.strip()
        elif(tile.find('span', {'class': 'price-dollars'})):
            price_dollar = tile.find('span', {'class': 'price-dollars'})
            price_cent = tile.find('span', {'class': 'price-cents'})
            price = price_dollar.text + '.' + price_cent.text
        else:
            price = None
            availability = False

        obj = {
            "name": product_name,
            "price": price,
            "availability": availability,
            "url": None,
            "image_url": None,
            "datetime": datetime.datetime.now(),
        }

        obj_list.append(obj)

    return obj_list


def get_navbar_objs(soup):
    obj_list = []

    for item in soup.find_all('a', {'class', 'categoryHeader-navigationLink'}):
        obj = {
            'title': item.string.strip(),
            'uri': item['href'],
        }

        obj_list.append(obj)

    return obj_list


def scrape(base_url, wait_times=None):
    if wait_times == None:
        wait_times = [3, 5]

    driver_options = webdriver.ChromeOptions()
    driver_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=driver_options)
    driver.get(base_url)
    time.sleep(wait_times[0])

    html = driver.page_source
    page_soup = soup(html, 'lxml')

    # find the navbar element.
    nav_bar_soup = page_soup.find(
        'nav', {'class': 'categoryHeader-navigation _departmentNav'})

    product_obj_list = []

    # iterate each navbar item (product-category).
    for obj in get_navbar_objs(nav_bar_soup):
        category_product_obj_list = []

        print('{} Scraping category: {}'.format(
            get_datetime_str(),  obj.get('title')))
        print('{} -- page: 0'.format(get_datetime_str()))

        url = urllib.parse.urljoin(base_url, obj.get('uri'))
        driver.get(url)
        time.sleep(wait_times[1])

        html = driver.page_source
        category_soup = soup(html, 'lxml')

        page_number = 1

        while(True):
            print('{} -- page: {}'.format(get_datetime_str(), page_number))

            url = urllib.parse.urljoin(url, '?pageNumber={}'.format(page_number))
            driver.get(url)
            time.sleep(wait_times[1])

            html = driver.page_source
            category_soup = soup(html, 'lxml')

            product_objs = get_product_objs(category_soup)

            if product_objs:
                # Add products to obj list.
                category_product_obj_list.extend(product_objs)
                
                page_number += 1
            else:
                break

        for item in category_product_obj_list:
            item['category'] = obj.get('title')

        product_obj_list.extend(category_product_obj_list)

    driver.quit()

    return product_obj_list


class WoolworthsScraper:
    def __init__(self):
        self.__base_url = 'https://www.woolworths.com.au/shop/browse/'
        self.__product_obj_list = []

    def __repr__(self):
        return 'Woolworths Scraper'

    def execute(self):
        """ Run scraper. """
        self.__product_obj_list = scrape(self.__base_url)

    @property
    def seller_info(self):
        info = {
            "name": "Woolworths",
            "description": "Woolworths Supermarkets is an Australian supermarket/grocery store chain owned by Woolworths Limited. Founded in 1924, Woolworths along with Coles forms a near-duopoly of Australian supermarkets accounting for about 80% of the Australian market",
            "url": "https://www.woolworths.com.au/",
            "added_datetime": None
        }

        return info

    @property
    def product_object_list(self):
        """ Get product list. """

        return self.__product_obj_list
