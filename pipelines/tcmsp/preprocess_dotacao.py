#!/usr/bin/env python3


import os
import re
import logging

import pandas as pd
from unidecode import unidecode

import folders


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def list_files():
    global folders
    logger.info(f'Listing files')
    folder = folders.DOWNLOAD_FOLDER
    file_list = []
    for root, _, files in os.walk(folder):
        logger.debug(f'Looking into folder {root}. {len(files)} files found')
        for file in files:
            if file.endswith('.csv'):
                file_list.append(file)
    logger.debug(f'Total .csv files found: {len(file_list)}')
    return file_list


def make_and_save_df(file_list):
    logger.info(f'Consolidate {len(file_list)} in a single file')
    global folders
    df = pd.DataFrame()
    for file in file_list:
        logger.debug(f'Reading and parsing file {file}')
        filename = os.path.join(folders.DOWNLOAD_FOLDER, file)
        temp_df = pd.read_csv(filename, encoding='latin1')
        temp_df['arquivo_original'] = file
        df = pd.concat([df, temp_df])

    logger.debug(f'Final dataframe has shape {df.shape}')
    logger.debug(f'Changing column names')
    def column_parser(name):
        # espaços + Código/cod + Descrição/desc
        s = name.replace(' ', '_')
        s = re.sub('Código_d[eao]_', 'cod_', s)
        s = re.sub('Descrição_d[eao]_', 'desc_', s)
        # replace('Código', 'cod').replace('Descrição', 'desc')
        # camel case to snake case
        s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
        s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()
        # unidecode (remover acentos)
        s = unidecode(s).replace(' ', '_').replace('__', '_')
        s = s.lower()
        return s

    df.columns = [column_parser(col) for col in df.columns]

    filename = os.path.join(folders.CLEAN_FOLDER, 'dotacao.csv')
    logger.debug(f'Saving dataframe to file {filename}')
    df.to_csv(filename, index=False)

    return df




if __name__ == '__main__':
    files = list_files()
    df = make_and_save_df(files)
