#!/usr/bin/env python3
"""
FarmTech Solutions - Fase 3: Preparação de Dados para Oracle
Desenvolvedor: Richard Schmitz - RM567951
Data: Janeiro 2025
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def limpar_dados_sensores():
    """
    Limpa e prepara os dados dos sensores da Fase 2 para importação no Oracle
    """
    
    # Caminho do arquivo original da Fase 2
    arquivo_original = "../FarmTech_Solutions_Fase2/dados_sensores.csv"
    arquivo_limpo = "database/dados_sensores_limpos.csv"
    
    try:
        # Ler arquivo CSV original
        print("Carregando dados da Fase 2...")
        df = pd.read_csv(arquivo_original, sep=',')
        
        # Remover colunas vazias e linhas com dados inválidos
        print("Processando limpeza dos dados...")
        
        # Remover colunas que são completamente vazias ou com nomes estranhos
        colunas_validas = ['timestamp', 'umidade_solo', 'ph_solo', 'nitrogenio', 
                          'fosforo', 'potassio', 'temperatura', 'chuva_mm', 'irrigacao_ativa']
        
        # Filtrar apenas as colunas válidas que existem
        colunas_existentes = [col for col in colunas_validas if col in df.columns]
        df_limpo = df[colunas_existentes].copy()
        
        # Remover linhas completamente vazias
        df_limpo = df_limpo.dropna(how='all')
        
        # Remover linhas onde timestamp está vazio
        df_limpo = df_limpo.dropna(subset=['timestamp'])
        
        # Converter timestamp para formato padrão
        df_limpo['timestamp'] = pd.to_datetime(df_limpo['timestamp'])
        
        # Preencher valores NaN com 0 para campos numéricos
        campos_numericos = ['umidade_solo', 'ph_solo', 'nitrogenio', 'fosforo', 
                           'potassio', 'temperatura', 'chuva_mm', 'irrigacao_ativa']
        
        for campo in campos_numericos:
            if campo in df_limpo.columns:
                df_limpo[campo] = pd.to_numeric(df_limpo[campo], errors='coerce').fillna(0)
        
        # Validar dados
        print("Executando validação dos dados...")
        
        # Umidade entre 0 e 100%
        df_limpo['umidade_solo'] = df_limpo['umidade_solo'].clip(0, 100)
        
        # pH entre 0 e 14
        df_limpo['ph_solo'] = df_limpo['ph_solo'].clip(0, 14)
        
        # NPK e irrigação apenas 0 ou 1
        for campo in ['nitrogenio', 'fosforo', 'potassio', 'irrigacao_ativa']:
            if campo in df_limpo.columns:
                df_limpo[campo] = df_limpo[campo].clip(0, 1).astype(int)
        
        # Temperatura entre -50 e 60°C
        df_limpo['temperatura'] = df_limpo['temperatura'].clip(-50, 60)
        
        # Chuva não pode ser negativa
        df_limpo['chuva_mm'] = df_limpo['chuva_mm'].clip(0, None)
        
        # Salvar dados limpos
        print("Salvando dados processados...")
        df_limpo.to_csv(arquivo_limpo, index=False)
        
        # Estatísticas
        print("\nESTATÍSTICAS DOS DADOS PROCESSADOS:")
        print(f"Total de registros: {len(df_limpo)}")
        print(f"Período: {df_limpo['timestamp'].min()} até {df_limpo['timestamp'].max()}")
        print(f"Umidade média: {df_limpo['umidade_solo'].mean():.1f}%")
        print(f"pH médio: {df_limpo['ph_solo'].mean():.1f}")
        print(f"Irrigações realizadas: {df_limpo['irrigacao_ativa'].sum()}")
        print(f"Arquivo salvo em: {arquivo_limpo}")
        
        return df_limpo
        
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        return None

def gerar_dados_adicionais():
    """
    Gera dados adicionais para demonstração (opcional)
    """
    
    print("\nGerando dados adicionais para demonstração...")
    
    # Criar dados sintéticos baseados nos padrões da Fase 2
    from datetime import timedelta
    
    dados_extras = []
    base_time = datetime(2025, 10, 2, 8, 0, 0)  # Dia seguinte
    
    for i in range(24):  # 24 horas
        timestamp = base_time + timedelta(hours=i)
        
        # Simular variações realistas
        umidade = np.random.normal(65, 15)  # Média 65%, desvio 15%
        umidade = max(30, min(90, umidade))  # Entre 30% e 90%
        
        ph = np.random.normal(6.4, 0.3)  # pH ideal para soja
        ph = max(5.5, min(7.5, ph))
        
        # NPK aleatório mas correlacionado
        npk = np.random.choice([0, 1], size=3, p=[0.3, 0.7])
        
        # Temperatura varia ao longo do dia
        temp_base = 25 + 8 * np.sin((i - 6) * np.pi / 12)  # Ciclo diário
        temperatura = temp_base + np.random.normal(0, 2)
        
        # Chuva ocasional
        chuva = np.random.exponential(0.5) if np.random.random() < 0.2 else 0
        
        # Irrigação baseada na umidade
        irrigacao = 1 if umidade < 55 and chuva < 0.5 else 0
        
        dados_extras.append({
            'timestamp': timestamp,
            'umidade_solo': round(umidade, 1),
            'ph_solo': round(ph, 1),
            'nitrogenio': npk[0],
            'fosforo': npk[1],
            'potassio': npk[2],
            'temperatura': round(temperatura, 1),
            'chuva_mm': round(chuva, 1),
            'irrigacao_ativa': irrigacao
        })
    
    # Salvar dados extras
    df_extras = pd.DataFrame(dados_extras)
    df_extras.to_csv("database/dados_extras_demo.csv", index=False)
    
    print(f"Gerados {len(dados_extras)} registros adicionais")
    print("Salvos em: database/dados_extras_demo.csv")
    
    return df_extras

def main():
    """
    Função principal
    """
    print("FarmTech Solutions - Preparação de Dados para Oracle")
    print("=" * 60)
    
    # Criar diretório se não existir
    os.makedirs("database", exist_ok=True)
    
    # Limpar dados originais
    df_limpo = limpar_dados_sensores()
    
    if df_limpo is not None:
        print("\nDados preparados com sucesso!")
        print("\nPRÓXIMOS PASSOS:")
        print("1. Abrir Oracle SQL Developer")
        print("2. Conectar com as credenciais FIAP")
        print("3. Importar o arquivo: database/dados_sensores_limpos.csv")
        print("4. Executar as consultas SQL do arquivo: database/consultas_sql.sql")
        
        # Gerar dados extras (opcional)
        resposta = input("\nDeseja gerar dados adicionais para demonstração? (s/n): ")
        if resposta.lower() == 's':
            gerar_dados_adicionais()
    
    print("\nPreparação concluída!")

if __name__ == "__main__":
    main()