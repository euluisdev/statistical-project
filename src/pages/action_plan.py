import streamlit as st
import streamlit.components.v1 as components
import os
import sys
import json

st.set_page_config(page_title="ACTION PLAN", layout="wide")

st.markdown("""
    <style>
        .block-container {
          padding-top: 3rem;
          padding-bottom: 1rem;
          padding-left: 1rem;
          padding-right: 1rem;
        }
    </style>
 """, unsafe_allow_html=True)

# ✅ VERIFICA SE HÁ DADOS NO SESSION_STATE
if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
    st.warning("❗ Nenhuma peça carregada. Vá para 'Gerenciar Relatórios' primeiro.")
    if st.button("← Voltar para Reports"):
        st.switch_page("pages/reports.py")
    st.stop()

# ✅ PEGA OS DADOS DO SESSION_STATE
peca = st.session_state['peca_atual']
df = st.session_state['df_peca'].copy()

# ✅ HEADER COM INFO DA PEÇA
col1, col2 = st.columns([5, 1])
with col1:
    st.title(f"📋 Action Plan - {peca.get('Nome', 'N/A')} ({peca.get('PartNumber', 'N/A')})")
with col2:
    if st.button("← Voltar", use_container_width=True):
        st.switch_page("pages/reports.py")

st.divider()

# ✅ CRIA LISTA DE PONTOS COM EIXO (PontoEixo)
if "Eixo" in df.columns and "NomePonto" in df.columns:
    df["PontoEixo"] = df["NomePonto"].astype(str) + " - " + df["Eixo"].astype(str)
    pontos_unicos = df["PontoEixo"].unique().tolist()
else:
    pontos_unicos = df['NomePonto'].unique().tolist() if 'NomePonto' in df.columns else []

# ✅ CONVERTE DATAFRAME COMPLETO PARA JSON (todos os dados)
df_json = df.to_dict('records')

# ✅ AGRUPA DADOS POR PONTO+EIXO
dados_por_ponto = {}
for ponto_eixo in pontos_unicos:
    df_ponto = df[df['PontoEixo'] == ponto_eixo] if 'PontoEixo' in df.columns else df[df['NomePonto'] == ponto_eixo]
    
    if not df_ponto.empty:
        primeira_linha = df_ponto.iloc[0]
        dados_por_ponto[ponto_eixo] = {
            'data': str(primeira_linha.get('Data', '')),
            'hora': str(primeira_linha.get('Hora', '')),
            'localizacao': str(primeira_linha.get('Localização', '')),
            'tipo_geo': str(primeira_linha.get('TipoGeométrico', '')),
            'nome_ponto': str(primeira_linha.get('NomePonto', '')),
            'eixo': str(primeira_linha.get('Eixo', '')),
            'nominal': float(primeira_linha.get('Nominal', 0)) if primeira_linha.get('Nominal') else 0,
            'medido': float(primeira_linha.get('Medido', 0)) if primeira_linha.get('Medido') else 0,
            'desvio': float(primeira_linha.get('Desvio', 0)) if primeira_linha.get('Desvio') else 0,
            'tol_mais': float(primeira_linha.get('Tol+', 0)) if primeira_linha.get('Tol+') else 0,
            'tol_menos': float(primeira_linha.get('Tol-', 0)) if primeira_linha.get('Tol-') else 0,
            'relatorio': str(primeira_linha.get('Relatorio', ''))
        }

info_peca = {
    'nome': str(peca.get('Nome', 'N/A')),
    'part_number': str(peca.get('PartNumber', 'N/A')),
    'modelo': str(peca.get('Modelo', 'N/A'))
}

# 1 add dir src ao path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

#2 import
try:
    from components.action import action_plan_component
    
    #passando todo df
    action_plan_component(
        pontos=pontos_unicos,
        dados_por_ponto=dados_por_ponto,
        info_peca=info_peca,
        dataframe_completo=df_json,  #df
        key="action_plan_main"
    )
    
except ImportError as e:
    st.error(f"Erro ao importar: {e}")
    st.info(f"Diretório src: {src_dir}")
    st.info(f"sys.path: {sys.path}")