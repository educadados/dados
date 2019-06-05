#!/usr/bin/env python3


import os
import logging

import pandas as pd

from folder import DOWNLOAD_FOLDER, CLEAN_FOLDER


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_filelist():
    logger.debug(f'Getting file list')
    folder = os.path.join(
        DOWNLOAD_FOLDER, 'microdados-servidores-atribuicao'
    )
    for root, folder, files in os.walk(folder):
        break
    files = [file for file in files if file.endswith('.csv')]
    files = [os.path.join(root, file) for file in files]
    logger.debug(f'{len(files)} files found')
    return files


def load(filename):
    logger.debug(f'Loading file {filename}')
    df = pd.read_csv(filename, encoding='latin1', sep=';')
    df.columns = map(str.lower, df.columns)
    df['filename'] = os.path.split(filename)[1]
    return df


def main():
    logger.debug(f'Starting main')
    filelist = get_filelist()
    df = []
    for n, file in enumerate(filelist):
        partial = load(file)
        df.append(partial)
    logger.debug('Concatenating dataframes')
    df = pd.concat(df, sort=False, copy=False)
    df.astype('category')
    filename = os.path.join(
        CLEAN_FOLDER,
        'microdados_servidores_atribuicao.csv.zip'
    )
    logger.debug(f'Saving file {filename} to disk')
    df.to_csv(filename, index=False, compression='zip')
    logger.debug(f'Done')


if __name__ == '__main__':
    logger.info(f'Starting')
    main()
    logger.info(f'Finished')
