import datetime
import glob
import json
import pathlib
import random
from argparse import ArgumentParser

from scrapers.woolworths import WoolworthsScraper


def default(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


def main(output_dir):
    if output_dir == None:
        output_dir = 'output\\'
    
    # Include scraper classes here (for loop?).
    woolies = WoolworthsScraper()
    print('*** Running {} ***'.format(woolies))
    woolies.execute()
    objs = woolies.product_object_list
    file_name = '{}{}'.format(output_dir, 'woolies.json')

    with open(file_name, 'w') as f:
        json.dump(objs, f, default=default)


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
