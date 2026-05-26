-- ============================================================
-- 04_consultas.sql
-- Consultas analíticas — 7 perguntas com interpretação
-- Projeto: Análise de Criminalidade no Ceará (SSPDS-CE)
-- ============================================================


-- ============================================================
-- PERGUNTA 1:
-- Quais foram os 10 municípios com mais crimes violentos
-- letais e intencionais (CVLI) em 2023?
-- ============================================================
-- Por que é importante: identifica os municípios mais críticos
-- e orienta políticas de segurança pública.

SELECT
    municipio,
    SUM(quantidade) AS total_cvli
FROM ocorrencias_cvli
WHERE ano = 2023
GROUP BY municipio
ORDER BY total_cvli DESC
LIMIT 10;

-- Interpretação esperada: Fortaleza tende a liderar pelo porte
-- populacional. Municípios do interior com alta incidência
-- podem indicar expansão do crime organizado.


-- ============================================================
-- PERGUNTA 2:
-- Como evoluiu o número total de CVLIs por ano?
-- (tendência temporal)
-- ============================================================
-- Por que é importante: revela se a criminalidade está
-- aumentando, diminuindo ou estável ao longo dos anos.

SELECT
    ano,
    SUM(quantidade) AS total_cvli
FROM ocorrencias_cvli
GROUP BY ano
ORDER BY ano;

-- Interpretação: uma queda consistente pode indicar sucesso
-- de políticas públicas. Picos em anos específicos podem
-- coincidir com crises ou disputas entre facções.


-- ============================================================
-- PERGUNTA 3:
-- Qual o tipo de crime mais frequente em cada ano?
-- ============================================================
-- Por que é importante: entender qual modalidade criminosa
-- predomina ajuda a direcionar o tipo de ação policial.

SELECT
    ano,
    tipo_crime,
    SUM(quantidade) AS total
FROM ocorrencias_cvli
GROUP BY ano, tipo_crime
ORDER BY ano, total DESC;

-- Dica: para ver só o "campeão" de cada ano, você pode
-- envolver essa query numa subquery com DISTINCT ON (ano).


-- ============================================================
-- PERGUNTA 4:
-- Qual é o perfil das vítimas de CVLI por sexo e raça/cor?
-- ============================================================
-- Por que é importante: dados de vitimização revelam
-- desigualdades estruturais que precisam de atenção.

SELECT
    sexo_vitima,
    raca_cor,
    SUM(quantidade)                              AS total,
    ROUND(
        100.0 * SUM(quantidade)
        / SUM(SUM(quantidade)) OVER ()
    , 1)                                         AS percentual
FROM ocorrencias_cvli
GROUP BY sexo_vitima, raca_cor
ORDER BY total DESC;

-- Interpretação: no contexto brasileiro, espera-se alta
-- concentração de vítimas do sexo masculino e negras.
-- Esse dado é fundamental para políticas de justiça racial.


-- ============================================================
-- PERGUNTA 5:
-- Em quais meses do ano ocorrem mais crimes? (sazonalidade)
-- ============================================================
-- Por que é importante: identificar picos sazonais permite
-- escalar efetivo policial em períodos críticos.

SELECT
    mes,
    nome_mes,
    SUM(quantidade)                           AS total_cvli,
    ROUND(AVG(quantidade), 1)                 AS media_por_ocorrencia
FROM ocorrencias_cvli
GROUP BY mes, nome_mes
ORDER BY mes;

-- Interpretação: meses de férias e festas (janeiro, julho,
-- dezembro) costumam registrar variações. Compare com CVP
-- para ver se o padrão é o mesmo.


-- ============================================================
-- PERGUNTA 6:
-- Comparação entre CVLI e CVP por município — quais
-- municípios têm mais crimes contra a vida E contra o patrimônio?
-- ============================================================
-- Por que é importante: municípios com alta incidência nos dois
-- indicadores são os que mais precisam de intervenção ampla.
-- Esta query usa JOIN para combinar as duas tabelas.

SELECT
    cvli.municipio,
    SUM(cvli.quantidade) AS total_cvli,
    SUM(cvp.quantidade)  AS total_cvp,
    SUM(cvli.quantidade) + SUM(cvp.quantidade) AS total_geral
FROM ocorrencias_cvli cvli
JOIN ocorrencias_cvp  cvp
  ON LOWER(cvli.municipio) = LOWER(cvp.municipio)
 AND cvli.ano = cvp.ano
GROUP BY cvli.municipio
ORDER BY total_geral DESC
LIMIT 15;

-- Interpretação: municípios no topo desta lista são "pontos
-- quentes" que concentram múltiplos tipos de violência.


-- ============================================================
-- PERGUNTA 7:
-- Qual a variação percentual de CVLIs entre 2022 e 2023
-- por município? (quem melhorou e quem piorou)
-- ============================================================
-- Por que é importante: uma análise de evolução relativa
-- mostra quais municípios estão progredindo ou regredindo.

WITH por_ano AS (
    SELECT
        municipio,
        SUM(quantidade) FILTER (WHERE ano = 2022) AS total_2022,
        SUM(quantidade) FILTER (WHERE ano = 2023) AS total_2023
    FROM ocorrencias_cvli
    WHERE ano IN (2022, 2023)
    GROUP BY municipio
)
SELECT
    municipio,
    total_2022,
    total_2023,
    ROUND(
        100.0 * (total_2023 - total_2022) / NULLIF(total_2022, 0)
    , 1) AS variacao_percentual,
    CASE
        WHEN total_2023 < total_2022 THEN '📉 Reduziu'
        WHEN total_2023 > total_2022 THEN '📈 Aumentou'
        ELSE '➡️  Estável'
    END AS tendencia
FROM por_ano
WHERE total_2022 IS NOT NULL AND total_2023 IS NOT NULL
ORDER BY variacao_percentual ASC;  -- piores resultados aparecem por último

-- Interpretação: municípios com maior redução percentual são
-- casos de sucesso. Os com maior aumento merecem atenção urgente.
