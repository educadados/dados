#!/usr/bin/env python3


import os
import logging

import pandas as pd

from folder import CLEAN_FOLDER


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    logger.debug(f'Started main')
    logger.debug(f'Reading atribuição')
    atrib = pd.read_csv('../../clean/microdados_servidores_atribuicao.csv')
    logger.debug(f'Reading perfil')
    perfil = pd.read_csv('../../clean/microdados_servidores_perfil.csv')

    logger.debug(f'Preparing to join')
    atrib = atrib.astype('category')
    perfil = perfil.astype('category')

    atrib['cd_serv_sme'] = atrib['cd_serv_sme'].astype(int)
    atrib['cd_serv_sme'].fillna(0, inplace=True)
    atrib['cd_serv_sme'] = atrib['cd_serv_sme'].astype(int)
    atrib['cd_serv_sme'] = atrib['cd_serv_sme'].astype(str)
    atrib['ano'] = atrib['ano'].astype(str)
    atrib['pk'] = atrib['ano'] + '_' + atrib['cd_serv_sme']

    perfil['ano'] = perfil.filename.apply(lambda x: x[14:18])
    perfil['ano'] = perfil['ano'].astype(str)
    perfil['cd_serv_sme'] = perfil['cd_serv_sme'].astype(str)

    perfil['pk'] = perfil['ano'] + '_' + perfil['cd_serv_sme']

    atrib.set_index('pk', inplace=True)
    perfil.set_index('pk', inplace=True)

    atrib = atrib.astype('category')
    perfil = perfil.astype('category')

    logger.debug(f'Join')
    df = pd.merge(
        atrib,
        perfil,
        how='outer',
        left_index=True,
        right_index=True,
    )

    msg = (
        f'Number of lines:' + '\n'
        f'  atribuicao: {atrib.shape[0]:12,.0f}' + '\n'
        f'  perfil:     {perfil.shape[0]:12,.0f}' + '\n'
        f'  join:       {df.shape[0]:12,.0f}'
    )
    logger.debug(msg)

    atrib_id = set(atrib.index)
    perfil_id = set(perfil.index)
    msg = (
        f'Number of uniques IDs in each dataset:' + '\n'
        f'  atrib:        {len(atrib_id):8,.0f}' + '\n'
        f'  perfil:       {len(perfil_id):8,.0f}' + '\n'
        f'  atrib+perfil: {len(atrib_id.intersection(perfil_id)):8,.0f}' + '\n'
        f'  atrib-perfil: {len(atrib_id.difference(perfil_id)):8,.0f}' + '\n'
        f'  perfil-atrib: {len(perfil_id.difference(atrib_id)):8,.0f}'
    )
    logger.debug(msg)

    filename = os.path.join(
        CLEAN_FOLDER,
        'microdados_servidores_joined.csv.zip'
    )
    logger.debug(f'Saving to file {filename}')
    df.reset_index()
    df.to_csv(filename, index=False, compression='zip')


if __name__ == '__main__':
    logger.info(f'Starting')
    main()
    logger.info(f'Finished')
