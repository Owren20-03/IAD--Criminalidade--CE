-- ============================================================
-- 02_importacao.sql
-- Tutorial de importação dos CSVs via DBeaver
-- Projeto: Análise de Criminalidade no Ceará (SSPDS-CE)
-- ============================================================

-- O comando COPY do PostgreSQL não funciona pelo DBeaver
-- pois ele tenta ler o arquivo pelo servidor, não pelo seu
-- computador. Use o importador visual do DBeaver conforme
-- o tutorial abaixo.

-- ============================================================
-- TUTORIAL — Como importar cada CSV pelo DBeaver
-- ============================================================

-- PASSO 1: Na barra lateral esquerda, expanda:
--   criminalidade_ce → Schemas → criminalidade → Tables

-- PASSO 2: Clique com botão direito na tabela desejada
--   (ex: cvli) → Import Data

-- PASSO 3: Selecione "CSV" como formato → clique Next

-- PASSO 4: Clique em Browse e selecione o arquivo CSV
--   (ex: cvli_2021.csv)

-- PASSO 5: IMPORTANTE — mude o delimitador de "," para ";"
--   (os arquivos usam ponto e vírgula como separador)

-- PASSO 6: Clique em Next para ir à tela de mapeamento.
--   Clique na seta (▶) ao lado do nome do arquivo para
--   expandir e ver as colunas.

-- PASSO 7: Mapeie as colunas conforme a tabela abaixo,
--   clicando em cada linha do Target e corrigindo se
--   aparecer o nome com aspas ou incorreto.

-- PASSO 8: Clique em Proceed para iniciar a importação.

-- PASSO 9: Repita o processo para cada arquivo CSV.

-- ============================================================
-- MAPEAMENTO DE COLUNAS — tabela cvli
-- ============================================================
--  Source (CSV)             →  Target (banco)
--  Município                →  municipio
--  AIS                      →  ais
--  Natureza                 →  natureza
--  Data                     →  data        (pode ficar "data")
--  Hora                     →  hora
--  Dia da Semana            →  dia_semana
--  Meio Empregado           →  meio_empregado
--  Gênero                   →  genero
--  Idade da Vítima          →  idade_vitima
--  Escolaridade da Vítima   →  escolaridade_vitima
--  Raça da Vítima           →  raca_vitima
--
--       As colunas "ano", "mes" e "id" NÃO aparecem —
--      são geradas automaticamente pelo banco. Ignore-as.

-- ============================================================
-- MAPEAMENTO DE COLUNAS — tabela cvp
-- ============================================================
--  Source (CSV)   →  Target (banco)
--  AIS            →  ais
--  Município      →  municipio
--  Dia da Semana  →  dia_semana
--  Data           →  data
--  Hora           →  hora

-- ============================================================
-- MAPEAMENTO DE COLUNAS — tabela intervencao_policial
-- ============================================================
--  Source (CSV)   →  Target (banco)
--  Município      →  municipio
--  AIS            →  ais
--  Meio Empregado →  meio_empregado
--  Data           →  data
--  Hora           →  hora
--  Dia da Semana  →  dia_semana
--  Gênero         →  genero
--  Idade          →  idade
--  Escolaridade   →  escolaridade
--  Raça           →  raca

-- ============================================================
-- ORDEM DE IMPORTAÇÃO
-- ============================================================
--  1. cvli_2021.csv          → tabela cvli
--  2. cvli_2022.csv          → tabela cvli
--  3. cvli_2023.csv          → tabela cvli
--  4. cvp_2021.csv           → tabela cvp
--  5. cvp_2022.csv           → tabela cvp
--  6. cvp_2023.csv           → tabela cvp
--  7. intervencao_policial_2021.csv  → tabela intervencao_policial
--  8. intervencao_policial_2022.csv  → tabela intervencao_policial
--  9. intervencao_policial_2023.csv  → tabela intervencao_policial

-- ============================================================
-- VERIFICAÇÃO — rode após importar tudo
-- ============================================================
SELECT 'CVLI'                AS tabela, COUNT(*) AS total FROM cvli
UNION ALL
SELECT 'CVP',                           COUNT(*)          FROM cvp
UNION ALL
SELECT 'Intervenção Policial',          COUNT(*)          FROM intervencao_policial;

-- Esperado:
-- CVLI                 →  9.239 linhas
-- CVP                  → 136.678 linhas
-- Intervenção Policial →    424 linhas
