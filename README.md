# FarmTech Solutions - Fase 3: Banco de Dados Oracle

- **Desenvolvedor**: Richard Schmitz
- **RM**: 567951
- **Curso**: Inteligência Artificial - FIAP


Implementação de banco de dados Oracle para armazenamento e análise de dados coletados por sensores IoT do sistema de irrigação inteligente para cultivo de soja.

## Dados Importados

### Origem dos Dados
- **Fonte**: Sensores IoT da Fase 2 (arquivo `dados_sensores.csv`)
- **Período**: Outubro 2025
- **Frequência**: Coleta horária
- **Cultura**: Soja

### Estrutura dos Dados

| Campo | Tipo | Descrição |
|-------|------|-----------|
| timestamp | TIMESTAMP | Data e hora da coleta |
| umidade_solo | NUMBER(5,2) | Umidade do solo (%) |
| ph_solo | NUMBER(3,1) | pH do solo |
| nitrogenio | NUMBER(1) | Presença de nitrogênio (0/1) |
| fosforo | NUMBER(1) | Presença de fósforo (0/1) |
| potassio | NUMBER(1) | Presença de potássio (0/1) |
| temperatura | NUMBER(4,1) | Temperatura ambiente (°C) |
| chuva_mm | NUMBER(4,1) | Precipitação (mm) |
| irrigacao_ativa | NUMBER(1) | Status irrigação (0/1) |

## Configuração do Banco Oracle

### Conexão
- **Host**: oracle.fiap.com.br
- **Porta**: 1521
- **SID**: ORCL
- **Usuário**: RM567951


### Tabela Criada
```sql
-- Nome da tabela: SENSORES_SOJA_RM567951
CREATE TABLE SENSORES_SOJA_RM567951 (
    TIMESTAMP TIMESTAMP,
    UMIDADE_SOLO NUMBER(5,2),
    PH_SOLO NUMBER(3,1),
    NITROGENIO NUMBER(1),
    FOSFORO NUMBER(1),
    POTASSIO NUMBER(1),
    TEMPERATURA NUMBER(4,1),
    CHUVA_MM NUMBER(4,1),
    IRRIGACAO_ATIVA NUMBER(1)
);
```

## Consultas SQL Realizadas

### 1. Consulta Geral
```sql
SELECT * FROM SENSORES_SOJA_RM567951;
```

### 2. Análise de Irrigação
```sql
SELECT 
    COUNT(*) as total_registros,
    SUM(IRRIGACAO_ATIVA) as vezes_irrigado,
    ROUND(AVG(UMIDADE_SOLO), 2) as umidade_media,
    ROUND(AVG(PH_SOLO), 2) as ph_medio
FROM SENSORES_SOJA_RM567951;
```

### 3. Condições Críticas
```sql
SELECT * FROM SENSORES_SOJA_RM567951 
WHERE UMIDADE_SOLO < 50 
AND IRRIGACAO_ATIVA = 1
ORDER BY TIMESTAMP;
```

### 4. Análise NPK
```sql
SELECT 
    NITROGENIO + FOSFORO + POTASSIO as nutrientes_disponiveis,
    COUNT(*) as ocorrencias,
    ROUND(AVG(UMIDADE_SOLO), 2) as umidade_media
FROM SENSORES_SOJA_RM567951
GROUP BY NITROGENIO + FOSFORO + POTASSIO
ORDER BY nutrientes_disponiveis DESC;
```

### 5. Correlação Chuva vs Irrigação
```sql
SELECT 
    CASE 
        WHEN CHUVA_MM > 0 THEN 'Com Chuva'
        ELSE 'Sem Chuva'
    END as condicao_chuva,
    COUNT(*) as registros,
    SUM(IRRIGACAO_ATIVA) as irrigacoes,
    ROUND(AVG(UMIDADE_SOLO), 2) as umidade_media
FROM SENSORES_SOJA_RM567951
GROUP BY CASE WHEN CHUVA_MM > 0 THEN 'Com Chuva' ELSE 'Sem Chuva' END;
```

## Processo de Importação

### Passos Seguidos:

1. **Download Oracle SQL Developer**
   - Versão para macOS baixada do site oficial Oracle

2. **Configuração da Conexão**
   - Nome: FIAP_FARMTECH
   - Usuário: RM567951
   - Host: oracle.fiap.com.br
   - Porta: 1521
   - SID: ORCL

3. **Preparação dos Dados**
   - Limpeza do arquivo CSV da Fase 2
   - Remoção de linhas vazias e caracteres especiais

4. **Importação**
   - Clique direito em "Tabelas (Filtrado)"
   - Seleção "Importa Dados"
   - Carregamento do arquivo `dados_sensores.csv`
   - Definição do nome da tabela: `SENSORES_SOJA_RM567951`

5. **Validação**
   - Execução de consultas SELECT
   - Verificação da integridade dos dados
   - Análise estatística básica

## Resultados Obtidos

### Estatísticas dos Dados:
- **Total de registros**: 15
- **Período de coleta**: 01/10/2025 08:00 - 01/10/2025 22:00
- **Ativações de irrigação**: 8 (53.3% do período)
- **Umidade média do solo**: 61.4%
- **pH médio**: 6.4

### Análise dos Resultados:
- Sistema de irrigação acionado conforme parâmetros estabelecidos (umidade < 60%)
- pH mantido dentro da faixa ótima para cultivo de soja (6.0-6.8)
- Suspensão automática da irrigação durante precipitações
- Balanço adequado de nutrientes NPK na maioria das amostras

## Arquivos do Projeto

```
FarmTech_Solutions_Fase3/
├── README.md
├── database/
│   ├── dados_sensores_limpos.csv
│   └── consultas_sql.sql
├── screenshots/
│   ├── 01_conexao_oracle.png
│   ├── 02_importacao_dados.png
│   ├── 03_tabela_criada.png
│   ├── 04_consulta_geral.png
│   └── 05_analises_sql.png
├── scripts/
│   └── preparacao_dados.py
└── docs/
    └── relatorio_fase3.md
```

**Conteúdo demonstrado**:
- Estabelecimento de conexão com Oracle SQL Developer
- Procedimento de importação dos dados
- Execução das consultas SQL desenvolvidas
- Apresentação dos resultados analíticos

