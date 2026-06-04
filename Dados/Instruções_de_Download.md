# 📥 Como Baixar os Dados do SSPDS-CE

## Fonte oficial

Acesse: https://www.sspds.ce.gov.br/estatisticas-2/

## O que baixar

Na página, procure pelas seções de **Indicadores Criminais Detalhados** — são planilhas em formato `.xlsx` ou `.csv`.

### Arquivos utilizados neste projeto:
1. **CVLI** — Crimes Violentos Letais e Intencionais (homicídios, latrocínios, feminicídio)
2. **CVP** — Crimes Violentos contra o Patrimônio (roubos, furtos)

> ⚠️ Os dados podem vir em uma planilha única com todos os anos juntos.
> Nesse caso, use o script Python abaixo para separar por ano automaticamente.

## Como separar os dados por ano (Python)

Se o arquivo vier com todos os anos numa planilha só (ex: `Dados_2021_a_2023.xlsx`),
rode o script abaixo para gerar os CSVs separados:

```python
import pandas as pd
import os

# Separar CVLI (arquivo .xlsx com múltiplas abas)
xls = pd.ExcelFile("Dados_Filtrados_2021_a_2023.xlsx")
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    df['Data'] = pd.to_datetime(df['Data'])
    df['ano'] = df['Data'].dt.year
    for ano in sorted(df['ano'].unique()):
        df_ano = df[df['ano'] == ano].drop(columns=['ano'])
        df_ano.to_csv(f"{sheet.lower()}_{ano}.csv", index=False, sep=';', encoding='utf-8-sig')
        print(f"Gerado: {sheet.lower()}_{ano}.csv — {len(df_ano)} linhas")

# Separar CVP (arquivo .csv único)
df = pd.read_csv("CVP_2021_a_2023.csv")
df['Data'] = pd.to_datetime(df['Data'])
df['ano'] = df['Data'].dt.year
for ano in sorted(df['ano'].unique()):
    df_ano = df[df['ano'] == ano].drop(columns=['ano'])
    df_ano.to_csv(f"cvp_{ano}.csv", index=False, sep=';', encoding='utf-8-sig')
    print(f"Gerado: cvp_{ano}.csv — {len(df_ano)} linhas")
```

## Arquivos gerados

Após rodar o script, a pasta `dados/` deve conter:

```
dados/
├── cvli_2021.csv                     (3.299 linhas)
├── cvli_2022.csv                     (2.970 linhas)
├── cvli_2023.csv                     (2.970 linhas)
├── cvp_2021.csv                      (48.141 linhas)
├── cvp_2022.csv                      (45.930 linhas)
├── cvp_2023.csv                      (42.607 linhas)
├── intervencao_policial_2021.csv     (125 linhas)
├── intervencao_policial_2022.csv     (152 linhas)
└── intervencao_policial_2023.csv     (147 linhas)
```

## Colunas reais dos arquivos

### CVLI
| Coluna | Descrição |
|--------|-----------|
| Município | Nome do município |
| AIS | Área Integrada de Segurança |
| Natureza | Tipo do crime (ex: Homicídio Doloso, Feminicídio) |
| Data | Data da ocorrência |
| Hora | Hora da ocorrência |
| Dia da Semana | Dia da semana |
| Meio Empregado | Arma ou meio utilizado |
| Gênero | Gênero da vítima |
| Idade da Vítima | Idade da vítima |
| Escolaridade da Vítima | Escolaridade da vítima |
| Raça da Vítima | Raça/Cor da vítima |

### CVP
| Coluna | Descrição |
|--------|-----------|
| AIS | Área Integrada de Segurança |
| Município | Nome do município |
| Dia da Semana | Dia da semana |
| Data | Data da ocorrência |
| Hora | Hora da ocorrência |

### Intervenção Policial
| Coluna | Descrição |
|--------|-----------|
| Município | Nome do município |
| AIS | Área Integrada de Segurança |
| Meio Empregado | Arma ou meio utilizado |
| Data | Data da ocorrência |
| Hora | Hora da ocorrência |
| Dia da Semana | Dia da semana |
| Gênero | Gênero da vítima |
| Idade | Idade da vítima |
| Escolaridade | Escolaridade da vítima |
| Raça | Raça/Cor da vítima |

> ⚠️ O delimitador dos CSVs gerados é `;` (ponto e vírgula).
> Lembre de configurar isso na tela de importação do DBeaver.
