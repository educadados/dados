#!/usr/bin/env python3


import os


BASE_FOLDER = os.path.split(os.environ['VIRTUAL_ENV'])[0]
DOWNLOAD_FOLDER = os.path.join(BASE_FOLDER, 'raw_data/tcmsp')
CLEAN_FOLDER = os.path.join(BASE_FOLDER, 'clean')
