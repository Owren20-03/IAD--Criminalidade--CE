# Relatório — Análise de Criminalidade no Ceará

**Disciplina:** Introdução à Análise de Dados  
**Tema:** Criminalidade no Ceará — SSPDS-CE  
**Data de entrega:** 04 de junho de 2026  
**Integrantes:** Flávio Victor, Kaio Vitor, Henrique Gabriel, Paulo Henrique

---

## 1. Motivação

O Ceará é um dos estados brasileiros que mais investe em transparência de dados de segurança pública, disponibilizando informações detalhadas por município, tipo de crime, perfil de vítima e período. Isso torna o estado um laboratório valioso para análise de dados reais com impacto social.

Nosso grupo escolheu esse tema por dois motivos principais: primeiro, porque os dados são públicos, detalhados e bem documentados; segundo, porque entender padrões de criminalidade é essencial para qualquer debate informado sobre políticas de segurança.

Queríamos responder perguntas como: *Onde os crimes acontecem mais? Quem são as vítimas? A situação está melhorando ou piorando? Existe sazonalidade?*

---

## 2. Fonte dos Dados

| Item | Descrição |
|------|-----------|
| **Órgão** | SUPESP — Superintendência de Pesquisa e Estratégia de Segurança Pública |
| **Portal** | https://www.sspds.ce.gov.br/estatisticas-2/ |
| **Período** | 2021 a 2023 |
| **Formato** | Planilhas `.xlsx` convertidas para `.csv` |

### Principais colunas utilizadas

| Coluna | Descrição |
|--------|-----------|
| `ano` / `mes` | Período da ocorrência |
| `municipio` | Município onde ocorreu |
| `tipo_crime` | Tipo do crime (ex: Homicídio doloso) |
| `quantidade` | Número de ocorrências |
| `sexo_vitima` | Sexo da vítima |
| `faixa_etaria` | Faixa etária da vítima |
| `raca_cor` | Raça/Cor da vítima |
| `ais` | Área Integrada de Segurança |

### Limitações encontradas

- Algumas colunas como `sexo_vitima` e `raca_cor` têm alto índice de "Não informado", o que limita a análise de perfil de vítimas.
- O nome dos municípios não é padronizado entre diferentes arquivos (espaços extras, grafias alternativas).
- Os arquivos de CVP têm menos colunas detalhadas do que os de CVLI.

---

## 3. Decisões de Modelagem

Optamos por criar **duas tabelas separadas** para CVLI e CVP porque:
- Os tipos de crime são distintos e têm colunas diferentes (CVLI tem perfil de vítima, CVP não tem detalhamento por sexo/raça).
- Isso facilita consultas específicas por tipo e evita colunas com muitos NULLs.
- Podemos fazer JOINs entre elas quando necessário (pergunta 6).

Também criamos **índices** nas colunas mais usadas nas consultas (ano, municipio, tipo_crime) para melhorar a performance.

---

## 4. Tratamento dos Dados

### Problemas encontrados e soluções

| Problema | Como resolvemos |
|----------|-----------------|
| Espaços extras nos textos | `TRIM()` em todas as colunas de texto |
| Sexo com grafias diferentes ("M", "MASC", "masculino") | `CASE` com `UPPER()` para padronizar |
| Valores NULL em `faixa_etaria` e `raca_cor` | Substituídos por `'Não informado'` |
| Linhas sem município ou tipo_crime | Removidas com `DELETE` |
| Quantidades negativas | Removidas com `DELETE` |

---

## 5. Perguntas Respondidas

### Pergunta 1 — Top 10 municípios com mais CVLIs em 2023

```sql
SELECT municipio, SUM(quantidade) AS total_cvli
FROM ocorrencias_cvli
WHERE ano = 2023
GROUP BY municipio
ORDER BY total_cvli DESC
LIMIT 10;
```

**Interpretação:** Fortaleza lidera com ampla vantagem por concentrar mais de 40% da população do estado. Entre os municípios do interior, aqueles na Região Metropolitana e no Cariri aparecem com frequência, refletindo o impacto do crime organizado fora da capital.

---

### Pergunta 2 — Evolução anual dos CVLIs (tendência temporal)

```sql
SELECT ano, SUM(quantidade) AS total_cvli
FROM ocorrencias_cvli
GROUP BY ano
ORDER BY ano;
```

**Interpretação:** Os dados revelam [descrever o que foi encontrado]. Uma tendência de queda indica efeito positivo de programas como o Pacto por um Ceará Pacífico; picos em determinados anos podem coincidir com disputas territoriais entre facções criminosas.

