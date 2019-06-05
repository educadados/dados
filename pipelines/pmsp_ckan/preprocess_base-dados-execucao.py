#!/usr/bin/env python3

import os
from io import BytesIO
from zipfile import ZipFile

import pandas as pd

from folder import DOWNLOAD_FOLDER, CLEAN_FOLDER


def get_dataframe(filepath):
    if filepath.endswith('.zip'):
        z = ZipFile(filepath)
        files = z.namelist()
        for file in files:
            if file.endswith('.xls'):
                break
        z = z.read(file)
        z = BytesIO(z)
        df = pd.read_excel(z)
    elif filepath.endswith('.xls'):
        df = pd.read_excel(filepath)
    else:
        raise NotImplementedError
    return df


def file_year(filename):
    if filename.startswith('basedadosexecucao') and filename.endswith('.xls'):
        year = filename.replace('basedadosexecucao', '').replace('.xls', '')
        return int(year)
    elif filename.startswith('200') and filename.endswith('.zip'):
        year = filename[:4]
        return int(year)
    else:
        return 0


def main():
    df = pd.DataFrame()
    for root, folders, files in os.walk(DOWNLOAD_FOLDER):
        for file in files:
            year = file_year(file)
            if year > 0:
                print(f'Processing file {file}')
                partial = get_dataframe(os.path.join(root, file))
                partial['filename'] = file
                partial.reset_index(inplace=True)
                partial.rename(
                    index=str,
                    columns={"index": "linha_original"},
                    inplace=True
                )
                partial.columns = [x.lower() for x in partial.columns]
                df = pd.concat([df, partial], sort=False)
    filename = os.path.join(CLEAN_FOLDER, 'basedadosexecucao.csv')
    print(f'Saving file to disk')
    df.to_csv(filename, index=False)
    print(f'Finished')


if __name__ == '__main__':
    main()
