#!/usr/bin/env python3


import os
import json
import hashlib

import requests
import pandas as pd
from tqdm import tqdm
from unidecode import unidecode

from folder import DOWNLOAD_FOLDER, CLEAN_FOLDER


URL = 'http://dados.prefeitura.sp.gov.br/'
TIMEOUT = 5
MANUAL_PACKAGES = {
    'base-dados-execucao',
    'sistema-de-acompanhamento-da-administracao-indireta-sadin-compilado',
    'remuneracao-servidores-prefeitura-de-sao-paulo',
    'microdados-servidores-atribuicao',
    'microdados-servidores-perfil',
}


def hashfile(filename, filepath='.'):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()
    with open(os.join(filepath, filename), 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def get(url, timeout=None):
    if timeout is None:
        timeout = TIMEOUT
    resp = requests.get(url, timeout=timeout)
    if not resp.ok:
        msg = 'Status code not 200' + '\n'
        msg += f'Url: {url}' + '\n'
        msg += f'Status Code: {resp.status_code}'
        raise requests.exceptions.ConnectionError(msg)
    return json.loads(resp.text)


def get_package_list():
    endpoint = 'api/3/action/package_list'
    url = URL + endpoint
    resp = get(url)
    return resp['result']


def get_datasets_from_package(package_name):
    endpoint = f'api/3/action/package_show?id={package_name}'
    url = URL + endpoint
    resp = get(url)
    try:
        resp = resp['result']['resources']
    except KeyError:
        print(f'\n\nPackage name: {package_name}\nUrl: {url}')
        raise
    return resp


def dataset_exists(dataset):
    folder = os.path.join(DOWNLOAD_FOLDER, dataset['package_name'])
    if not os.path.isdir(folder):
        return False
    filename = os.path.join(folder, dataset['url'].split(r'/')[-1])
    return os.path.isfile(filename)


def save_dataset(dataset_name, package_name, file_contents):
    # check if package folder exists, if not, create it
    folder = os.path.join(DOWNLOAD_FOLDER, package_name)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    # save the file
    filename = os.path.join(folder, dataset_name)
    with open(filename, 'wb') as f:
        f.write(file_contents)


def to_save(resource):
    if resource['package_name'] in MANUAL_PACKAGES:
        return True
    target_words = {
        'educacao',
        'escolar',
        'cultura',
        'docente',
        'educacionai',
        'educacional',
        'ensino',
        'escolar',
        'aluno',
        'professor',
        'professores',
        'sme',
    }
    description = resource['description'].split()
    name = resource['name'].split()
    package = resource['package_name'].split('-')
    words = description + name + package
    words = [unidecode(i).lower() for i in words]
    words = words + [i[:-1] for i in words]
    words = set(words)
    if words.intersection(target_words):
        return True
    else:
        return False


def main():
    # get packages
    print(f'Getting packages list. ', end='')
    packages = get_package_list()
    print(f'{len(packages)} packages found.')

    # get resources
    datasets = []
    print(f'Getting dataset list:', flush=True)
    for package in tqdm(packages):
        resources = get_datasets_from_package(package)
        for i in range(len(resources)):
            resources[i].update({'package_name': package})
            resources[i].update({'to_save': to_save(resources[i])})
        datasets += resources
    print(f'\t{len(datasets)} Datasets found.', flush=True)

    # Make table from all datasets
    print(f'Creating dataframe. ', end='', flush=True)
    df = pd.DataFrame(datasets)
    df.to_csv(os.path.join(CLEAN_FOLDER, 'datasets.csv'), index=False)
    print(f'Done.', flush=True)

    # filter eductaion datasets
    datasets = [i for i in datasets if i['to_save']]

    # download and save resources
    print(f'Downloading {len(datasets)} datasets (after filter):', flush=True)
    for dataset in tqdm(datasets):
        if not dataset_exists(dataset):
            url = dataset['url']
            resp = requests.get(url, timeout=600)
            save_dataset(
                url.split(r'/')[-1],
                dataset['package_name'],
                resp.content
            )
    print(f'\tDone', flush=True)


if __name__ == '__main__':
    main()
