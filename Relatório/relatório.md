# Relatório — Análise de Criminalidade no Ceará

**Disciplina:** Introdução à Análise de Dados  
**Tema:** Criminalidade no Ceará — SSPDS-CE  
**Data de entrega:** 04 de junho de 2026  
**Integrantes:** Flávio, Paulo Henrique, Kaio Vitor, Henrique Gabriel

---

## 1. Motivação

O Ceará é um dos estados brasileiros que mais investe em transparência de dados de segurança pública, disponibilizando informações detalhadas por município, tipo de crime, perfil de vítima e período. Isso torna o estado um laboratório valioso para análise de dados reais com impacto social.

Nosso grupo escolheu esse tema por dois motivos principais: primeiro, porque os dados são públicos, detalhados e bem documentados; segundo, porque entender padrões de criminalidade é essencial para qualquer debate informado sobre políticas de segurança pública.

Queríamos responder perguntas como: *Onde os crimes acontecem mais? Quem são as vítimas? A situação está melhorando ou piorando ao longo dos anos? Existe sazonalidade nos crimes?*

---

## 2. Fonte dos Dados

| Item | Descrição |
|------|-----------|
| **Órgão** | SUPESP — Superintendência de Pesquisa e Estratégia de Segurança Pública |
| **Portal** | https://www.sspds.ce.gov.br/estatisticas-2/ |
| **Período** | 2021 a 2023 |
| **Formato original** | Planilhas `.xlsx` e `.csv` convertidas para `.csv` separado por ano |

### Conjuntos de dados utilizados

| Tabela | Descrição | Total de registros |
|--------|-----------|-------------------|
| `cvli` | Crimes Violentos Letais e Intencionais | 9.239 |
| `cvp` | Crimes Violentos contra o Patrimônio | 136.678 |
| `intervencao_policial` | Mortes por intervenção policial | 424 |

### Principais colunas

| Coluna | Descrição |
|--------|-----------|
| `municipio` | Município onde ocorreu o crime |
| `ais` | Área Integrada de Segurança |
| `natureza` | Tipo do crime (ex: Homicídio Doloso, Feminicídio) |
| `data` / `hora` | Data e hora da ocorrência |
| `dia_semana` | Dia da semana |
| `meio_empregado` | Arma ou meio utilizado |
| `genero` | Gênero da vítima |
| `idade_vitima` | Idade da vítima |
| `escolaridade_vitima` | Escolaridade da vítima |
| `raca_vitima` | Raça/Cor da vítima |

### Limitações encontradas

- A coluna `raca_vitima` apresentou alto índice de "Não Informada" (64,3% dos casos), o que limita análises de vitimização racial com precisão absoluta.
- O CVP não possui colunas de perfil de vítima (apenas localização e data), impossibilitando análises demográficas para crimes patrimoniais.
- A tabela `Unidade_Prisional` do arquivo original continha apenas 4 registros e foi descartada por ser insuficiente para análise.

---

## 3. Decisões de Modelagem

Optamos por criar **três tabelas separadas**:

- **`cvli`** — crimes letais, com perfil detalhado de vítima
- **`cvp`** — crimes patrimoniais, com dados de localização e período
- **`intervencao_policial`** — mortes por ação policial, para comparação com CVLIs

Essa separação foi escolhida porque os três conjuntos têm estruturas de colunas diferentes e dinâmicas distintas de análise. Juntar tudo em uma tabela geraria muitas colunas nulas.

As colunas `ano` e `mes` foram geradas automaticamente a partir da coluna `data` usando colunas computadas (`GENERATED ALWAYS AS`), evitando redundância e garantindo consistência.

Índices foram criados nas colunas `municipio`, `natureza`, `data`, `genero` e `raca_vitima` para acelerar as consultas analíticas.

---

## 4. Tratamento dos Dados

| Problema encontrado | Como foi resolvido |
|--------------------|-------------------|
| Espaços extras no início/fim dos textos | `TRIM()` em todas as colunas de texto |
| Gênero com grafias inconsistentes ("M", "MASC", "Masculino") | Padronização com `CASE` + `UPPER()` |
| Valores `NULL` em `faixa_etaria`, `raca_vitima`, `escolaridade` | Substituídos por `'Não Informada'` |
| Valores `NULL` em `ais` | Substituídos por `'Não Identificada'` |
| Linhas sem município | Removidas com `DELETE` |
| Erro no script: `DELETE FROM cvli WHERE municipio OR TRIM...` | Corrigido para `WHERE municipio IS NULL OR TRIM(municipio) = ''` |

