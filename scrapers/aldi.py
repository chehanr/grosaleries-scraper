"""
Scraper for aldi.com.au
"""

import datetime
import urllib.parse
import requests

from bs4 import BeautifulSoup as soup
from selenium import webdriver

from utils import get_datetime_str


def get_product_objs(soup):
    # TODO: Scrape product url, image url, seperate quantity from price

    product_tile_soup = soup.findAll('a', {'title': 'to product detail'})

    obj_list = []

    for tile in product_tile_soup:
        product_name = tile.find(
            'div', {'class': 'box--description--header'}).text.strip()
        availability = True
        if(tile.find('span', {'class': 'box--baseprice'})):
            price = tile.find('span', {'class': 'box--baseprice'}).text.strip()
        elif(tile.find('span', {'class': 'price-dollars'})):
            price_dollar = tile.find(
                'span', {'class': 'box--value'}).text.strip()
            price_cent = tile.find(
                'span', {'class': 'box--decimal'}).text.strip()
            price = price_dollar + price_cent
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

    for item in soup.find_all('li', {'class', 'tab-nav--item dropdown--list--item'}):
        link = item.find('a')
        obj = {
            'title': link.text.strip(),
            'url': link['href'],
        }

        obj_list.append(obj)

    return obj_list


def scrape(base_url, wait_times=None):
    if wait_times == None:
        wait_times = [3, 5]

    response = requests.get(base_url)
    html = response.content
    page_soup = soup(html, 'lxml')

    # find the navbar element.
    nav_bar_soup = page_soup.find(
        'ul', {'class': 'tab-nav--list dropdown--list ym-clearfix'})

    product_obj_list = []

    # iterate each navbar item (product-category).
    for obj in get_navbar_objs(nav_bar_soup):
        category_product_obj_list = []

        print('{} Scraping category: {}'.format(
            get_datetime_str(),  obj.get('title')))
        print('{} -- page: 0'.format(get_datetime_str()))

        url = obj.get('url')
        response = requests.get(url)

        html = response.content
        category_soup = soup(html, 'lxml')

        # find pagination element.
        # paging_element = category_soup.find(
        #     'div', {'class': 'paging _pagingControl'})
        # page_count = 0

        category_soup = soup(html, 'lxml')

        product_objs = get_product_objs(category_soup)

        if product_objs:
            # Add products to obj list.
            category_product_obj_list.extend(product_objs)

        for item in category_product_obj_list:
            item['category'] = obj.get('title')

        product_obj_list.extend(category_product_obj_list)

    # driver.quit()

    return product_obj_list


class AldiScraper:
    def __init__(self):
        self.__base_url = 'https://www.aldi.com.au/en/groceries/'
        self.__product_obj_list = []

    def __repr__(self):
        return 'Aldi Scraper'

    def execute(self):
        """ Run scraper. """
        self.__product_obj_list = scrape(self.__base_url)

    @property
    def seller_info(self):
        info = {
            "name": "Aldi",
            "description": "Aldi is the common brand of two German family owned discount supermarket chains with over 10,000 stores in 20 countries, and an estimated combined turnover of more than €50 billion.",
            "url": "https://www.aldi.com.au/",
            "added_datetime": None
        }

        return info

    @property
    def product_object_list(self):
        """ Get product list. """

        return self.__product_obj_list
