#!/usr/bin/env python3


import os
import hashlib
import logging
from urllib.parse import urljoin

import requests_html

import folders

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


URL_BASE = 'https://portal.tcm.sp.gov.br'
TIMEOUT = 10


def list_all():
    logger.info('Getting list of files')
    url = urljoin(URL_BASE, '/Publicacoes/ResultadoPorSubTipo/')
    payload = {'cdTipoId': '639'}
    with requests_html.HTMLSession() as session:
        resp = session.post(url, data=payload, timeout=TIMEOUT)
    links = resp.html.xpath("//p/a[@href][contains(@title, 'dota')][i[contains(text(),'csv')]]/@href")
    links = [l[24:-20] for l in links]
    logger.info(f'{len(links)} files found')
    return links

def download(link):
    # new file
    url = urljoin(URL_BASE, link)
    logger.info(f'Downloading file. Url: {url}')
    with requests_html.HTMLSession() as session:
        resp = session.get(url, timeout=TIMEOUT*10)
    new_sha256 = hashlib.sha256(resp.content).hexdigest()
    # old file
    filename = resp.headers['Content-Disposition'].split('=')[1]
    try:
        with open(os.path.join(folders.DOWNLOAD_FOLDER, filename), 'rb') as f:
            old_sha256 = hashlib.sha256(f.read()).hexdigest()
    except FileNotFoundError:
        logger.debug(f'Filename {filename} not found')
        old_sha256 = ''
    # if file is the same, return false
    if old_sha256 == new_sha256:
        logger.debug(f'File {filename} already exists.')
        return False
    # or, save file and return filename
    logger.debug(f'New file {filename}. Saving file to disk.')
    with open(os.path.join(folders.DOWNLOAD_FOLDER, filename), 'wb') as f:
        f.write(resp.content)
    return filename





if __name__ == '__main__':
    links = list_all()
    filenames = [download(link) for link in links]
    filenames = [f for f in filenames if f is not False]
