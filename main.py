import pandas as pd
import sqlalchemy as sql
import time

# Configurando a conexão
user = 'postgres'
password = 'suasenha'
host = 'localhost'
port = '5432'
database = 'nome-tabela'

engine = sql.create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

inicial = 0
final = 1000000
cont = 0
novas_colunas = ["mes_competencia", "mes_referencia", "uf", "codigo_municipio_siafi", "nome_municipio", "cpf_favorecido", "nis_favorecido", "nome_favorecido", "valor_parcela"]

while cont <= 20:
    df = 0
    df = pd.read_csv('202401_NovoBolsaFamilia.csv', delimiter=';', encoding='cp1252', names=novas_colunas, header=0, skiprows=inicial, nrows=final)
    df.to_sql('pagamento_janeiro', engine, index=False, if_exists='append') 
    cont+=1
    time.sleep(2) # Pausa para evitar erros
    if cont < 20:
        inicial += 1000000
    else:
        if cont != 21:
            inicial += 1000000
        final = 833379

    # Condição para ver o loading dos dados sendo importados
    if cont == 20:
        print(inicial/20833379*100)
    else:
        print((inicial+final)/20833379*100)



