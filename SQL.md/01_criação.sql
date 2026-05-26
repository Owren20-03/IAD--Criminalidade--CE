-- ============================================================
-- 01_criacao.sql
-- Criação das tabelas do banco de dados
-- Projeto: Análise de Criminalidade no Ceará (SSPDS-CE)
-- ============================================================

-- Remove as tabelas se já existirem (útil para recriar do zero)
DROP TABLE IF EXISTS ocorrencias_cvli CASCADE;
DROP TABLE IF EXISTS ocorrencias_cvp CASCADE;
DROP TABLE IF EXISTS municipios CASCADE;

-- ------------------------------------------------------------
-- Tabela de municípios (dimensão auxiliar)
-- ------------------------------------------------------------
CREATE TABLE municipios (
    id          SERIAL PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL UNIQUE,
    ais         VARCHAR(10),   -- Área Integrada de Segurança
    regiao      VARCHAR(50)    -- ex: Fortaleza, Grande Fortaleza, Interior
);

-- ------------------------------------------------------------
-- Tabela de CVLI
-- Crimes Violentos Letais e Intencionais
-- (homicídios dolosos, latrocínios, lesão corporal seguida de morte)
-- ------------------------------------------------------------
CREATE TABLE ocorrencias_cvli (
    id              SERIAL PRIMARY KEY,
    ano             SMALLINT       NOT NULL,
    mes             SMALLINT       NOT NULL CHECK (mes BETWEEN 1 AND 12),
    municipio       VARCHAR(100)   NOT NULL,
    tipo_crime      VARCHAR(100)   NOT NULL,
    quantidade      INTEGER        NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
    sexo_vitima     VARCHAR(20),
    faixa_etaria    VARCHAR(30),
    raca_cor        VARCHAR(30),
    ais             VARCHAR(10)
);

-- ------------------------------------------------------------
-- Tabela de CVP
-- Crimes Violentos contra o Patrimônio
-- (roubos a pessoas, veículos, residências, comércio)
-- ------------------------------------------------------------
CREATE TABLE ocorrencias_cvp (
    id              SERIAL PRIMARY KEY,
    ano             SMALLINT       NOT NULL,
    mes             SMALLINT       NOT NULL CHECK (mes BETWEEN 1 AND 12),
    municipio       VARCHAR(100)   NOT NULL,
    tipo_crime      VARCHAR(100)   NOT NULL,
    quantidade      INTEGER        NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
    ais             VARCHAR(10)
);

-- ------------------------------------------------------------
-- Índices para acelerar as consultas analíticas
-- ------------------------------------------------------------
CREATE INDEX idx_cvli_ano_municipio ON ocorrencias_cvli(ano, municipio);
CREATE INDEX idx_cvli_tipo_crime    ON ocorrencias_cvli(tipo_crime);
CREATE INDEX idx_cvli_municipio     ON ocorrencias_cvli(municipio);

CREATE INDEX idx_cvp_ano_municipio  ON ocorrencias_cvp(ano, municipio);
CREATE INDEX idx_cvp_tipo_crime     ON ocorrencias_cvp(tipo_crime);
CREATE INDEX idx_cvp_municipio      ON ocorrencias_cvp(municipio);

-- Confirma criação
SELECT 'Tabelas criadas com sucesso!' AS status;