---

## 5. Perguntas Respondidas

### Pergunta 1 — Quais os 10 municípios com mais CVLIs no período?

```sql
SELECT municipio, COUNT(*) AS total_cvli
FROM cvli
GROUP BY municipio
ORDER BY total_cvli DESC
LIMIT 10;
```

| # | Município | Total CVLI |
|---|-----------|-----------|
| 1 | Fortaleza | 2.488 |
| 2 | Caucaia | 691 |
| 3 | Maracanaú | 410 |
| 4 | Sobral | 245 |
| 5 | Juazeiro do Norte | 222 |
| 6 | Aquiraz | 182 |
| 7 | Cascavel | 168 |
| 8 | Maranguape | 155 |
| 9 | Pacatuba | 142 |
| 10 | Horizonte | 137 |

**Interpretação:** Fortaleza lidera com 2.488 casos — mais de 3 vezes o segundo colocado (Caucaia, 691). Os municípios do Top 10 são predominantemente da Região Metropolitana de Fortaleza, o que indica que a violência letal está fortemente concentrada no entorno da capital. Municípios como Sobral e Juazeiro do Norte, polos do interior, também aparecem, refletindo sua importância regional e possível influência do crime organizado fora da RMF.

---

### Pergunta 2 — Como evoluiu o número de CVLIs e CVPs por ano?

```sql
SELECT ano, COUNT(*) AS total_cvli FROM cvli GROUP BY ano ORDER BY ano;
SELECT ano, COUNT(*) AS total_cvp  FROM cvp  GROUP BY ano ORDER BY ano;
```

**CVLI por ano:**

| Ano | Total |
|-----|-------|
| 2021 | 3.299 |
| 2022 | 2.970 |
| 2023 | 2.970 |

**CVP por ano:**

| Ano | Total |
|-----|-------|
| 2021 | 48.141 |
| 2022 | 45.930 |
| 2023 | 42.607 |

**Interpretação:** Ambos os indicadores mostram uma tendência de **queda consistente** ao longo do período. Os CVLIs reduziram 10% entre 2021 e 2023, enquanto os CVPs caíram aproximadamente 11,5%. Essa redução simultânea em crimes letais e patrimoniais sugere um efeito positivo das políticas de segurança pública implementadas no estado, como o Pacto por um Ceará Pacífico. Vale destacar que 2022 e 2023 apresentaram exatamente o mesmo número de CVLIs (2.970), indicando uma estabilização após a queda inicial.

---

### Pergunta 3 — Qual o tipo de crime mais frequente por ano?

```sql
SELECT ano, natureza, COUNT(*) AS total
FROM cvli
GROUP BY ano, natureza
ORDER BY ano, total DESC;
```

| Ano | Natureza | Total |
|-----|----------|-------|
| 2021 | Homicídio Doloso | 3.202 |
| 2021 | Roubo Seguido de Morte (Latrocínio) | 43 |
| 2021 | Feminicídio | 31 |
| 2021 | Lesão Corporal Seguida de Morte | 23 |
| 2022 | Homicídio Doloso | 2.881 |
| 2022 | Roubo Seguido de Morte (Latrocínio) | 44 |
| 2022 | Feminicídio | 29 |
| 2022 | Lesão Corporal Seguida de Morte | 16 |
| 2023 | Homicídio Doloso | 2.893 |
| 2023 | Feminicídio | 42 |
| 2023 | Roubo Seguido de Morte (Latrocínio) | 24 |
| 2023 | Lesão Corporal Seguida de Morte | 11 |

**Interpretação:** O Homicídio Doloso domina absolutamente os CVLIs nos três anos, representando mais de 97% dos casos. Um dado preocupante é o aumento do **Feminicídio** em 2023 (42 casos), superando o Latrocínio e chegando ao maior valor do período — um alerta para a necessidade de políticas específicas de proteção à mulher. O Latrocínio e a Lesão Corporal Seguida de Morte apresentaram queda, o que é positivo.

---

### Pergunta 4 — Qual o perfil das vítimas de CVLI por gênero e raça?

```sql
SELECT genero, raca_vitima,
       COUNT(*) AS total,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS percentual
FROM cvli
GROUP BY genero, raca_vitima
ORDER BY total DESC;
```

