#!/usr/bin/env python3


import os
import ftplib
import hashlib
import logging
import zipfile

import numpy as np
import pandas as pd


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


BASE_FOLDER = os.path.split(os.environ['VIRTUAL_ENV'])[0]
DOWNLOAD_FOLDER = os.path.join(BASE_FOLDER, 'raw_data/ibge/ipca')
CLEAN_FOLDER = os.path.join(BASE_FOLDER, 'clean')
FILENAME = 'ipca_SerieHist.zip'


def get_newest():
    # basic info
    logger.debug('Setting up basic info')
    url = 'ftp.ibge.gov.br'
    dir = '/Precos_Indices_de_Precos_ao_Consumidor/IPCA/Serie_Historica/'
    # callback for ftp retrbinary function
    logger.info(f'Downloading data')
    tmp_data = []
    def handle_binary(more_data):
        tmp_data.append(more_data)
    with ftplib.FTP(url, 'anonymous', '') as ftp:
        ftp.cwd(dir)
        filedata = ftp.retrbinary('RETR ' + FILENAME, callback=handle_binary)
    filedata = b''.join(tmp_data)
    # compare buffered file with existing one
    logger.debug('Comparing new data with existing one')
    sha256_new = hashlib.sha256(filedata).hexdigest()
    with open(os.path.join(DOWNLOAD_FOLDER, FILENAME), 'rb') as f:
        sha256_disk = hashlib.sha256(f.read()).hexdigest()
    # if equal: do nothing and warn user
    if sha256_new == sha256_disk:
        logger.warning(f'Downloaded and existing file are the same.')
        return False
    # save only if file is different
    logger.debug(f'Saving file')
    with open(os.path.join(DOWNLOAD_FOLDER, FILENAME), 'wb') as f:
        f.write(filedata)
    return True

def unzip():
    logger.debug('Unzipping file')
    with zipfile.ZipFile(os.path.join(DOWNLOAD_FOLDER, FILENAME), 'r') as zf:
        files = zf.namelist()
        zf.extractall(DOWNLOAD_FOLDER)
        zf.close()
    return [file for file in files if file.endswith('.xls')][0]

def convert_to_csv(filename):
    logger.debug('Converting file to .csv')
    # reading file
    df = pd.read_excel(os.path.join(DOWNLOAD_FOLDER, filename))
    # preparing states
    df2 = []
    year = None
    month = None
    cum = 1
    # run state machine
    for index, row in df.iterrows():
        if row[0] is not np.nan:
            year = row[0]
        if row[1] is not np.nan:
            month = row[1]
        if type(row[3]) == float:
            if row[3] is not np.nan:
                rate = row[3]
                rate = np.round(rate/100, decimals=4)
                cum = np.round(cum * (1+rate), decimals=4)
                df2.append(dict(year=year, month=month, rate=rate, cumulative=cum))
    # convert list of dicts to dataframe
    df2 = pd.DataFrame(df2)
    # save dataframe to csv
    logger.debug('Saving file')
    df2.to_csv(os.path.join(CLEAN_FOLDER, 'ipca.csv'), index=False)


if __name__ == '__main__':
    if get_newest():
        filename = unzip()
        convert_to_csv(filename)
