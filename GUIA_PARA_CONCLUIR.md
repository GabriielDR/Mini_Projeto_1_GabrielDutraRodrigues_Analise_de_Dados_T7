# Como concluir o mini-projeto e entender o essencial

Esta versão contém código executado sobre a base indicada no enunciado. Falta você identificar o trabalho, executar no seu ambiente, revisar os resultados e publicar no seu GitHub. O enunciado enviado menciona 26/10 às 22h; foi considerado o prazo atualizado de 29/10 informado por você. Confira o prazo no AVA.

## 1. Prepare os arquivos

Baixe e extraia `Mini_Projeto_Varejo.zip`. Dentro dele, a pasta `mini_projeto_varejo` contém código, notebook, dados comprimidos, README e resultados. Não é necessário baixar a base novamente.

Para começar, concentre-se em três arquivos:

- `Mini_Projeto_Varejo.ipynb`: código dividido em blocos, com explicações e resultados de referência.
- `dados/Base_Varejo.csv.gz`: base original comprimida, sem alterações de conteúdo.
- `README.md`: descrição do trabalho e decisões da análise.

## 2. Crie o repositório no início do seu trabalho

No GitHub, crie um repositório público com o padrão exigido, substituindo os campos:

`Miniprojeto_SeuNome_Analise_de_Dados_T7`

O cabeçalho indica T7, mas um exemplo no enunciado usa T1: confirme a sua turma antes de nomear. Comece com um README curto que apresente o objetivo e a fonte da base. Registre esse primeiro passo com uma mensagem como `Inicia projeto e documenta fonte dos dados`.

O histórico precisa acompanhar o trabalho real que você fará: preparação, execução, revisão e documentação. Não é necessário simular dias anteriores nem criar datas artificiais.

## 3. Execute no Google Colab

O Colab permite trabalhar no navegador sem instalar Python. Se você já tem o VS Code configurado e prefere usá-lo, siga a alternativa abaixo.

1. Acesse <https://colab.research.google.com/> e abra/envie `Mini_Projeto_Varejo.ipynb`.
2. Edite a primeira célula de texto com seu nome e turma.
3. No painel de arquivos, envie `Base_Varejo.csv.gz`, que está na pasta `dados` do pacote. Não precisa descomprimir o `.gz`.
4. Execute uma célula de código por vez, de cima para baixo, pelo botão de executar ou com **Shift + Enter**.
5. Antes de cada execução, leia o texto que apresenta o bloco. Após executar, compare a saída com a explicação.
6. Ao terminar a célula 8, use a célula opcional de download para obter um ZIP dos resultados.
7. Baixe/salve o notebook com suas alterações e as saídas da execução. Arquivos enviados para a sessão do Colab não ficam garantidamente disponíveis depois que a sessão termina.

Se aparecer `FileNotFoundError`, confira o nome e o envio da base. O código aceita `Base_Varejo.csv.gz`, `Base Varejo.csv` ou `Varejo.csv`, nos locais descritos na primeira célula. Se aparecer outro erro, copie a mensagem completa para que possamos corrigi-lo.

## 4. Entenda estas seis ideias antes da entrega

| Ideia | Neste projeto |
|---|---|
| DataFrame | Uma tabela em memória, chamada `df` no código. |
| Tipo de dado | Data precisa virar data; número de filhos precisa virar inteiro; identificadores podem ficar como texto. |
| Ausente não é zero | `#N/D` significa informação indisponível; zero filhos significa que a informação conhecida é zero. |
| Linha não é compra | A mesma compra aparece em várias linhas, uma para cada registro de produto. `nunique()` conta os códigos de compra distintos. |
| Duplicata exige contexto | Duas linhas idênticas podem ser erro ou repetição de unidades. Aqui a base limpa serve para presença de produtos por compra, sem estimar unidades vendidas. |
| Unidade da estatística | Para conhecer o perfil dos clientes, conte cada cliente uma vez. A estatística por linha também é fornecida para atender ao enunciado. |

