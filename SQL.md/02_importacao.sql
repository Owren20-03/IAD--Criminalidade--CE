-- ============================================================
-- 02_importacao.sql
-- Importação dos arquivos CSV para o PostgreSQL
-- Projeto: Análise de Criminalidade no Ceará (SSPDS-CE)
-- ============================================================

-- ⚠️  ATENÇÃO: Antes de rodar este script:
--     1. Verifique que os CSVs estão em /caminho/para/seus/dados/
--     2. Ajuste os caminhos abaixo conforme onde você salvou os arquivos
--     3. Abra o CSV num editor e confira se os nomes das colunas batem

-- ------------------------------------------------------------
-- OPÇÃO A: Importar com COPY (via psql no terminal)
-- Troque o caminho pelo caminho real do arquivo no seu computador
-- ------------------------------------------------------------

-- Importar CVLI
COPY ocorrencias_cvli (ano, mes, municipio, tipo_crime, quantidade, sexo_vitima, faixa_etaria, raca_cor, ais)
FROM '/caminho/para/dados/cvli_2021.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

COPY ocorrencias_cvli (ano, mes, municipio, tipo_crime, quantidade, sexo_vitima, faixa_etaria, raca_cor, ais)
FROM '/caminho/para/dados/cvli_2022.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

COPY ocorrencias_cvli (ano, mes, municipio, tipo_crime, quantidade, sexo_vitima, faixa_etaria, raca_cor, ais)
FROM '/caminho/para/dados/cvli_2023.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- Importar CVP
COPY ocorrencias_cvp (ano, mes, municipio, tipo_crime, quantidade, ais)
FROM '/caminho/para/dados/cvp_2021.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

COPY ocorrencias_cvp (ano, mes, municipio, tipo_crime, quantidade, ais)
FROM '/caminho/para/dados/cvp_2022.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

COPY ocorrencias_cvp (ano, mes, municipio, tipo_crime, quantidade, ais)
FROM '/caminho/para/dados/cvp_2023.csv'
DELIMITER ';'
CSV HEADER
ENCODING 'UTF8';

-- ------------------------------------------------------------
-- OPÇÃO B: Se estiver usando o DBeaver
-- Clique com o botão direito na tabela → Import Data
-- Selecione o arquivo CSV e mapeie as colunas manualmente
-- ------------------------------------------------------------

-- Verificação rápida após importação
SELECT 'CVLI importados:'  AS tabela, COUNT(*) AS total FROM ocorrencias_cvli
UNION ALL
SELECT 'CVP importados:',           COUNT(*)         FROM ocorrencias_cvp;
