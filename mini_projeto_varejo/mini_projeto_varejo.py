# %% [markdown]
# # Mini-projeto: análise exploratória da base Varejo
# **Aluno(a):** Gabriel Dutra Rodrigues | **Turma:** T7 - Análise de Dados com Python
#
# Objetivo: importar, diagnosticar, limpar e resumir uma base com pandas.
# Execute os blocos na ordem. Uma linha é um registro de produto em uma compra;
# `CO_ID` identifica a compra e `CL_ID` identifica o cliente.
# A base não contém preços, valores monetários, quantidades ou dimensões físicas.

# %% [markdown]
# ## 1. Importação
# `read_csv` lê o arquivo; `sep=";"` informa que as colunas são separadas por
# ponto e vírgula. Identificadores ficam como texto, pois são códigos.
# A versão `.csv.gz` contém os mesmos bytes do CSV, apenas comprimidos.

# %%
from pathlib import Path
from datetime import datetime
import pandas as pd

# No script, procura arquivos ao lado do código; no notebook, na pasta atual.
PASTA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
candidatos = [PASTA / "dados" / "Base_Varejo.csv.gz",
              PASTA / "Base_Varejo.csv.gz", PASTA / "Base Varejo.csv",
              PASTA / "Varejo.csv"]
ARQUIVO = next((p for p in candidatos if p.exists()), None)
if ARQUIVO is None:
    raise FileNotFoundError("Coloque Base_Varejo.csv.gz na pasta dados ou junto ao notebook.")

SAIDA = PASTA / "resultados"
SAIDA.mkdir(exist_ok=True)
df_bruto = pd.read_csv(
    ARQUIVO, sep=";", encoding="utf-8",
    dtype={"CO_ID": "string", "CL_ID": "string", "PR_ID": "string"},
    low_memory=False,
)
print(f"Registros: {len(df_bruto):,} | Colunas: {df_bruto.shape[1]}")
print("\nTipos após a importação:\n", df_bruto.dtypes)
print("\nPrimeiros registros:\n", df_bruto.head().to_string(index=False))

# %% [markdown]
# ## 2. Diagnóstico antes da limpeza
# `isna()` identifica ausências reconhecidas pelo pandas. O texto `#N/D`
# também significa informação ausente, mas precisa ser reconhecido por nós.
# `duplicated()` conta repetições completas além da primeira ocorrência.

# %%
nulos_antes = df_bruto.isna().sum()
duplicatas_antes = int(df_bruto.duplicated().sum())
print("Nulos reconhecidos na leitura:\n", nulos_antes)
print("\nDuplicatas exatas além da primeira:", duplicatas_antes)

# Remove somente colunas sem nome e inteiramente vazias.
colunas_vazias = [c for c in df_bruto.columns
                  if c.startswith("Unnamed:") and df_bruto[c].isna().all()]
df = df_bruto.drop(columns=colunas_vazias).copy()
print("\nColunas vazias removidas:", colunas_vazias)

# Normaliza espaços com expressão regular e identifica marcadores de ausência.
for coluna in df.columns:
    df[coluna] = df[coluna].astype("string").str.strip()
    df[coluna] = df[coluna].str.replace(r"\s+", " ", regex=True)
    df[coluna] = df[coluna].replace(["", "#N/D", "NULL", "N/A"], pd.NA)

nulos_reconhecidos = df.isna().sum()
print("\nNulos após reconhecer marcadores textuais:\n", nulos_reconhecidos)
nomes_padronizados = int((df["PR_NOME"] != df["PR_NOME"].str.upper()).sum())

# %% [markdown]
# ## 3. Limpeza de textos, nulos, números e datas
# Categoria ausente recebe "Sem Categoria", sem inventar a categoria verdadeira.
# Nomes de produto são padronizados em maiúsculas. Dados numéricos inválidos
# viram ausentes, nunca zero. Zero filhos é uma informação válida.
# Datas seguem a hipótese explícita dia/mês/ano, usual no contexto brasileiro.

