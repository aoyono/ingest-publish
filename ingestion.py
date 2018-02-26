# -*- coding: utf-8 -*-
"""
ingestion module for functions handling the ingestion of products
"""
import csv
import logging

import requests

logger = logging.getLogger('ingest-publish')


def ingest_local_csv(filename):
    """Ingest a list of products from a local csv file"""
    logger.info('Getting list of products from csv file: %s', filename)
    with open(filename, newline='') as fh:
        fh.readline()  # skip the first line (header line)
        try:
            reader = csv.DictReader(fh, fieldnames=('id', 'name', 'brand', 'retailer', 'price', 'in_stock'),
                                    skipinitialspace=True)
            return [
                __clean_entry(row)
                for row in reader
            ]
        except Exception as e:
            logger.warning('Unable to retrieve products from csv file: %s. Error: %s', filename, e)
            return []


def ingest_remote(url):
    """Ingest a list of products from a remote location"""
    try:
        logger.info('Getting list of products from url: %s', url)
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError as e:
        logger.warning('Unable to retrieve products from url: %s. Error: %s', url, e)
        return []
    return [
        __clean_entry(row)
        for row in response.json()
    ]


def __clean_entry(entry):
    """Private helper to cleanup a product entry from the sources"""
    for key, value in entry.items():
        if not value:
            entry[key] = None
        else:
            if isinstance(value, str):
                value = value.strip()
            if key == 'price' and not isinstance(value, float):
                entry[key] = float(value)
            if key == 'in_stock' and not isinstance(value, bool):
                if value.lower() in ('n', 'no'):
                    entry[key] = False
                elif value.lower() in ('y', 'yes'):
                    entry[key] = True
                else:
                    entry[key] = None
    return entry