| Gênero | Raça/Cor | Total | % |
|--------|----------|-------|---|
| Masculino | Não Informada | 5.937 | 64,3% |
| Masculino | Parda | 1.986 | 21,5% |
| Feminino | Não Informada | 629 | 6,8% |
| Masculino | Branca | 303 | 3,3% |
| Feminino | Parda | 199 | 2,2% |
| Masculino | Preta | 120 | 1,3% |
| Feminino | Branca | 38 | 0,4% |
| Feminino | Preta | 12 | 0,1% |
| Masculino | Indígena | 7 | 0,1% |
| Masculino | Amarela | 6 | 0,1% |
| Feminino | Indígena | 2 | 0,0% |

**Interpretação:** As vítimas são esmagadoramente do **sexo masculino** (cerca de 91% dos casos). O alto índice de raça "Não Informada" (71,1% do total) limita a análise racial, mas entre os casos informados, pessoas **pardas e pretas** representam a maioria das vítimas — padrão consistente com as estatísticas nacionais de violência. Esse dado reforça a urgência de políticas de segurança com recorte racial. As mulheres representam cerca de 9% das vítimas de CVLI, mas merecem atenção especial pelo crescimento do feminicídio observado na Pergunta 3.

---

### Pergunta 5 — Em quais meses ocorrem mais crimes? (sazonalidade)

```sql
SELECT mes, TO_CHAR(TO_DATE(mes::TEXT, 'MM'), 'TMMonth') AS nome_mes,
       COUNT(*) AS total_cvli
FROM cvli GROUP BY mes ORDER BY mes;
```

**CVLI — sazonalidade mensal:**

| Mês | Total CVLI | Mês | Total CVP |
|-----|-----------|-----|----------|
| Janeiro | 809 | Janeiro | 12.654 |
| Fevereiro | 777 | Fevereiro | 11.523 |
| Março | 703 | Março | 11.160 |
| Abril | 736 | Abril | 10.952 |
| Maio | 742 | Maio | 11.659 |
| Junho | 700 | Junho | 10.850 |
| Julho | 762 | Julho | 11.517 |
| Agosto | 786 | Agosto | 11.784 |
| Setembro | 791 | Setembro | 11.187 |
| Outubro | 840 | Outubro | 11.423 |
| Novembro | 807 | Novembro | 11.103 |
| Dezembro | 786 | Dezembro | 10.866 |

**Interpretação:** Os CVLIs têm **outubro como mês de pico** (840 casos) e **junho como mínimo** (700). Curiosamente, o padrão é relativamente estável ao longo do ano, sem pico tão pronunciado quanto se esperaria no verão. Já os CVPs têm **janeiro como mês mais crítico** (12.654 casos), possivelmente associado ao período de férias com mais pessoas nas ruas e maior movimentação de valores. O segundo semestre concentra levemente mais crimes patrimoniais que o primeiro.

---

### Pergunta 6 — Quais municípios concentram mais CVPs e como se comparam com CVLIs?

```sql
SELECT cvp.municipio,
       COUNT(DISTINCT cvp.id) AS total_cvp,
       COUNT(DISTINCT cvli.id) AS total_cvli
FROM cvp
LEFT JOIN cvli ON LOWER(TRIM(cvp.municipio)) = LOWER(TRIM(cvli.municipio))
              AND cvp.ano = cvli.ano
GROUP BY cvp.municipio
ORDER BY total_cvp DESC
LIMIT 15;
```

| # | Município | CVP | CVLI |
|---|-----------|-----|------|
| 1 | Fortaleza | 92.312 | 2.488 |
| 2 | Caucaia | 7.277 | 691 |
| 3 | Maracanaú | 5.148 | 410 |
| 4 | Sobral | 3.999 | 245 |
| 5 | Juazeiro do Norte | 3.812 | 222 |
| 6 | Pacajus | 1.986 | 112 |
| 7 | Horizonte | 1.859 | 137 |
| 8 | Aquiraz | 1.189 | 182 |
| 9 | Maranguape | 1.014 | 155 |
| 10 | Eusébio | 1.003 | 58 |
| 11 | Crato | 960 | 120 |
| 12 | Cascavel | 894 | 168 |
| 13 | Itaitinga | 723 | 79 |
| 14 | Pacatuba | 640 | 142 |
| 15 | Tianguá | 528 | 103 |

**Interpretação:** Fortaleza é absolutamente dominante nos dois indicadores, com 92.312 CVPs — mais de 12 vezes o segundo colocado (Caucaia, 7.277). A concentração de CVP e CVLI nos mesmos municípios da Região Metropolitana confirma que essas cidades enfrentam um desafio amplo de segurança pública, não restrito a um único tipo de crime. Municípios como Eusébio e Pacajus se destacam por ter CVP relativamente alto em relação ao seu CVLI, indicando perfil mais patrimonial que violento.