# %%
def preencher_categoria(valor):
    """Usa if/else, conforme o critério da atividade."""
    if pd.isna(valor):
        return "Sem Categoria"
    else:
        return valor.upper()


df["PR_CAT"] = df["PR_CAT"].apply(preencher_categoria).astype("string")
df["PR_NOME"] = df["PR_NOME"].str.upper().fillna("Produto não informado")
df["CL_GENERO"] = df["CL_GENERO"].str.upper().fillna("Não informado")
df["CL_SEG"] = df["CL_SEG"].str.upper().fillna("Não informado")

for coluna in ["CL_FHL", "CL_EC"]:
    numeros = pd.to_numeric(df[coluna], errors="coerce")
    # Int64, com I maiúsculo, permite inteiros e valores ausentes.
    validos = numeros.ge(0) & numeros.mod(1).eq(0)
    if coluna == "CL_EC":
        validos = validos & numeros.between(1, 5)
    df[coluna] = numeros.where(validos).astype("Int64")


def converter_data(texto):
    """Usa o módulo datetime; datas ausentes/inválidas viram NaT."""
    if pd.isna(texto):
        return pd.NaT
    try:
        return datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        return pd.NaT


# Converte cada data distinta uma vez, evitando repetir trabalho em 830 mil linhas.
mapa_datas = {texto: converter_data(texto) for texto in df["DATA"].dropna().unique()}
df["DATA"] = pd.to_datetime(df["DATA"].map(mapa_datas))
print("Datas ausentes ou inválidas:", int(df["DATA"].isna().sum()))
print("Nomes de produto padronizados:", nomes_padronizados)

# %% [markdown]
# ## 4. Validação dos identificadores e separação de inconsistências
# O enunciado não informa tamanho obrigatório ou dígito verificador de `CO_ID`.
# Adotamos e documentamos uma regra operacional: código numérico positivo;
# cada compra deve corresponder a uma data e a um cliente.
# Repetir CO_ID em vários produtos é esperado e não significa duplicata.

# %%
id_invalido = pd.Series(False, index=df.index)
for coluna in ["CO_ID", "CL_ID", "PR_ID"]:
    somente_digitos = df[coluna].str.fullmatch(r"[0-9]+", na=False)
    maior_que_zero = pd.to_numeric(df[coluna], errors="coerce").gt(0).fillna(False)
    id_invalido = id_invalido | ~(somente_digitos & maior_que_zero)

consistencia_compras = df.groupby("CO_ID")[["DATA", "CL_ID"]].nunique()
compras_conflitantes = consistencia_compras.index[
    consistencia_compras.gt(1).any(axis=1)]
registro_invalido = (id_invalido | df["DATA"].isna()
                    | df["CO_ID"].isin(compras_conflitantes))
registros_invalidos = df.loc[registro_invalido].copy()
df_valido = df.loc[~registro_invalido].copy()
print("Compras com conflito de data/cliente:", len(compras_conflitantes))
print("Linhas separadas por identificador ou data:", len(registros_invalidos))
if df_valido.empty:
    raise ValueError("Não restaram registros válidos para analisar.")

# %% [markdown]
# ## 5. Duplicatas e unidade de análise
# Removemos apenas linhas inteiramente iguais depois da padronização.
# Guardamos as ocorrências excedentes em um arquivo separado.
# Sem quantidade e identificador do item, não sabemos se as repetições são
# erros ou várias unidades do mesmo produto. A base deduplicada representa
# presença de SKU na compra; não deve estimar unidades vendidas.

# %%
mascara_duplicatas = df_valido.duplicated(keep="first")
duplicatas_removidas = df_valido.loc[mascara_duplicatas].copy()
df_limpo = df_valido.loc[~mascara_duplicatas].copy()
print("Linhas após a limpeza:", len(df_limpo))
print("Repetições exatas separadas:", len(duplicatas_removidas))
print("Compras distintas:", df_limpo["CO_ID"].nunique())
print("Clientes distintos:", df_limpo["CL_ID"].nunique())
print("\nTipos finais:\n", df_limpo.dtypes)

