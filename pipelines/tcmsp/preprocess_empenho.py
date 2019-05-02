#!/usr/bin/env python3


import os
import re
import logging
from zipfile import ZipFile
from io import StringIO

import pandas as pd
from unidecode import unidecode

import folders


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def list_files():
    global folders
    logger.info(f'Listing files')
    folder = folders.EMPENHO_FOLDER
    file_list = []
    for root, _, files in os.walk(folder):
        logger.debug(f'Looking into folder {root}. {len(files)} files found')
        for file in files:
            if file.endswith('.zip'):
                file_list.append(file)
    logger.debug(f'Total .zip files found: {len(file_list)}')
    return file_list


def make_and_save_df(file_list):
    logger.info(f'Consolidate {len(file_list)} in a single file')
    global folders
    df = pd.DataFrame()
    for file in file_list:

        logger.debug(f'Reading {file}')
        filename = os.path.join(folders.EMPENHO_FOLDER, file)
        with ZipFile(filename) as zip:
            filename = zip.namelist()[0]
            file_contents = zip.read(filename)
        file_contents = file_contents.decode('latin1')

        # logger.debug(f'Removing bogus lines')
        # file_contents = file_contents.replace(
        #     ',"SR - SP/MP - CONTRATO DE LOCAÇÃO DE IMÓVEL - PRINCIPAL,',
        #     ',SR - SP/MP - CONTRATO DE LOCAÇÃO DE IMÓVEL - PRINCIPAL,'
        # )
        # file_contents = file_contents.replace(
        #     ',"SR - SP/SM - CONTRATO DE LOCAÇÃO DE IMÓVEL - PRINCIPAL,',
        #     ',SR - SP/SM - CONTRATO DE LOCAÇÃO DE IMÓVEL - PRINCIPAL,'
        # )
        # file_contents = file_contents.replace(
        #     ""","SR - SP/SM' - CONTRATO DE LOCAÇÃO DE IMÓVEL - REEMBOLSO DE SEGURO,""",
        #     """,SR - SP/SM - CONTRATO DE LOCAÇÃO DE IMÓVEL - REEMBOLSO DE SEGURO,""",
        # )
        # file_contents = file_contents.replace(
        #     ',"Aquisição de Luvas de Procedimento Ambidestra Tamanho Médio - ATA de Registro de Preços nº 062/SMS/2009.,',
        #     ',Aquisição de Luvas de Procedimento Ambidestra Tamanho Médio - ATA de Registro de Preços nº 062/SMS/2009.,',
        # )

        logger.debug(f'Parsing')
        temp_df = pd.read_csv(StringIO(file_contents), quoting=3)
        temp_df['arquivo_original'] = file + '/' + filename
        df = pd.concat([df, temp_df])

    logger.debug(f'Final dataframe has shape {df.shape}')
    logger.debug(f'Changing column names')
    def column_parser(name):
        # espaços + Código/cod + Descrição/desc
        s = name.replace(' ', '_')
        s = re.sub('Código_d[eao]_', 'cod_', s)
        s = re.sub('Descrição_d[eao]_', 'desc_', s)
        # camel case to snake case
        s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
        s = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()
        # unidecode (remover acentos)
        s = unidecode(s).replace(' ', '_').replace('__', '_')
        s = s.lower()
        return s

    df.columns = [column_parser(col) for col in df.columns]

    logger.debug(f'Saving dataset to file {filename}')
    if df.shape[0] > 300_000:
        logger.debug(f'Dataset has more then 300k lines')
        logger.debug(f'Saving zipped version')
        filename = os.path.join(folders.CLEAN_FOLDER, 'empenho.csv.zip')
        df.to_csv(filename, index=False, compression='zip')
        logger.debug(f'Saving 100k lines sample version')
        filename = os.path.join(folders.CLEAN_FOLDER, 'empenho_sample.csv')
        df.sample(100_000).to_csv(filename, index=False)
    else:
        logger.debug(f'Saving full dataset')
        filename = os.path.join(folders.CLEAN_FOLDER, 'empenho.csv')
        df.to_csv(filename, index=False)

    return df




if __name__ == '__main__':
    files = list_files()
    df = make_and_save_df(files)