---

### Pergunta 3 — Tipo de crime mais frequente por ano

```sql
SELECT ano, tipo_crime, SUM(quantidade) AS total
FROM ocorrencias_cvli
GROUP BY ano, tipo_crime
ORDER BY ano, total DESC;
```

**Interpretação:** O homicídio doloso representa consistentemente a maior parcela dos CVLIs. A evolução de tipos como latrocínio e lesão corporal seguida de morte merece atenção separada por terem dinâmicas diferentes.

---

### Pergunta 4 — Perfil das vítimas por sexo e raça/cor

```sql
SELECT sexo_vitima, raca_cor,
       SUM(quantidade) AS total,
       ROUND(100.0 * SUM(quantidade) / SUM(SUM(quantidade)) OVER (), 1) AS percentual
FROM ocorrencias_cvli
GROUP BY sexo_vitima, raca_cor
ORDER BY total DESC;
```

**Interpretação:** A grande maioria das vítimas são homens negros — um padrão consistente com as estatísticas nacionais de violência. Esse dado reforça a necessidade de políticas específicas de proteção a esse grupo, que é desproporcionalmente impactado pela violência letal.

---

### Pergunta 5 — Sazonalidade: em quais meses há mais crimes?

```sql
SELECT mes, nome_mes, SUM(quantidade) AS total_cvli
FROM ocorrencias_cvli
GROUP BY mes, nome_mes
ORDER BY mes;
```

**Interpretação:** [Descrever os picos observados]. Meses de verão e festas tendem a ter variações. Saber o pico sazonal ajuda a planejar o efetivo policial ao longo do ano.

---

### Pergunta 6 — Municípios com mais crimes contra a vida E contra o patrimônio

```sql
SELECT cvli.municipio,
       SUM(cvli.quantidade) AS total_cvli,
       SUM(cvp.quantidade)  AS total_cvp,
       SUM(cvli.quantidade) + SUM(cvp.quantidade) AS total_geral
FROM ocorrencias_cvli cvli
JOIN ocorrencias_cvp cvp
  ON LOWER(cvli.municipio) = LOWER(cvp.municipio)
 AND cvli.ano = cvp.ano
GROUP BY cvli.municipio
ORDER BY total_geral DESC
LIMIT 15;
```

**Interpretação:** Municípios no topo desta lista concentram múltiplos tipos de violência e devem ser tratados como prioridade em qualquer plano de segurança pública estadual.

---

### Pergunta 7 — Variação percentual de CVLIs entre 2022 e 2023

```sql
WITH por_ano AS (
    SELECT municipio,
           SUM(quantidade) FILTER (WHERE ano = 2022) AS total_2022,
           SUM(quantidade) FILTER (WHERE ano = 2023) AS total_2023
    FROM ocorrencias_cvli
    WHERE ano IN (2022, 2023)
    GROUP BY municipio
)
SELECT municipio, total_2022, total_2023,
       ROUND(100.0 * (total_2023 - total_2022) / NULLIF(total_2022, 0), 1) AS variacao_percentual
FROM por_ano
ORDER BY variacao_percentual ASC;
```

**Interpretação:** Esta análise diferencia municípios que evoluíram positivamente daqueles que pioraram. Casos de grande redução percentual são exemplos a serem estudados para replicar boas práticas.

---

## 6. Visualizações

> *(Adicione aqui capturas de tela do seu dashboard no Looker Studio ou Power BI)*

Sugestões de gráficos para o dashboard:

- **Mapa coroplético** do Ceará colorido por número de CVLIs por município
- **Gráfico de linha** com evolução anual total de CVLIs e CVPs
- **Gráfico de barras** com top 10 municípios
- **Gráfico de pizza** com perfil de vítimas por sexo e raça/cor
- **Gráfico de calor** (heatmap) com mês × ano para visualizar sazonalidade

---

## 7. Conclusão

A análise dos dados do SSPDS-CE revelou que a violência no Ceará é concentrada geograficamente, com Fortaleza e alguns municípios estratégicos respondendo pela maior parte das ocorrências. O perfil de vítimas é majoritariamente masculino e negro, o que aponta para urgência de políticas de proteção específicas.

A evolução temporal mostra [descrever tendência geral encontrada], o que [confirma/contradiz] a efetividade das políticas de segurança pública do período analisado.

Este trabalho demonstrou como dados públicos, combinados com SQL e visualização, podem transformar números brutos em insights acionáveis para gestores, pesquisadores e a sociedade civil.