# %% [markdown]
# ## 6. Estatísticas do número de filhos
# Calculamos todas as medidas pedidas na coluna CL_FHL da base limpa.
# Também calculamos uma vez por cliente: quem compra mais não deve ter peso
# maior se a pergunta é o perfil dos clientes. Antes, verificamos a consistência.
# Valores ausentes ficam fora das estatísticas; a quantidade ausente é informada.

# %%
def estatisticas(serie):
    valores = serie.dropna()
    return pd.Series({
        "contagem": valores.count(), "ausentes": serie.isna().sum(),
        "media": valores.mean(), "mediana": valores.median(),
        "desvio_padrao_amostral": valores.std(ddof=1),
        "moda": ", ".join(str(v) for v in valores.mode()),
        "minimo": valores.min(), "maximo": valores.max(),
        "Q1_25%": valores.quantile(0.25),
        "Q2_50%": valores.quantile(0.50),
        "Q3_75%": valores.quantile(0.75),
    })


campos_cliente = ["CL_GENERO", "CL_EC", "CL_FHL", "CL_SEG"]
consistencia_clientes = df_limpo.groupby("CL_ID")[campos_cliente].nunique(dropna=False)
if consistencia_clientes.gt(1).any().any():
    raise ValueError("Há perfis divergentes do mesmo cliente. Revise antes de selecionar um perfil.")
clientes = df_limpo[["CL_ID"] + campos_cliente].drop_duplicates("CL_ID")
estatisticas_filhos = pd.DataFrame({
    "por_registro_limpo": estatisticas(df_limpo["CL_FHL"]),
    "por_cliente_unico": estatisticas(clientes["CL_FHL"]),
})
print(estatisticas_filhos.to_string())

# %% [markdown]
# ## 7. Agrupamentos
# `groupby` separa os grupos; `size` conta linhas e `nunique` conta códigos
# distintos. Comparamos compras, não receita. Uma compra pode conter várias
# categorias, portanto não se somam contagens de compras entre categorias.

# %%
total_compras = df_limpo["CO_ID"].nunique()
por_categoria = df_limpo.groupby("PR_CAT").agg(
    registros_limpos=("PR_ID", "size"),
    compras_distintas=("CO_ID", "nunique"),
    clientes_distintos=("CL_ID", "nunique"),
).sort_values("compras_distintas", ascending=False)
por_categoria["presenca_em_compras_pct"] = (
    por_categoria["compras_distintas"] / total_compras * 100).round(2)

# Uma linha por compra para evitar contá-la uma vez por produto.
compras = df_limpo[["CO_ID", "DATA", "CL_ID", "CL_GENERO", "CL_SEG"]].drop_duplicates("CO_ID")
por_genero = compras.groupby("CL_GENERO").agg(
    compras_distintas=("CO_ID", "nunique"), clientes_distintos=("CL_ID", "nunique"))
por_genero["compras_por_cliente"] = (
    por_genero["compras_distintas"] / por_genero["clientes_distintos"]).round(2)

# Duas combinações explícitas de variáveis, como solicita a rubrica.
por_categoria_genero = df_limpo.groupby(["PR_CAT", "CL_GENERO"]).agg(
    compras_distintas=("CO_ID", "nunique"), registros_limpos=("PR_ID", "size"))
por_segmento_genero = compras.groupby(["CL_SEG", "CL_GENERO"]).agg(
    compras_distintas=("CO_ID", "nunique"), clientes_distintos=("CL_ID", "nunique"))

compras["MES"] = compras["DATA"].dt.to_period("M").astype(str)
por_mes = compras.groupby("MES").agg(compras_distintas=("CO_ID", "nunique"))
print("\nPOR CATEGORIA:\n", por_categoria.to_string())
print("\nPOR GENERO:\n", por_genero.to_string())
print("\nCATEGORIA E GENERO:\n", por_categoria_genero.to_string())
print("\nSEGMENTO E GENERO:\n", por_segmento_genero.to_string())
print("\nPOR MES:\n", por_mes.to_string())

