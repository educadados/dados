import numpy as np
import pandas as pd


filename = '../clean/basedadosexecucao.csv'

dtypes = {
    'linha_original':       np.int64,
    'cd_anoexecucao':       np.int64,
    'cd_exercicio':         np.int64,
    'administracao':        'category',
    'cd_orgao':             np.int64,
    'ds_orgao':             'object',
    'cd_unidade':           np.int64,
    'ds_unidade':           'object',
    'projetoatividade':     np.int64,
    'ds_projeto_atividade': 'object',
    'cd_despesa':           np.int64,
    'ds_despesa':           'category',
    'sld_orcado_ano':       np.int64,
    'vl_atualizado':        np.float64,
    'vl_empenhadoliquido':  np.float64,
    'vl_liquidado':         np.float64,
    'filename':             'category',
    'datainicial':          'datetime',
    'datafinal':            'datetime',
    'cd_exerc_empresa_id':  np.float64,
    'sigla_orgao':          'object',
    'cd_funcao':            np.float64,
    'ds_funcao':            'category',
    'cd_subfuncao':         np.float64,
    'ds_subfuncao':         'category',
    'cd_programa':          np.float64,
    'ds_programa':          'category',
    'pa':                   'category',
    'papa':                 'category',
    'categoria_despesa':    np.float64,
    'ds_categoria':         'category',
    'grupo_despesa':        np.float64,
    'ds_grupo':             'category',
    'cd_modalidade':        np.float64,
    'ds_modalidade':        'category',
    'cd_elemento':          np.float64,
    'cd_fonte':             np.float64,
    'ds_fonte':             'category',
    'vl_congeladoliquido':  np.float64,
    'vl_reservadoliquido':  np.float64,
    'vl_pago':              np.float64,
    'dataextracao':         'datetime',
    'vl_reservado':         np.float64,
    'vl_cancelado':         np.float64,
    'vl_empenhado':         np.float64,
    'vl_anulado':           np.float64,
    'tp_projeto_atividade': np.float64,
    'cd_projeto_atividade': np.float64,
}


def load():
    global dtypes
    tmp_types = dtypes.copy()
    for k,v in tmp_types.items():
        if v == 'category':
            tmp_types[k] = 'object'
    df = pd.read_csv(
        filename,
        dtype = {k:v for k,v in tmp_types.items() if v != 'datetime'},
        parse_dates = [k for k,v in dtypes.items() if v == 'datetime'],
    )
    for k,v in dtypes.items():
        if v == 'category':
            df[k] = df[k].astype('category')
    return df
