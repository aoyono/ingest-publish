#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The main command line application
"""
import logging

import click

from api import app
from ingestion import ingest_local_csv, ingest_remote

logging.basicConfig()
logger = logging.getLogger('ingest-publish')
logger.setLevel(logging.INFO)


@click.command(name='ingest-publish',
               help='A simple command line utility that publishes an endpoint for getting some price info loaded from a'
                    'local csv file and a remote json resource')
@click.option('--csv-file', type=click.Path(exists=True, dir_okay=False),
              help='A path to a local csv file with a list of products')
@click.option('--url', help='A url pointing to a list of products in json format')
@click.option('-d', '--debug', is_flag=True,
              help='Wether to start the server in debug mode')
@click.option('-h', '--host', type=click.STRING,
              help='The host interface where to publish the endpoint')
@click.option('-p', '--port', type=click.IntRange(0, 65000),
              help='The host port where to publish the endpoint')
def ingpub(csv_file, url, debug, host, port):
    if debug:
        logger.setLevel(logging.DEBUG)
    store = ingest_local_csv(csv_file)
    store.extend(ingest_remote(url))
    app.products_storage = store
    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    ingpub()
