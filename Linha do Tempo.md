# 🕐 Linha do Tempo — Projeto IAD Criminalidade CE

Registro de todas as etapas, pedidos e ajustes feitos durante o desenvolvimento do projeto com ajuda do Claude.

---

## 📌 Etapa 1 — Planejamento inicial
**Pedido:** Ajuda para fazer o trabalho final de Análise de Dados com SQL sobre criminalidade no Ceará usando dados do SSPDS-CE.

**Contexto definido:**
- Dados: SSPDS-CE (`sspds.ce.gov.br`)
- Período: 2021 a 2023
- Nível SQL: iniciante
- Precisava de tudo: estrutura, SQL e relatório

**Entregues:**
- `README.md`
- `dados/INSTRUCOES_DOWNLOAD.md`
- `sql/01_criacao.sql`
- `sql/02_importacao.sql`
- `sql/03_tratamento.sql`
- `sql/04_consultas.sql` (7 perguntas analíticas)
- `relatorio/relatorio.md`

---

## 📌 Etapa 2 — Ajuste de período
**Pedido:** Confirmação se a mudança de período para 2021–2023 afetava algum arquivo.

**Resultado:** Nenhum arquivo precisou ser alterado — o período 2021–2023 já estava correto em todos os arquivos gerados.

---

## 📌 Etapa 3 — Problema no DBeaver (multi-database)
**Pedido:** Ajuda para criar o banco `criminalidade_ce` no DBeaver após erro:
> *"Cannot create a database when multi-database mode is disabled"*

**Solução:** Ativar a opção **"Show all databases"** nas configurações da conexão PostgreSQL no DBeaver.

---

## 📌 Etapa 4 — Dados em uma planilha única (não separados por ano)
**Pedido:** Os dados baixados vieram em uma planilha única com os 3 anos juntos, não em arquivos separados por ano como o script esperava.

**Arquivo enviado:** `Dados_Filtrados_2021_a_2023.xlsx`

**Descoberta:** O arquivo tinha 3 abas:
- `CVLI` — 9.239 linhas
- `Intervencao_Policial` — 424 linhas
- `Unidade_Prisional` — apenas 4 linhas (descartada)

**Ação:** Script Python gerou os CSVs separados por ano:
- `cvli_2021.csv` (3.299 linhas)
- `cvli_2022.csv` (2.970 linhas)
- `cvli_2023.csv` (2.970 linhas)
- `intervencao_policial_2021/22/23.csv`

---

## 📌 Etapa 5 — Atualização dos SQLs com colunas reais
**Pedido:** Os arquivos SQL precisavam ser atualizados pois as colunas reais eram diferentes das planejadas inicialmente.

**Colunas reais do CVLI:** `Município, AIS, Natureza, Data, Hora, Dia da Semana, Meio Empregado, Gênero, Idade da Vítima, Escolaridade da Vítima, Raça da Vítima`

**Arquivos atualizados:** `01_criacao.sql`, `02_importacao.sql`, `03_tratamento.sql`, `04_consultas.sql`

---

## 📌 Etapa 6 — Adição dos dados de CVP
**Pedido:** Verificar se o arquivo `CVP_2021_a_2023.csv` correspondia ao CVP ou era igual ao anterior.

**Resultado:** Era o CVP de fato — 136.678 linhas com colunas: `AIS, Município, Dia da Semana, Data, Hora`.

**Ação:** Gerados os CSVs separados por ano:
- `cvp_2021.csv` (48.141 linhas)
- `cvp_2022.csv` (45.930 linhas)
- `cvp_2023.csv` (42.607 linhas)

**Todos os 4 SQLs atualizados** para incluir a nova tabela `cvp`.

---

## 📌 Etapa 7 — Erro no COPY do PostgreSQL
**Erro:** 
> *"could not open file for reading: No such file or directory. COPY FROM instructs the PostgreSQL server process to read a file."*

**Causa:** O comando `COPY` tenta ler o arquivo pelo servidor PostgreSQL, não pelo computador local.

**Solução:** Usar a importação visual do DBeaver (botão direito na tabela → Import Data) em vez do `COPY`.

---

## 📌 Etapa 8 — Dados importados em uma coluna só
**Problema:** O preview da importação mostrava todos os dados colados em uma única coluna.

**Causa:** O DBeaver estava usando `,` (vírgula) como delimitador, mas os CSVs usam `;` (ponto e vírgula).

**Solução:** Alterar o delimitador para `;` nas configurações de importação.

---

## 📌 Etapa 9 — Colunas duplicadas após importação errada
**Problema:** A importação do arquivo de 2021 entrou errada (sem o delimitador correto), gerando colunas duplicadas com nomes originais do CSV (`"Dia da Semana"`, `"Meio Empregado"`, etc.) em vez de mapear para as colunas existentes.

**Solução:**
1. `TRUNCATE TABLE cvli` para apagar tudo
2. Reimportar os 3 arquivos com delimitador `;` correto
3. Mapear manualmente as colunas na tela de mapeamento do DBeaver

---

## 📌 Etapa 10 — DBeaver insistindo em "Persist Changes"
**Problema:** O DBeaver ficou travado exibindo a tela "Persist Changes" com `DROP COLUMN` de colunas que já não existiam, impedindo o "Save All".

**Causa:** O DBeaver guardou na memória as alterações feitas visualmente, mas as colunas já tinham sido removidas manualmente antes.

**Solução:** Fechar o DBeaver sem salvar — os dados no PostgreSQL já estavam corretos e não foram afetados.

---

## 📌 Etapa 11 — Aviso "Execute dangerous queries" no tratamento
**Situação:** Ao rodar o `03_tratamento.sql`, o DBeaver exibiu aviso de "possível perda de dados" nos comandos `UPDATE` sem `WHERE`.

**Esclarecimento:** Nenhuma perda real — o aviso é padrão do DBeaver para `UPDATE` sem filtro. Os comandos apenas removiam espaços extras dos textos.

---

## 📌 Etapa 12 — Erro no DELETE do tratamento
**Erro:** Linha 167 do `03_tratamento.sql` com erro de coluna inexistente.

**Causa:** Script gerado com `IS NULL` faltando na condição:
```sql
-- Errado (estava assim):
DELETE FROM cvli WHERE municipio OR TRIM(municipio) = '';

-- Correto:
DELETE FROM cvli WHERE municipio IS NULL OR TRIM(municipio) = '';
```

**Status:** Corrigido manualmente no SQL Editor.

---

## 📊 Status atual do projeto

| Etapa | Status |
|---|---|
| Estrutura do repositório | ✅ Concluído |
| Download e separação dos dados | ✅ Concluído |
| Criação das tabelas (`01_criacao.sql`) | ✅ Concluído |
| Importação dos dados (`02_importacao.sql`) | ✅ Concluído |
| Tratamento dos dados (`03_tratamento.sql`) | ✅ Concluído |
| Consultas analíticas (`04_consultas.sql`) | ✅ Concluído |
| Dashboard (Looker Studio / Power BI) | ⏳ Pendente |
| Relatório final | ✅ Concluído |
