#!/usr/bin/env python3


import os
import datetime

import pytest
import calendar
import numpy as np
import pandas as pd
from unidecode import unidecode


BASE_FOLDER = os.path.split(os.environ['VIRTUAL_ENV'])[0]
CLEAN_FOLDER = os.path.join(BASE_FOLDER, 'clean')
DEFAULT_INDEX = 'ipca'


def acumulado(end_date=datetime.date.today(),
        start_date=datetime.date(1994,1,31), index=DEFAULT_INDEX):

    global dataset
    start_date = mes_ano(start_date).replace(day=1) - datetime.timedelta(days=1)
    end_date = mes_ano(end_date)
    meses = {1:'JAN', 2:'FEV', 3:'MAR', 4:'ABR', 5:'MAI', 6:'JUN', 7:'JUL',
        8:'AGO', 9:'SET', 10:'OUT', 11:'NOV', 12:'DEZ'}
    if start_date < datetime.date(1994,1,1):
        start_cum = 1
    else:
        start_cum = dataset[(dataset.month==meses[start_date.month])&\
            (dataset.year==start_date.year)].cumulative.values[0]
    end_cum = dataset[(dataset.month==meses[end_date.month])&\
        (dataset.year==end_date.year)].cumulative.values[0]
    return np.round(end_cum / start_cum, decimals=4)

def mes_ano(data):
    if type(data) == datetime.date:
        return data
    elif type(data) == datetime.datetime:
        return data.date()
    elif type(data) == int:
        if data < 1000:
            data += 2000
        if data > 2060:
            data += -100
        return datetime.date(data, 12, 31)
    elif type(data) == str:
        if data.isnumeric():
            dt = datetime.date(int(data), 12, 31)
            if dt.year < 1000:
                dt = dt.replace(year=dt.year+2000)
            if dt.year > 2060:
                dt = dt.replace(year=dt.year-100)
            return dt
        data = data.lower()
        data = unidecode(data)
        meses = {'janeiro':1, 'fevereiro':2, 'marco':3, 'abril':4, 'maio':5,
            'junho':6, 'julho':7, 'agosto':8, 'setembro':9, 'outubro':10,
            'novembro':11, 'dezembro':12}
        for mes,num in meses.items():
            data = data.replace(mes, str(num))
            data = data.replace(mes[:3], str(num))
        formats = ['%m/%Y', '%m-%Y', '%m/%y', '%m-%y']
        for format in formats:
            try:
                dt = datetime.datetime.strptime(data, format).date()
            except ValueError:
                continue
            else:
                dt = dt.replace(day=calendar.monthrange(dt.year,dt.month)[1])
                if dt.year < 1000:
                    dt = dt.replace(year=dt.year+2000)
                if dt.year > 2060:
                    dt = dt.replace(year=dt.year-100)
                return dt
    raise TypeError(f'Value {data} of type {type(data)} is not recognized')


dataset = pd.read_csv(os.path.join(CLEAN_FOLDER, 'ipca.csv'))


# testes
def test_mes_ano_00(): assert mes_ano(2019) == datetime.date(2019,12,31)
def test_mes_ano_01(): assert mes_ano(2014) == datetime.date(2014,12,31)
def test_mes_ano_02(): assert mes_ano(1994) == datetime.date(1994,12,31)
def test_mes_ano_03(): assert mes_ano(19) == datetime.date(2019,12,31)
def test_mes_ano_04(): assert mes_ano(94) == datetime.date(1994,12,31)
def test_mes_ano_05(): assert mes_ano(14) == datetime.date(2014,12,31)
def test_mes_ano_06(): assert mes_ano('2019') == datetime.date(2019,12,31)
def test_mes_ano_07(): assert mes_ano('2014') == datetime.date(2014,12,31)
def test_mes_ano_08(): assert mes_ano('1994') == datetime.date(1994,12,31)
def test_mes_ano_09(): assert mes_ano('19') == datetime.date(2019,12,31)
def test_mes_ano_10(): assert mes_ano('94') == datetime.date(1994,12,31)
def test_mes_ano_11(): assert mes_ano('14') == datetime.date(2014,12,31)
def test_mes_ano_12(): assert mes_ano('12/2019') == datetime.date(2019,12,31)
def test_mes_ano_13(): assert mes_ano('12/2014') == datetime.date(2014,12,31)
def test_mes_ano_14(): assert mes_ano('12/1994') == datetime.date(1994,12,31)
def test_mes_ano_15(): assert mes_ano('09/2019') == datetime.date(2019,9,30)
def test_mes_ano_16(): assert mes_ano('09/2014') == datetime.date(2014,9,30)
def test_mes_ano_17(): assert mes_ano('09/1994') == datetime.date(1994,9,30)
def test_mes_ano_18(): assert mes_ano('9/2019') == datetime.date(2019,9,30)
def test_mes_ano_19(): assert mes_ano('9/2014') == datetime.date(2014,9,30)
def test_mes_ano_20(): assert mes_ano('9/1994') == datetime.date(1994,9,30)
def test_mes_ano_21(): assert mes_ano('09-2019') == datetime.date(2019,9,30)
def test_mes_ano_22(): assert mes_ano('09-2014') == datetime.date(2014,9,30)
def test_mes_ano_23(): assert mes_ano('09-1994') == datetime.date(1994,9,30)
def test_mes_ano_24(): assert mes_ano('9-2019') == datetime.date(2019,9,30)
def test_mes_ano_25(): assert mes_ano('9-2014') == datetime.date(2014,9,30)
def test_mes_ano_26(): assert mes_ano('9-1994') == datetime.date(1994,9,30)
def test_mes_ano_27(): assert mes_ano('jan/2019') == datetime.date(2019,1,31)
def test_mes_ano_28(): assert mes_ano('jan/2014') == datetime.date(2014,1,31)
def test_mes_ano_29(): assert mes_ano('jan/1994') == datetime.date(1994,1,31)
def test_mes_ano_30(): assert mes_ano('JAN/2019') == datetime.date(2019,1,31)
def test_mes_ano_31(): assert mes_ano('JAN/2014') == datetime.date(2014,1,31)
def test_mes_ano_32(): assert mes_ano('JAN/1994') == datetime.date(1994,1,31)
def test_mes_ano_33(): assert mes_ano('janeiro/2019') == datetime.date(2019,1,31)
def test_mes_ano_34(): assert mes_ano('fevereiro/2019') == datetime.date(2019,2,28)
def test_mes_ano_35(): assert mes_ano('marco/2019') == datetime.date(2019,3,31)
def test_mes_ano_36(): assert mes_ano('março/2019') == datetime.date(2019,3,31)
def test_mes_ano_37(): assert mes_ano('Dezembro/2019') == datetime.date(2019,12,31)
def test_mes_ano_38(): assert mes_ano('Dezembro/2019') == datetime.date(2019,12,31)
def test_mes_ano_39():
    with pytest.raises(TypeError):
        mes_ano('xxx')
def test_mes_ano_40():
    with pytest.raises(TypeError):
        mes_ano('')
def test_mes_ano_41():
    with pytest.raises(TypeError):
        mes_ano('January/2018')
def test_mes_ano_42():
    with pytest.raises(TypeError):
        mes_ano('13/19')
def test_mes_ano_43():
    with pytest.raises(TypeError):
        mes_ano('13/2019')

def test_acumulado_01(): assert acumulado(datetime.date(1994,1,1)) == 1.4131
def test_acumulado_02(): assert acumulado(datetime.date(1994,2,1)) == 1.9822
def test_acumulado_03(): assert acumulado(datetime.date(2019,3,1)) == 51.7755
