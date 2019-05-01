import datetime
import glob
import json
import pathlib
import random
from argparse import ArgumentParser

from scrapers.woolworths import WoolworthsScraper
from scrapers.aldi import AldiScraper

def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def main(output_dir):
    if output_dir == None:
        output_dir = 'output\\'
    
    # Include scraper classes here (for loop?).
    woolies = WoolworthsScraper()
    aldi = AldiScraper()

    scrapers = []
    scrapers.append(woolies)
    scrapers.append(aldi)

    for scraper in scrapers:
        print('*** Running {} ***'.format(scraper))
        scraper.execute()
        seller_obj = scraper.seller_info
        product_objs = scraper.product_object_list
        file_name = '{}{}'.format(output_dir, '{}.json'.format(seller_obj.get('name', scraper).lower()))

        with open(file_name, 'w') as f:
            obj = {
                'seller' : seller_obj,
                'products' : product_objs
            }

            json.dump(obj, f, default=default)


def arg_parse():
    """Argument parser."""

    parser = ArgumentParser(prog='grosalaries-scraper', description='Scraping tools made for the SWE20001 project (GroSaleries) by chehanr.')
    parser.add_argument('-o', '--output_dir', action='store', dest='output_dir',
                        help='output directory', required=False)
    results = parser.parse_args()

    return results


if __name__ == '__main__':
    args = arg_parse()

    main(args.output_dir)
