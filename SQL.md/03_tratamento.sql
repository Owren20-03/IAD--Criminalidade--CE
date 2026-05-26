-- ============================================================
-- 03_tratamento.sql
-- Limpeza e transformações dos dados
-- Projeto: Análise de Criminalidade no Ceará (SSPDS-CE)
-- ============================================================

-- ------------------------------------------------------------
-- DIAGNÓSTICO: Entendendo os problemas antes de corrigir
-- ------------------------------------------------------------

-- 1. Verificar valores nulos por coluna (CVLI)
SELECT
    COUNT(*)                                        AS total_linhas,
    COUNT(*) FILTER (WHERE municipio IS NULL)       AS municipio_nulo,
    COUNT(*) FILTER (WHERE tipo_crime IS NULL)      AS tipo_crime_nulo,
    COUNT(*) FILTER (WHERE sexo_vitima IS NULL)     AS sexo_vitima_nulo,
    COUNT(*) FILTER (WHERE faixa_etaria IS NULL)    AS faixa_etaria_nulo,
    COUNT(*) FILTER (WHERE raca_cor IS NULL)        AS raca_cor_nulo,
    COUNT(*) FILTER (WHERE quantidade IS NULL)      AS quantidade_nulo
FROM ocorrencias_cvli;

-- 2. Verificar valores únicos de sexo (para achar inconsistências)
SELECT DISTINCT sexo_vitima, COUNT(*) AS qtd
FROM ocorrencias_cvli
GROUP BY sexo_vitima
ORDER BY qtd DESC;

-- 3. Verificar valores únicos de raça/cor
SELECT DISTINCT raca_cor, COUNT(*) AS qtd
FROM ocorrencias_cvli
GROUP BY raca_cor
ORDER BY qtd DESC;

-- 4. Verificar municípios que podem ter nome com espaços extras ou grafias diferentes
SELECT DISTINCT municipio
FROM ocorrencias_cvli
ORDER BY municipio;

-- ------------------------------------------------------------
-- LIMPEZA: Corrigindo os problemas encontrados
-- ------------------------------------------------------------

-- 5. Remover espaços extras no início/fim de texto em todas as colunas de texto
UPDATE ocorrencias_cvli
SET
    municipio    = TRIM(municipio),
    tipo_crime   = TRIM(tipo_crime),
    sexo_vitima  = TRIM(sexo_vitima),
    faixa_etaria = TRIM(faixa_etaria),
    raca_cor     = TRIM(raca_cor),
    ais          = TRIM(ais);

UPDATE ocorrencias_cvp
SET
    municipio  = TRIM(municipio),
    tipo_crime = TRIM(tipo_crime),
    ais        = TRIM(ais);

-- 6. Padronizar sexo para maiúsculas consistentes
-- (ex: "masculino", "MASCULINO", "M" → tudo vira "Masculino")
UPDATE ocorrencias_cvli
SET sexo_vitima = CASE
    WHEN UPPER(sexo_vitima) IN ('M', 'MASCULINO', 'MASC')   THEN 'Masculino'
    WHEN UPPER(sexo_vitima) IN ('F', 'FEMININO', 'FEM')     THEN 'Feminino'
    WHEN sexo_vitima IS NULL OR TRIM(sexo_vitima) = ''       THEN 'Não informado'
    ELSE sexo_vitima
END;

-- 7. Preencher valores nulos com "Não informado" (ao invés de NULL)
UPDATE ocorrencias_cvli
SET faixa_etaria = 'Não informado'
WHERE faixa_etaria IS NULL OR TRIM(faixa_etaria) = '';

UPDATE ocorrencias_cvli
SET raca_cor = 'Não informado'
WHERE raca_cor IS NULL OR TRIM(raca_cor) = '';

UPDATE ocorrencias_cvli
SET ais = 'Não informado'
WHERE ais IS NULL OR TRIM(ais) = '';

UPDATE ocorrencias_cvp
SET ais = 'Não informado'
WHERE ais IS NULL OR TRIM(ais) = '';

-- 8. Remover linhas onde municipio ou tipo_crime estão vazios
-- (essas linhas não têm utilidade para análise)
DELETE FROM ocorrencias_cvli
WHERE municipio IS NULL OR TRIM(municipio) = ''
   OR tipo_crime IS NULL OR TRIM(tipo_crime) = '';

DELETE FROM ocorrencias_cvp
WHERE municipio IS NULL OR TRIM(municipio) = ''
   OR tipo_crime IS NULL OR TRIM(tipo_crime) = '';

-- 9. Remover linhas com quantidade negativa ou NULL
-- (erro de digitação na fonte)
DELETE FROM ocorrencias_cvli WHERE quantidade IS NULL OR quantidade < 0;
DELETE FROM ocorrencias_cvp  WHERE quantidade IS NULL OR quantidade < 0;

-- ------------------------------------------------------------
-- ENRIQUECIMENTO: Adicionar coluna auxiliar de nome do mês
-- ------------------------------------------------------------

-- 10. Adicionar coluna com nome do mês (facilita leitura dos relatórios)
ALTER TABLE ocorrencias_cvli ADD COLUMN IF NOT EXISTS nome_mes VARCHAR(20);
ALTER TABLE ocorrencias_cvp  ADD COLUMN IF NOT EXISTS nome_mes VARCHAR(20);

UPDATE ocorrencias_cvli
SET nome_mes = TO_CHAR(TO_DATE(mes::TEXT, 'MM'), 'TMMonth');

UPDATE ocorrencias_cvp
SET nome_mes = TO_CHAR(TO_DATE(mes::TEXT, 'MM'), 'TMMonth');

-- ------------------------------------------------------------
-- VERIFICAÇÃO FINAL
-- ------------------------------------------------------------
SELECT 'Após tratamento — CVLI' AS tabela, COUNT(*) AS total FROM ocorrencias_cvli
UNION ALL
SELECT 'Após tratamento — CVP',             COUNT(*)         FROM ocorrencias_cvp;

SELECT 'Tratamento concluído com sucesso!' AS status;
