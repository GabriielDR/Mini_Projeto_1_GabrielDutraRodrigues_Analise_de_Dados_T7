# Instruções de execução

**Aluno:** Gabriel Dutra Rodrigues  
**Turma:** T7 — Análise de Dados com Python

## Ambiente utilizado

VS Code no Windows, Python 3.13.17, pandas 2.2.3 e ipykernel para executar o notebook.

## Execução a partir da pasta principal do repositório

Use um ambiente Python no qual as dependências abaixo estejam instaladas:

```powershell
python -m pip install -r mini_projeto_varejo/requirements.txt
python -m pip install ipykernel
```

Para executar o script:

```powershell
python mini_projeto_varejo/mini_projeto_varejo.py
```

Para usar o notebook, abra `Mini_Projeto_Varejo.ipynb` no VS Code,
selecione esse mesmo ambiente em **Select Kernel** e execute as células na ordem.
No terminal, os comandos de instalação devem usar o Python do ambiente escolhido.

## Dados e resultados

- Entrada: `mini_projeto_varejo/dados/Base_Varejo.csv.gz`.
- Saídas: `mini_projeto_varejo/resultados/`.
- Base limpa: `mini_projeto_varejo/resultados/df_limpo.csv.gz`.

Os arquivos `.csv.gz` são CSVs comprimidos e podem ser lidos diretamente pelo pandas.
O script também funciona quando iniciado em outra pasta, pois localiza os dados
em relação ao próprio arquivo de código.

Consulte o [relatório da análise](RELATORIO_ANALISE.md) para conhecer as decisões
de limpeza, estatísticas, agrupamentos, conclusões e limitações.
