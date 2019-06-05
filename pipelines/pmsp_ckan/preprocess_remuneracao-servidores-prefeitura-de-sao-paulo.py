#!/usr/bin/env python3


import os
import re
import logging
import datetime
from collections import namedtuple

import pandas as pd

from folder import DOWNLOAD_FOLDER, CLEAN_FOLDER


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_year_month(file):
    patt = '(remuneracao)?(?P<month>\d{2})-?(?P<year>\d{4})ati.*\.csv'
    match = re.match(patt, file.name)
    match = {k: int(v) for k, v in match.groupdict().items()}
    file = file._replace(
        date=datetime.date(year=match['year'], month=match['month'], day=1)
    )
    logger.debug((
        f'Do arquivo {file.name}, extraido mês: {file.date.month} '
        f'e ano: {file.date.year}'
    ))
    return file


def get_file_list():
    logger.info(f'Listando arquivos')
    folder = os.path.join(
        DOWNLOAD_FOLDER, 'remuneracao-servidores-prefeitura-de-sao-paulo/'
    )
    for root, folders, files in os.walk(folder):
        break
    File = namedtuple('File', ['name', 'folder', 'date'], defaults=(None,)*3)
    files = [File(name=file, folder=root) for file in files]
    logger.debug(f'{len(files)} arquivos encontrados')
    logger.debug(f'Filtrando arquivos')
    for n in range(len(files), 0, -1):
        file = files[n-1]
        if not file.name.endswith('.csv'):
            logger.debug(f'Ignorando arquivo {file.name}')
            files.remove(file)
    logger.debug(f'{len(files)} arquivos restantes')
    files = [get_year_month(file) for file in files]
    return files


def main():
    files = get_file_list()
    df = pd.DataFrame()
    for file in files:
        logger.debug(f'Lendo arquivo {file.name}')
        tmp_df = pd.read_csv(
            os.path.join(file.folder, file.name),
            sep=';',
            decimal=',',
            encoding='latin1',
        )
        logger.debug(f'Adicionando colunas extras')
        tmp_df['arquivo_original'] = file.name
        tmp_df['execicio'] = file.date.strftime(f'%Y-%m')
        logger.debug(f'Concatenando')
        df = pd.concat([df, tmp_df], sort=False)
        logger.debug((
            f'Arquivo principal tem {df.shape[0]} '
            f'linhas e {df.shape[1]} colunas'
        ))
    logger.debug(f'Salvando arquivo final')
    df.to_csv(
        os.path.join(CLEAN_FOLDER, 'remuneracao-servidores.csv'),
        index=False,
    )
    return


if __name__ == '__main__':
    main()