Não é necessário dominar cada detalhe de sintaxe hoje. Priorize explicar o que entra em cada bloco, o que ele modifica e por que essa escolha faz sentido.

## 5. Confira os resultados de referência

- Leitura: **830.000 linhas e 14 colunas**.
- Colunas sem nome e vazias removidas: **4**.
- Ausências textuais `#N/D`: **3.650 em PR_CAT e 3.650 em PR_NOME**, nas mesmas linhas.
- Repetições exatas separadas: **96.553**; registros limpos: **733.447**.
- Compras distintas: **18.471**; clientes distintos: **1.000**.
- Média de filhos por cliente único: **1,136**; moda: **0**.

Esses valores se referem exatamente ao arquivo fornecido no pacote. O código calcula os resultados; os números não são usados como entrada para fabricar saídas.

## 6. Complete a documentação e faça os próximos commits

Depois de executar e compreender importação e limpeza, registre o código e a base comprimida, por exemplo com `Implementa importacao e limpeza da base`.

Após revisar as estatísticas e agrupamentos, registre a versão executada e os resultados, por exemplo com `Adiciona estatisticas e agrupamentos validados`.

Por fim, revise o README com suas próprias palavras, identifique aluno e turma e registre a documentação final, por exemplo com `Documenta conclusoes e decisoes de qualidade dos dados`.

Você pode enviar arquivos pelo menu **Add file > Upload files** do repositório. Mantenha a estrutura das pastas e não envie apenas o ZIP do projeto. Os dados foram comprimidos porque o CSV original tem cerca de 49 MB e o envio pelo navegador aceita até 25 MiB por arquivo; cada `.gz` deste projeto cabe nesse limite.

Antes de enviar o link no AVA:

- [ ] Nome e turma preenchidos no notebook e nos READMEs.
- [ ] `README_SEU_NOME_SUA_TURMA.md` renomeado com seus dados.
- [ ] Repositório público com o padrão de nome solicitado.
- [ ] Código comentado e notebook executado, sem erros.
- [ ] Base de entrada, `requirements.txt` e resultados presentes, incluindo `df_limpo.csv.gz`.
- [ ] README com reflexão sobre ETL, qualidade de dados e seis conclusões.
- [ ] Histórico com os passos efetivamente realizados durante sua revisão.
- [ ] Link do repositório acessível fora da sua conta e enviado na atividade correta.

## Pontos do enunciado que precisam de interpretação

**Regra do número da compra:** não foi informado comprimento obrigatório, faixa ou dígito verificador. O projeto adota códigos numéricos positivos e verifica se cada compra se associa a uma única data e a um único cliente. Se o professor ensinou uma regra adicional em aula, ela deve ser acrescentada.

**Dimensões físicas:** a rubrica menciona nulos em dimensões físicas, mas esta base não tem peso, altura, largura ou outras medidas. Isso foi documentado; não foram criadas colunas artificiais.

**Datas:** adotou-se dia/mês/ano. As datas ambíguas não foram adivinhadas nem reordenadas pelo suposto calendário de vendas. As conclusões temporais dependem desse formato e da cobertura da amostra.

**Duplicatas:** foram separadas linhas inteiramente iguais, preservando os registros excedentes em arquivo. Não foi removida uma compra só porque seu identificador se repetia em produtos diferentes.

## Alternativa no VS Code

Abra a pasta extraída do projeto e execute no terminal:

```bash
python -m pip install -r requirements.txt
python mini_projeto_varejo.py
```

O notebook e o script possuem a mesma lógica principal. Você não precisa usar os dois ambientes.

## O que pode ficar para depois da entrega

Gráficos elaborados, dashboards, testes estatísticos, aprendizado de máquina, automação de download do Kaggle e detalhes avançados de Git. Nada disso foi exigido nos anexos enviados. O PDF que acompanha o dataset no Kaggle é de outra atividade e não substitui as instruções do seu curso.

## Documentação de apoio

- Colab: <https://research.google.com/colaboratory/faq.html>
- Leitura CSV com pandas: <https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html>
- Envio de arquivos ao GitHub: <https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository>
