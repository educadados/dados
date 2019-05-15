#!/usr/bin/env python3


import json
import logging

import requests
from pandas.io.json import json_normalize


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

URL = 'http://portal.sme.prefeitura.sp.gov.br///School/List'


def main():
    logger.info('Starting main')
    page = -1
    results = []
    while True:
        page += 1
        logger.debug(f'page: {page:3}')
        resp = requests.get(
            URL,
            headers={'CurrentPage': str(page), 'PageSize': '950'},
            timeout=9
        )
        resp = json.loads(resp.text)
        logger.debug(f'results found: {len(resp)}')
        logger.debug(f'first id: {resp[0]["Id"]}')
        results += resp
        if len(resp) < 950:
            break
    logger.debug(f'end of requests')
    logger.debug(f'converting to dataframe')
    df = json_normalize(results)
    logger.debug(f'saving dataframe')
    df.to_csv('scraped_data.csv.zip', index=False, compression='zip')


if __name__ == '__main__':
    main()