---

### Pergunta 7 — Qual o meio mais usado nos CVLIs e qual a proporção de mortes por intervenção policial?

```sql
SELECT ano, meio_empregado, COUNT(*) AS total
FROM cvli GROUP BY ano, meio_empregado ORDER BY ano, total DESC;
```

| Ano | Meio Empregado | Total |
|-----|---------------|-------|
| 2021 | Arma de fogo | 2.842 |
| 2021 | Arma branca | 269 |
| 2021 | Outros meios | 188 |
| 2022 | Arma de fogo | 2.518 |
| 2022 | Arma branca | 284 |
| 2022 | Outros meios | 168 |
| 2023 | Arma de fogo | 2.553 |
| 2023 | Arma branca | 245 |
| 2023 | Outros meios | 172 |

**Interpretação:** A **arma de fogo** é o meio dominante em todos os anos, responsável por mais de 86% dos CVLIs. Houve uma queda de 2021 para 2022 (-324 casos com arma de fogo), mas uma leve recuperação em 2023 (+35). Isso reforça a necessidade de políticas de controle de armas de fogo como estratégia central de redução da violência letal. A arma branca e outros meios mantêm participação relativamente estável e pequena.

---

## 6. Visualizações

> *<img width="1844" height="506" alt="image" src="https://github.com/user-attachments/assets/68563506-db95-4100-b09b-dee4cbda2815" />
<img width="888" height="618" alt="image" src="https://github.com/user-attachments/assets/88eecb96-e66c-493c-a2e7-9b489039e994" />
<img width="895" height="625" alt="image" src="https://github.com/user-attachments/assets/58db1110-4562-44ae-9d57-c10ab780da16" />
<img width="897" height="640" alt="image" src="https://github.com/user-attachments/assets/b5b81f8d-f3b7-41b6-bc6e-4d36fabdbe7c" />
<img width="877" height="599" alt="image" src="https://github.com/user-attachments/assets/09f0766d-261e-4f82-8d2d-3793daca77a8" />
<img width="900" height="629" alt="image" src="https://github.com/user-attachments/assets/25c3b91c-b606-44dc-b49e-c66471ad0e3b" />
<img width="869" height="592" alt="image" src="https://github.com/user-attachments/assets/aa6f2c2b-a3dc-40ae-92d9-7a5b5d8d3aae" />
*

O dashboard foi desenvolvido em Python com as bibliotecas **Plotly** e **Dash**, rodando localmente em `http://localhost:8050`. Os seguintes gráficos foram produzidos:

- **KPIs no topo:** totais de CVLI, CVP e Intervenção Policial com filtro por ano
- **Gráfico de barras agrupadas:** evolução anual de CVLI e CVP lado a lado
- **Gráfico de barras:** tipos de natureza dos CVLIs
- **Gráfico de barras horizontal:** Top 10 municípios com mais CVLIs
- **Gráfico de linhas:** sazonalidade mensal de CVLI e CVP
- **Gráfico de pizza:** perfil das vítimas por gênero
- **Gráfico de barras:** perfil das vítimas por raça/cor

Adicionalmente, gráficos estáticos em PNG foram gerados com **Matplotlib** e **Seaborn** para inserção neste relatório.

---

## 7. Conclusão

A análise dos dados do SSPDS-CE revelou padrões claros e relevantes sobre a criminalidade no Ceará entre 2021 e 2023.

**Positivo:** ambos os indicadores — CVLI e CVP — apresentaram **tendência de queda** no período, com reduções de 10% e 11,5% respectivamente, sugerindo avanços nas políticas de segurança pública do estado.

**Preocupante:** o **Feminicídio aumentou em 2023** (42 casos), atingindo o maior valor do triênio e superando o Latrocínio pela primeira vez. Isso exige atenção específica de políticas de proteção à mulher.

**Estrutural:** a violência no Ceará é fortemente **concentrada geograficamente** — a Região Metropolitana de Fortaleza, e especialmente a capital, responde pela maior parte das ocorrências nos dois tipos de crime. O perfil das vítimas de crimes letais é predominantemente **masculino**, e entre os casos com raça informada, **pardos e pretos** são a maioria absoluta.

**Metodológico:** a arma de fogo é o instrumento em mais de 86% dos CVLIs, dado que orienta diretamente qualquer política de desarmamento ou controle de armas no estado.

Este trabalho demonstrou como dados públicos, tratados com SQL e visualizados com Python, podem transformar números brutos em insights acionáveis para gestores, pesquisadores e a sociedade civil.
