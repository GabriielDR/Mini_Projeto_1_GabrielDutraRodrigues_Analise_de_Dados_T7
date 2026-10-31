# Mini-projeto: análise exploratória da base Varejo

**Aluno(a): Gabriel Dutra Rodrigues**  
**Turma: T7 - Análise de Dados com Python**  

## Objetivo

Usar pandas para importar, verificar a qualidade, limpar e resumir os dados da base Varejo. As perguntas principais são: quais categorias aparecem em mais compras, como as compras se distribuem entre os grupos e qual é o perfil dos clientes quanto ao número de filhos.

## Fonte e escopo

Base indicada no enunciado: [Base Varejo — Kaggle, namespaiva](https://www.kaggle.com/datasets/namespaiva/base-varejo/data), obtida em 28/10/2026. O arquivo `dados/Base_Varejo.csv.gz` preserva integralmente o conteúdo do CSV original, com compressão gzip.

O PDF descritivo que acompanha o dataset apresenta os campos, mas descreve um universo maior, de 50.000 compras em 2010–2022. O **arquivo efetivamente analisado** tem **830.000 registros, 18.471 compras e 1.000 clientes**, com datas interpretadas entre **04/01/2019 e 08/12/2022**. A análise usa esses valores observados, sem assumir que o recorte cobre todas as vendas do período.

Uma linha representa um registro de produto associado a uma compra. Uma compra pode ocupar várias linhas. Não há preços, faturamento, quantidades vendidas nem dimensões físicas.

SHA-256 do CSV original, antes da compressão:

`b26904b7f8ff696127304b327caf5be325e7f1b5ffc49cf95f1fa6c14f737f58`

## Campos

| Campo | Significado | Tipo final |
|---|---|---|
| DATA | Data da compra | datetime |
| CO_ID | Identificação da compra/nota fiscal | string |
| CL_ID | Identificação do cliente | string |
| CL_GENERO | Código F/M informado na base | string |
| CL_EC | Estado civil: 1 casado/união estável; 2 divorciado; 3 separado; 4 solteiro; 5 viúvo | Int64 |
| CL_FHL | Número de filhos | Int64 |
| CL_SEG | Segmento econômico A, B ou C | string |
| PR_ID | Código do produto (SKU) | string |
| PR_CAT | Categoria do produto | string |
| PR_NOME | Nome do produto | string |

## Como executar no VS Code

O projeto foi executado no VS Code com Python 3.13.17 e pandas 2.2.3.
As instruções desta seção consideram o terminal aberto em `mini_projeto_varejo`,
a pasta que contém `requirements.txt` e o notebook.

### Script

```powershell
python -m pip install -r requirements.txt
python mini_projeto_varejo.py
```

### Notebook

Instale o componente necessário ao notebook no mesmo ambiente Python:

```powershell
python -m pip install ipykernel
```

Abra `Mini_Projeto_Varejo.ipynb` no VS Code, selecione esse ambiente em
**Select Kernel** e execute as células de cima para baixo. Os dados de entrada
estão em `dados/Base_Varejo.csv.gz`; o pandas lê o arquivo comprimido diretamente.
O notebook e o script contêm a mesma análise principal.

Os resultados ficam em `resultados/`. Os arquivos CSV não preservam os tipos
Python; para reler a base limpa, informe os identificadores e a coluna de data:

```python
import pandas as pd
df = pd.read_csv(
    "resultados/df_limpo.csv.gz", sep=";", parse_dates=["DATA"],
    dtype={"CO_ID": "string", "CL_ID": "string", "PR_ID": "string"}
)
```

## Diagnóstico e decisões de limpeza

| Problema observado | Evidência | Tratamento e justificativa |
|---|---|---|
| Colunas extras vazias | 4 colunas `Unnamed`, cada uma com 830.000 nulos | Remover somente as colunas sem nome e inteiramente vazias, produzidas pelos separadores extras do CSV. |
| Ausência representada como texto | 3.650 `#N/D` em PR_CAT e 3.650 em PR_NOME, nas mesmas linhas | Reconhecer como ausente. Categoria recebe `Sem Categoria`, por função com `if/else`; nome recebe `Produto não informado`. Preserva-se a compra sem inventar o produto. |
| Texto sem padronização | 7.320 registros com `REFRIGERANTE LIMaO` | Normalizar espaços com expressão regular e letras em maiúsculas. Não reconstruir acentos ou nomes por suposição. |
| Datas como texto | DATA inicialmente é texto | Converter com `datetime.strptime` e o formato `%d/%m/%Y`. Nenhuma data falhou nesse formato. A interpretação dia/mês/ano é uma hipótese documentada, pois datas com dia e mês até 12 são ambíguas. |
| Repetições exatas | 96.553 ocorrências além da primeira | Separar em arquivo e manter uma ocorrência de cada linha inteira na base analítica de presença de produtos. |
| Validação de identificadores | Nenhum identificador inválido pela regra adotada; nenhuma compra com mais de uma data ou cliente | Verificar códigos numéricos positivos e consistência de CO_ID; separar registros inválidos se houver. |

**Atenção à unidade de análise:** CO_ID repetido em diferentes produtos é esperado. A limpeza nunca remove uma compra apenas porque seu código aparece novamente. Sem quantidade ou identificador do item, não se pode comprovar que todas as repetições exatas são erros. A base deduplicada é usada para presença de produtos por compra; as repetições são preservadas em `duplicatas_removidas.csv.gz` e não se estima quantidade física vendida.

**Regra da compra:** o enunciado não especifica tamanho, faixa ou dígito verificador. A regra acima é uma escolha operacional explícita. Uma regra adicional ensinada em aula precisa ser incorporada, caso exista.

**Nulos numéricos:** número de filhos inválido ou ausente não recebe zero. A estatística usa apenas valores disponíveis e informa a contagem de ausentes. Nesta versão, CL_FHL não teve ausências. Não foi necessária imputação de medidas físicas, pois essas colunas não existem no arquivo.

Resultado da limpeza: **733.447 linhas e 10 colunas**, sem registros segregados por identificador/data, mantendo as 18.471 compras e os 1.000 clientes.

## Estatísticas do número de filhos

Para atender ao enunciado, as medidas são calculadas na coluna CL_FHL da base limpa. Para interpretar o perfil dos clientes, são apresentadas também uma vez por cliente. Antes dessa segunda análise, foi verificado que os campos de perfil são consistentes para cada CL_ID neste arquivo.

| Medida | Por registro da base limpa | Por cliente único |
|---|---:|---:|
| Contagem válida | 733.447 | 1.000 |
| Ausentes | 0 | 0 |
| Média | 1,146049 | 1,136000 |
| Mediana | 0 | 0 |
| Desvio padrão amostral (ddof=1) | 1,416917 | 1,413330 |
| Moda | 0 | 0 |
| Mínimo | 0 | 0 |
| Máximo | 4 | 4 |
| Q1 (25%) | 0 | 0 |
| Q2 (50%) | 0 | 0 |
| Q3 (75%) | 2 | 2 |

A média por linha dá mais peso a clientes com mais registros de produto. Para a pergunta “quantos filhos os clientes têm?”, a média por cliente único é a referência mais adequada.

## Agrupamentos

São produzidos cinco agrupamentos com `groupby()`:

1. **Categoria:** registros limpos, compras distintas, clientes distintos e percentual de compras contendo a categoria.
2. **Gênero informado na base:** compras distintas, clientes e compras por cliente.
3. **Categoria × gênero:** compras distintas e registros limpos; primeira combinação de duas variáveis.
4. **Segmento econômico × gênero:** compras e clientes distintos; segunda combinação de duas variáveis.
5. **Mês:** compras distintas ao longo do período.

| Categoria | Compras contendo a categoria | Presença nas 18.471 compras |
|---|---:|---:|
| ALIMENTOS | 18.267 | 98,90% |
| HIGIENE | 17.610 | 95,34% |
| LIMPEZA | 17.475 | 94,61% |
| BEBIDAS | 14.735 | 79,77% |
| PET | 13.495 | 73,06% |
| ACESSORIOS | 9.224 | 49,94% |
| Sem Categoria | 3.228 | 17,48% |

Uma compra pode incluir diversas categorias. Por isso, essas porcentagens **não são parcelas mutuamente exclusivas** e sua soma pode exceder 100%.

| Grupo | Compras | Clientes | Compras por cliente |
|---|---:|---:|---:|
| F | 9.615 | 519 | 18,53 |
| M | 8.856 | 481 | 18,41 |

O grupo F tem maior número absoluto de compras, mas a frequência média por cliente é próxima entre os grupos. Não foi realizado teste de diferença nem análise causal.

## Conclusões

- A base passou de 830.000 para 733.447 registros; foram separadas 96.553 repetições exatas e 0 linhas por identificador/data.

- O recorte contém 18.471 compras e 1.000 clientes, de 04/01/2019 a 08/12/2022, adotando dia/mês/ano. A descrição geral do dataset não substitui o período observado.

- ALIMENTOS aparece em 18.267 compras (98,90% do total). As participações de categorias podem somar mais de 100%.

- O grupo F tem mais compras neste recorte: 9.615. A tabela também informa compras por cliente, para considerar o tamanho dos grupos.

- Nos clientes únicos, a média de filhos é 1,136 e a moda é 0. O mês com mais compras é 2019-05, com 711; isso não demonstra sazonalidade em uma amostra de cobertura não confirmada.

- Há 3.228 registros limpos sem categoria. Sem preços, quantidades e confirmação da origem das repetições, não estimamos faturamento nem unidades vendidas. Não há colunas de dimensões físicas.

## Reflexão sobre ETL e qualidade dos dados

**Extração (Extract):** o CSV é lido com pandas, respeitando o separador e preservando os códigos de identificação como texto. O arquivo original é mantido, permitindo rastrear o ponto de partida.

**Transformação (Transform):** o diagnóstico vem antes das alterações. Colunas vazias, marcadores de ausência, padronização textual, tipos de dados e repetições recebem tratamentos justificados. O contexto define a regra: repetir uma compra em vários produtos é esperado, e um dado ausente não significa zero.

**Carga (Load):** a base limpa, as ocorrências segregadas e as tabelas são exportadas para novos arquivos. Assim, a análise pode ser repetida e suas decisões podem ser verificadas.

A qualidade não se resume a remover nulos e duplicatas. Também envolve validade dos tipos, consistência dos identificadores, preservação do significado dos registros e escolha da unidade de análise. Uma tabela sem nulos ainda pode produzir conclusões incorretas se linhas forem confundidas com compras ou se ausência de preço for ignorada.

As limitações remanescentes são a origem incerta das repetições, o produto/categoria ausente do SKU 107, a ambiguidade de algumas datas e a cobertura não confirmada do recorte. Essas limitações impedem estimar unidades vendidas, faturamento ou tendências representativas de todo o varejo.

## Arquivos

- `mini_projeto_varejo.py`: código comentado executável.
- `Mini_Projeto_Varejo.ipynb`: notebook comentado com a mesma análise.
- `requirements.txt`: versão do pandas utilizada na validação.
- `dados/Base_Varejo.csv.gz`: entrada original comprimida.
- `resultados/df_limpo.csv.gz`: base analítica limpa.
- `resultados/duplicatas_removidas.csv.gz`: ocorrências exatas excedentes, preservadas para conferência.
- `resultados/registros_invalidos.csv`: registros segregados por identificador/data; só contém cabeçalho nesta execução.
- `resultados/qualidade_dados.csv`: nulos por coluna antes e depois do tratamento.
- `resultados/estatisticas_filhos.csv`: todas as medidas solicitadas.
- `resultados/por_*.csv`: tabelas dos agrupamentos.
- `resultados/conclusoes.md`: seis tópicos recalculados pelo código.
- `README_GabrielDutraRodrigues_T7.md`: identificação e instruções de execução no VS Code.

Os resultados descritos neste README correspondem à base identificada acima. Se a entrada mudar, execute novamente o código e atualize a discussão com os novos resultados.

## Referências

- [Base de dados Varejo — Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data).
- Dicionário de campos: PDF `Projeto III - Anlise Exploratria de Dados Utilizando o Python ou RStudio.pdf`, incluído pelo autor no arquivo de download do dataset. As exigências de entrega seguidas são as do mini-projeto SCTEC, apresentadas no enunciado do curso.
- [pandas: read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html).
- [GitHub: adicionar arquivos a um repositório](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
