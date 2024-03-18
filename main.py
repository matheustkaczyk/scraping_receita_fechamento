import os
from pandas import DataFrame
from data_processing import processData
from fetch_data import fetchData

YEAR_TARGET = input('Digite o ano desejado: ')
# YEAR_TARGET = '2023'

while not os.path.isfile(f'data_{YEAR_TARGET}.json'):
    fetchData(YEAR_TARGET)

try:
    print('Processando os dados...')
    data = processData(YEAR_TARGET)
    df = DataFrame(data)
    df.to_excel(f'dados{YEAR_TARGET}.xlsx', index=False)
except Exception as e:
    print('Erro ao processar os dados.')
    print(e)

print('Finalizado com sucesso!')
