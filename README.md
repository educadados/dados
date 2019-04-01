# Dados
Repositório com cópia de todos os datasets
Preferencial para python 3.7



# Pastas


### raw_data
Pasta com os datasets baixados (sem tratamento nenhum)
Uma subpasta para cada fonte de dados

##### pmsp_ckan
Portal de dados da prefeitura de São Paulo
http://dados.prefeitura.sp.gov.br/


### clean
Pasta com os datasets ja tratados
- formato padronizado sempre em csv
- separador de colunas: ','
- separador decimal: '.'
- encoding utf8
- sem indices


### pipelines
Package com os pipelines de downloads e tratamento de arquivos

##### settings.py
Arquivo com configurações gerais uteis a todos os pipelines

##### pmsp_ckan
scripts para download e tratamento dos dados do CKAN da prefeitura de São Paulo

