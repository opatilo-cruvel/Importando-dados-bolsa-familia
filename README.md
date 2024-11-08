# Desafio: Importação de Dados do Bolsa Família para PostgreSQL

Este projeto foi desenvolvido como parte de um desafio acadêmico proposto pelo professor, com o objetivo de criar um algoritmo para a importação de uma base de dados massiva do programa Bolsa Família para o banco de dados PostgreSQL. O desafio incluiu:

1. **Manipulação de Grandes Volumes de Dados**: Importação de uma base com milhões de registros, exigindo uma abordagem otimizada e escalável.
2. **Estruturação para Consultas Rápidas**: O banco de dados deveria permitir consultas eficientes, considerando que a análise e filtragem de dados seriam essenciais.
3. **Preservação da Integridade dos Dados**: Garantia de consistência e precisão durante o processo de importação.
4. **Minimização de Recursos e Tempo de Execução**: O algoritmo deveria otimizar o uso de recursos e reduzir o tempo de carga para um banco de dados de alta performance.

Este repositório documenta a implementação do algoritmo, detalha a estratégia de importação utilizada e discute os desafios técnicos enfrentados.

## Arquivo de dados Importado (Caso você queira utilizar/testar)
- **Mês/Ano**: Pagamentos de Janeiro de 2024 (01/2024)
- **Fonte**: [Portal da Transparência - Bolsa Família](https://dados.gov.br/dados/conjuntos-dados/bolsa-familia---pagamentos)



# Relatório de Importação de Dados para PostgreSQL

## 1. Objetivo do Relatório
Este relatório descreve a estratégia utilizada para importar dados de um arquivo CSV para uma base de dados PostgreSQL, utilizando a linguagem de programação Python e a biblioteca pandas para manipulação de dados. O processo visa carregar um grande volume de dados de forma eficiente, considerando os desafios de leitura de grandes arquivos e a necessidade de otimização do tempo de importação.

## 2. Ferramentas e Tecnologias Utilizadas
- **Python**: Linguagem de programação utilizada para implementar o script de importação.
- **pandas**: Biblioteca Python usada para leitura, manipulação e transformação dos dados.
- **SQLAlchemy**: Biblioteca Python que facilita a conexão e interação com bancos de dados, utilizada para integrar o Python com o PostgreSQL.
- **PostgreSQL**: Sistema gerenciador de banco de dados relacional utilizado para armazenar os dados.

## 3. Estratégia de Importação de Dados (ETL)

### 3.1 Extração (E)
A extração dos dados foi realizada a partir de um arquivo CSV contendo informações sobre o programa Bolsa Família. O arquivo possui aproximadamente 20 milhões de registros, com campos separados por ponto e vírgula e codificação em cp1252. O processo de extração consistiu na leitura desse arquivo em blocos menores para evitar sobrecarga de memória.

- **Leitura do CSV**: Utilizamos a função `pd.read_csv()` da biblioteca pandas para carregar os dados em lotes. A cada iteração, foram lidas 1 milhão de linhas, começando a partir da linha de índice definida pela variável inicial e terminando na linha de índice da variável final.
- **Colunas Definidas**: O arquivo possui uma estrutura de colunas com os seguintes nomes: `mes_competencia`, `mes_referencia`, `uf`, `codigo_municipio_siafi`, `nome_municipio`, `cpf_favorecido`, `nis_favorecido`, `nome_favorecido`, `valor_parcela`. Estas colunas foram definidas explicitamente no código para garantir que os dados fossem carregados de forma correta, mesmo com ausência de cabeçalho no arquivo original.

### 3.2 Transformação (T)
No caso dessa importação específica, não houve necessidade de grandes transformações nos dados durante a leitura. No entanto, é importante destacar que a leitura em pedaços menores ajudou a tratar problemas de desempenho, evitando o consumo excessivo de memória. As transformações realizadas foram mínimas, com foco apenas em garantir que as colunas estivessem corretamente nomeadas e que os dados fossem lidos de maneira eficiente.

### 3.3 Carga (L)
A carga dos dados foi realizada diretamente no banco de dados PostgreSQL. Utilizamos a função `to_sql()` do pandas, que facilita a importação dos dados diretamente de um DataFrame para uma tabela SQL. A tabela de destino foi configurada com o nome `pagamento_janeiro`.

**Parâmetros utilizados**:
- `index=False`: Não incluímos o índice do DataFrame como coluna na tabela SQL.
- `if_exists='append'`: Dados são adicionados à tabela existente. Caso a tabela já contenha dados, os novos dados são adicionados à tabela sem sobrescrever os existentes.

A tabela `pagamento_janeiro` foi populada de forma incremental, sendo que a cada iteração de leitura do CSV, as linhas lidas eram imediatamente carregadas no banco de dados.

## 4. Considerações sobre o Processo
A estratégia adotada foi a de realizar a importação dos dados em "pedaços" menores (batch processing), para controlar o uso de memória e otimizar o desempenho durante a execução. Com isso, conseguimos:
- **Evitar falhas de memória**: Ao carregar o arquivo em blocos de 1 milhão de linhas, conseguimos evitar o sobrecarregamento da memória do sistema, o que poderia ocorrer se tentássemos carregar o arquivo inteiro de uma vez.
- **Controle do progresso da importação**: Durante a execução do processo, um contador foi utilizado para monitorar a quantidade de dados já importados, e o progresso foi impresso na tela como uma porcentagem do total de linhas do arquivo.

Além disso, o uso do `time.sleep(2)` entre cada iteração ajuda a evitar que a conexão com o banco de dados seja sobrecarregada, garantindo que o processo de carga seja realizado de forma estável.

## 5. Desempenho e Resultados
A importação foi realizada de forma bem-sucedida, e a tabela no PostgreSQL foi preenchida com os dados do arquivo CSV. O processo levou aproximadamente 15 minutos.

## 6. Conclusão
A estratégia adotada para importação de dados foi eficiente, utilizando o processo de ETL com Python e pandas para manipular grandes volumes de dados. A leitura em blocos, a carga incremental no banco de dados e a utilização de pausas entre as importações ajudaram a garantir um processo de importação estável e sem falhas. Essa abordagem é escalável e pode ser aplicada a outros conjuntos de dados de tamanho similar.
