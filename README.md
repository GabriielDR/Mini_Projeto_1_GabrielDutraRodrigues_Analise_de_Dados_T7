# Mini-projeto — Análise Exploratória de Dados do Varejo

**Aluno:** Gabriel Dutra Rodrigues  
**Turma:** T7 — Análise de Dados com Python

## Objetivo

Realizar uma análise exploratória com pandas, incluindo importação,
diagnóstico da qualidade dos dados, limpeza, estatísticas descritivas
e agrupamentos.

## Como executar

No terminal, a partir da pasta principal do repositório:

```powershell
python -m pip install -r mini_projeto_varejo/requirements.txt
python mini_projeto_varejo/mini_projeto_varejo.py
```

Também é possível abrir o notebook abaixo no VS Code, selecionar um
ambiente Python com pandas e ipykernel e executar as células na ordem.

## Arquivos principais

- [Notebook executado](mini_projeto_varejo/Mini_Projeto_Varejo.ipynb)
- [Script Python](mini_projeto_varejo/mini_projeto_varejo.py)
- [Relatório completo e metodologia](mini_projeto_varejo/README.md)
- [Instruções de execução](mini_projeto_varejo/README_GabrielDutraRodrigues_T7.md)
- [Resultados](mini_projeto_varejo/resultados/)

## Principais resultados

- A limpeza passou de 830.000 para 733.447 registros, separando
  96.553 repetições exatas e preservando 18.471 compras e 1.000 clientes.
- Alimentos apareceram em 98,90% das compras. Uma compra pode conter
  várias categorias, portanto esses percentuais podem somar mais de 100%.
- O grupo F realizou 9.615 compras e o grupo M, 8.856. As frequências
  por cliente foram próximas: 18,53 e 18,41, respectivamente.
- Entre os clientes únicos, a média de filhos foi 1,136;
  a mediana e a moda foram zero.
- Adotando dia/mês/ano, o período observado foi de 04/01/2019
  a 08/12/2022. Maio de 2019 teve mais compras, sem que isso,
  isoladamente, comprove sazonalidade.
- Permaneceram 3.228 registros sem categoria informada. A ausência
  de preços e quantidades impede estimar faturamento e unidades vendidas.

## ETL e qualidade dos dados

A extração consistiu na leitura do CSV com pandas. Na transformação,
foram tratadas colunas vazias, ausências textuais, tipos de dados
e repetições. Na carga, a base limpa e as tabelas foram exportadas.

As repetições foram preservadas em arquivo separado, pois podem
representar erros ou várias unidades do mesmo produto. A análise
considera presença de produtos nas compras, sem estimar unidades vendidas.

## Fonte

[Base Varejo — Kaggle](https://www.kaggle.com/datasets/namespaiva/base-varejo/data)