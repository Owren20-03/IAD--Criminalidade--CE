# 📥 Como Baixar os Dados do SSPDS-CE

## Fonte oficial

Acesse: https://www.sspds.ce.gov.br/estatisticas-2/

## O que baixar

Na página, procure pelas seções de **Indicadores Criminais Detalhados** — são planilhas em formato `.xlsx` ou `.csv`.

### Arquivos recomendados:
1. **CVLI** — Crimes Violentos Letais e Intencionais (homicídios, latrocínios)
2. **CVP** — Crimes Violentos contra o Patrimônio (roubos, furtos)

Baixe os dados de pelo menos **3 anos** (ex: 2021, 2022, 2023) para ter análise temporal.

## Como salvar

Salve os arquivos baixados nesta pasta (`dados/`) com os nomes:
```
dados/
├── cvli_2021.csv
├── cvli_2022.csv
├── cvli_2023.csv
├── cvp_2021.csv
├── cvp_2022.csv
└── cvp_2023.csv
```

## Colunas esperadas nos arquivos

As planilhas da SUPESP geralmente contêm:

| Coluna             | Descrição                              |
|--------------------|----------------------------------------|
| ano                | Ano da ocorrência                      |
| mes                | Mês da ocorrência (número)             |
| municipio          | Nome do município                      |
| tipo_crime         | Tipo do crime (ex: Homicídio doloso)   |
| quantidade         | Número de ocorrências                  |
| sexo_vitima        | Sexo da vítima                         |
| faixa_etaria       | Faixa etária da vítima                 |
| raca_cor           | Raça/Cor da vítima                     |
| ais                | Área Integrada de Segurança            |

> ⚠️ Os nomes das colunas podem variar entre versões dos arquivos.
> Abra o CSV em um editor antes de importar e ajuste o script de importação se necessário.

## Dica: teste com uma amostra pequena

Antes de importar tudo, importe apenas 1 arquivo pequeno para verificar se as colunas batem com as tabelas criadas no SQL.