# %% [markdown]
# ## 8. Conclusões e exportação
# Os tópicos abaixo são gerados com os resultados executados, sem números fixos.
# As limitações fazem parte da análise: não há dados para faturamento e não
# podemos extrapolar este recorte para todo o varejo ou inferir causalidade.

# %%
categoria_lider = por_categoria.index[0]
genero_lider = por_genero["compras_distintas"].idxmax()
mes_lider = por_mes["compras_distintas"].idxmax()
media_filhos = float(clientes["CL_FHL"].mean())
moda_filhos = ", ".join(str(v) for v in clientes["CL_FHL"].mode())
conclusoes = [
    f"A base passou de {len(df_bruto):,} para {len(df_limpo):,} registros; "
    f"foram separadas {len(duplicatas_removidas):,} repetições exatas e "
    f"{len(registros_invalidos):,} linhas por identificador/data.",
    f"O recorte contém {total_compras:,} compras e {len(clientes):,} clientes, "
    f"de {df_limpo['DATA'].min():%d/%m/%Y} a {df_limpo['DATA'].max():%d/%m/%Y}, "
    "adotando dia/mês/ano. A descrição geral do dataset não substitui o período observado.",
    f"{categoria_lider} aparece em {int(por_categoria.loc[categoria_lider, 'compras_distintas']):,} "
    f"compras ({por_categoria.loc[categoria_lider, 'presenca_em_compras_pct']:.2f}% do total). "
    "As participações de categorias podem somar mais de 100%.",
    f"O grupo {genero_lider} tem mais compras neste recorte: "
    f"{int(por_genero.loc[genero_lider, 'compras_distintas']):,}. "
    "A tabela também informa compras por cliente, para considerar o tamanho dos grupos.",
    f"Nos clientes únicos, a média de filhos é {media_filhos:.3f} e a moda é {moda_filhos}. "
    f"O mês com mais compras é {mes_lider}, com {int(por_mes.loc[mes_lider, 'compras_distintas']):,}; "
    "isso não demonstra sazonalidade em uma amostra de cobertura não confirmada.",
    f"Há {int(df_limpo['PR_CAT'].eq('Sem Categoria').sum()):,} registros limpos sem categoria. "
    "Sem preços, quantidades e confirmação da origem das repetições, "
    "não estimamos faturamento nem unidades vendidas. Não há colunas de dimensões físicas.",
]
relatorio = "# Conclusões da análise\n\n" + "\n\n".join("- " + c for c in conclusoes) + "\n"
print("\n" + relatorio)

qualidade = pd.concat([nulos_antes.rename("nulos_na_leitura"),
                       nulos_reconhecidos.rename("nulos_apos_reconhecer_marcadores"),
                       df_limpo.isna().sum().rename("nulos_finais")], axis=1)
tabelas = {
    "qualidade_dados": qualidade, "estatisticas_filhos": estatisticas_filhos,
    "por_categoria": por_categoria, "por_genero": por_genero,
    "por_categoria_genero": por_categoria_genero,
    "por_segmento_genero": por_segmento_genero, "por_mes": por_mes,
}
for nome, tabela in tabelas.items():
    tabela.to_csv(SAIDA / f"{nome}.csv", sep=";", encoding="utf-8-sig")

df_limpo.to_csv(SAIDA / "df_limpo.csv.gz", sep=";", index=False,
                encoding="utf-8", compression="gzip", date_format="%Y-%m-%d")
duplicatas_removidas.to_csv(SAIDA / "duplicatas_removidas.csv.gz", sep=";",
                           index=False, encoding="utf-8", compression="gzip")
registros_invalidos.to_csv(SAIDA / "registros_invalidos.csv", sep=";",
                          index=False, encoding="utf-8-sig")
(SAIDA / "conclusoes.md").write_text(relatorio, encoding="utf-8")
print("Resultados salvos na pasta resultados.")
