# Relatório Técnico - FarmTech Solutions Fase 3
**Desenvolvido por**: Richard Schmitz - RM567951 

## Resumo Executivo

A Fase 3 do projeto FarmTech Solutions implementou com sucesso a integração dos dados coletados pelos sensores IoT (Fase 2) em um banco de dados Oracle corporativo. O sistema demonstrou eficiência na coleta, armazenamento e análise de dados para otimização da irrigação de soja.

## Metodologia

### 1. Preparação dos Dados
- **Fonte**: Arquivo CSV da Fase 2 com 15 registros horários
- **Período**: 01/10/2025 das 08:00 às 22:00
- **Limpeza**: Remoção de caracteres especiais e validação de tipos

### 2. Configuração do Banco Oracle
- **Ambiente**: Oracle Database via SQL Developer
- **Conexão**: oracle.fiap.com.br:1521/ORCL
- **Tabela**: SENSORES_SOJA_RM567951

### 3. Estrutura da Tabela
```sql
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

## Resultados Obtidos

### Estatísticas Gerais
- **Total de registros**: 15
- **Irrigações realizadas**: 8 (53.3% do tempo)
- **Umidade média**: 61.4%
- **pH médio**: 6.4
- **Temperatura média**: 27.1°C

### Análises Realizadas

#### 1. Eficiência do Sistema de Irrigação
- Sistema ativado corretamente quando umidade < 60%
- Desativado durante períodos de chuva (17:00-19:00)
- Taxa de acerto: 100% nas condições críticas

#### 2. Qualidade do Solo
- pH mantido na faixa ideal para soja (6.0-6.8)
- 100% das medições dentro do range aceitável
- Nutrientes NPK balanceados em 80% das medições

#### 3. Correlação Chuva vs Irrigação
- **Sem chuva**: 11 registros, 8 irrigações (72.7%)
- **Com chuva**: 4 registros, 0 irrigações (0%)
- Demonstra eficiência do algoritmo de decisão

#### 4. Padrões Temporais
- **Manhã (08-11h)**: Umidade baixa, irrigação necessária
- **Tarde (12-17h)**: Pico de temperatura, irrigação crítica
- **Noite (18-22h)**: Chuva natural, irrigação desnecessária

## Consultas SQL Implementadas

### Consultas Básicas
1. `SELECT * FROM SENSORES_SOJA_RM567951` - Visualização geral
2. Estatísticas agregadas (COUNT, AVG, MIN, MAX)
3. Filtros por condições críticas

### Consultas Analíticas
4. Análise de nutrientes NPK por disponibilidade
5. Correlação entre chuva e irrigação
6. Padrões por período do dia
7. Verificação de condições ideais para soja
8. Eficiência do sistema de irrigação
9. Tendências horárias
10. Relatório executivo consolidado

## Insights Técnicos

### Pontos Fortes
- **Precisão**: Sistema de irrigação 100% eficiente
- **Sustentabilidade**: Economia de água durante chuvas
- **Monitoramento**: pH sempre na faixa ideal
- **Automação**: Decisões baseadas em múltiplos sensores

### Oportunidades de Melhoria
- Aumentar frequência de coleta (atual: 1h)
- Implementar predição meteorológica
- Adicionar sensores de vento e radiação solar
- Desenvolver algoritmos de machine learning

## Validação dos Dados

### Integridade
- Todos os timestamps validados
- Valores numéricos dentro dos intervalos esperados
- Correlações lógicas entre variáveis confirmadas
- Ausência de dados duplicados ou inconsistentes

### Qualidade
- **Completude**: 100% dos campos preenchidos
- **Precisão**: Valores compatíveis com sensores reais
- **Consistência**: Padrões temporais coerentes
- **Relevância**: Dados adequados para análise agrícola

## Conclusões

### Técnicas
1. **Banco Oracle**: Implementação bem-sucedida com performance adequada
2. **Consultas SQL**: Conjunto abrangente de análises implementadas
3. **Integridade**: Dados íntegros e consistentes para análises futuras

### Agronômicas
1. **Irrigação Inteligente**: Sistema demonstrou eficiência operacional
2. **Qualidade do Solo**: Parâmetros mantidos dentro do ideal para soja
3. **Sustentabilidade**: Redução do desperdício de água comprovada

### Próximos Passos
1. **Dashboard**: Implementar visualização em tempo real (Streamlit)
2. **Machine Learning**: Desenvolver modelos preditivos
3. **Escalabilidade**: Expandir para múltiplas culturas
4. **IoT Avançado**: Integrar mais tipos de sensores

## Anexos

### A. Scripts Desenvolvidos
- `preparacao_dados.py`: Limpeza e validação dos dados
- `consultas_sql.sql`: Conjunto completo de consultas analíticas

### B. Arquivos de Dados
- `dados_sensores_limpos.csv`: Dataset preparado para Oracle
- Screenshots do processo de importação e consultas



---
