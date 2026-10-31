# Instruções de execução

Aluno(a): **Gabriel Dutra Rodrigues**

Turma: **T7 - Análise de Dados com Python** (o cabeçalho do enunciado indica T7).

Renomeie este arquivo substituindo SEU_NOME e SUA_TURMA antes de entregar.

## Google Colab

1. Abra o arquivo `Mini_Projeto_Varejo.ipynb` no Google Colab.
2. Envie `dados/Base_Varejo.csv.gz` pelo painel de arquivos do Colab. Ele pode ficar na pasta principal da sessão.
3. Execute as células na ordem, de cima para baixo, lendo as explicações.
4. Confira os resultados; baixe o notebook executado e os resultados.

## VS Code / terminal

Mantenha as pastas e arquivos organizados como neste projeto. No terminal, na pasta do projeto:

```bash
python -m pip install -r requirements.txt
python mini_projeto_varejo.py
```

Os arquivos produzidos ficam em `resultados/`. O arquivo `df_limpo.csv.gz` é um CSV comprimido; o pandas lê esse formato diretamente.

A descrição do projeto, as escolhas de limpeza, a reflexão sobre ETL, os resultados e as referências estão no [README principal](README.md).
