#!/usr/bin/env python3
"""
FarmTech Solutions - Fase 3: Dashboard Streamlit (Ir Além)
Desenvolvedor: Richard Schmitz - RM567951
Data: Janeiro 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="FarmTech Solutions - Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    """Carrega dados dos sensores"""
    try:
        df = pd.read_csv('database/dados_sensores_limpos.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except:
        # Dados de exemplo se arquivo não encontrado
        return pd.DataFrame({
            'timestamp': pd.date_range('2025-10-01 08:00', periods=15, freq='H'),
            'umidade_solo': [45.2, 52.8, 68.4, 71.2, 58.9, 43.7, 39.1, 55.3, 72.6, 81.2, 85.7, 78.9, 65.4, 58.2, 51.7],
            'ph_solo': [6.3, 6.5, 6.2, 6.7, 6.4, 6.1, 6.6, 6.3, 6.8, 6.5, 6.2, 6.4, 6.7, 6.3, 6.5],
            'nitrogenio': [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
            'fosforo': [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
            'potassio': [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            'temperatura': [22.5, 24.1, 26.3, 28.7, 31.2, 32.8, 33.5, 32.1, 29.4, 27.8, 25.6, 23.2, 21.5, 20.1, 19.3],
            'chuva_mm': [0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.3, 3.1, 1.8, 0.5, 0.0, 0.0],
            'irrigacao_ativa': [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]
        })

def main():
    # Header
    st.title("FarmTech Solutions - Dashboard IoT")
    st.markdown("**Sistema de Irrigação Inteligente para Cultivo de Soja**")
    st.markdown("---")
    
    # Carregar dados
    df = load_data()
    
    # Sidebar - Filtros
    st.sidebar.header("Filtros")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Umidade Média", 
            f"{df['umidade_solo'].mean():.1f}%",
            f"{df['umidade_solo'].std():.1f}% desvio"
        )
    
    with col2:
        st.metric(
            "pH Médio", 
            f"{df['ph_solo'].mean():.1f}",
            "Ideal: 6.0-6.8"
        )
    
    with col3:
        irrigacoes = df['irrigacao_ativa'].sum()
        st.metric(
            "Irrigações", 
            f"{irrigacoes}",
            f"{(irrigacoes/len(df)*100):.1f}% do tempo"
        )
    
    with col4:
        chuva_total = df['chuva_mm'].sum()
        st.metric(
            "Chuva Total", 
            f"{chuva_total:.1f}mm",
            f"Média: {df['chuva_mm'].mean():.1f}mm/h"
        )
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Umidade do Solo ao Longo do Tempo")
        fig_umidade = px.line(
            df, x='timestamp', y='umidade_solo',
            title="Monitoramento da Umidade",
            labels={'umidade_solo': 'Umidade (%)', 'timestamp': 'Tempo'}
        )
        fig_umidade.add_hline(y=60, line_dash="dash", line_color="red", 
                             annotation_text="Limite Irrigação (60%)")
        st.plotly_chart(fig_umidade, use_container_width=True)
    
    with col2:
        st.subheader("pH do Solo")
        fig_ph = px.scatter(
            df, x='timestamp', y='ph_solo', 
            color='irrigacao_ativa',
            title="Variação do pH",
            labels={'ph_solo': 'pH', 'timestamp': 'Tempo'}
        )
        fig_ph.add_hline(y=6.0, line_dash="dash", line_color="green")
        fig_ph.add_hline(y=6.8, line_dash="dash", line_color="green")
        st.plotly_chart(fig_ph, use_container_width=True)
    
    # Status da Irrigação
    st.subheader("Status da Irrigação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras - Irrigação por hora
        df['hora'] = df['timestamp'].dt.hour
        irrigacao_hora = df.groupby('hora')['irrigacao_ativa'].sum().reset_index()
        
        fig_irrigacao = px.bar(
            irrigacao_hora, x='hora', y='irrigacao_ativa',
            title="Irrigações por Hora do Dia",
            labels={'irrigacao_ativa': 'Irrigações', 'hora': 'Hora'}
        )
        st.plotly_chart(fig_irrigacao, use_container_width=True)
    
    with col2:
        # Correlação Chuva vs Irrigação
        df['tem_chuva'] = df['chuva_mm'] > 0
        correlacao = df.groupby('tem_chuva').agg({
            'irrigacao_ativa': 'sum',
            'umidade_solo': 'mean'
        }).reset_index()
        
        fig_chuva = px.bar(
            correlacao, x='tem_chuva', y='irrigacao_ativa',
            title="Irrigação vs Presença de Chuva",
            labels={'irrigacao_ativa': 'Total Irrigações', 'tem_chuva': 'Chuva'}
        )
        st.plotly_chart(fig_chuva, use_container_width=True)
    
    # Análise NPK
    st.subheader("Análise de Nutrientes NPK")
    
    df['npk_total'] = df['nitrogenio'] + df['fosforo'] + df['potassio']
    npk_stats = df.groupby('npk_total').size().reset_index(name='count')
    
    fig_npk = px.pie(
        npk_stats, values='count', names='npk_total',
        title="Distribuição de Nutrientes Disponíveis"
    )
    st.plotly_chart(fig_npk, use_container_width=True)
    
    # Sugestões de Irrigação
    st.subheader("Sugestões Baseadas em Clima")
    
    # Última medição
    ultima_medicao = df.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if ultima_medicao['umidade_solo'] < 60:
            st.error("Umidade baixa - Irrigação recomendada")
        else:
            st.success("Umidade adequada")
    
    with col2:
        if 6.0 <= ultima_medicao['ph_solo'] <= 6.8:
            st.success("pH ideal para soja")
        else:
            st.warning("pH fora da faixa ideal")
    
    with col3:
        if ultima_medicao['chuva_mm'] > 0:
            st.info("Chuva detectada - Suspender irrigação")
        else:
            st.info("Sem chuva - Monitorar umidade")
    
    # Dados brutos
    with st.expander("Ver Dados Brutos"):
        st.dataframe(df)

if __name__ == "__main__":
    main()