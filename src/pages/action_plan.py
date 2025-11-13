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

# ✅ VERIFICA SE HÁ DADOS NO SESSION_STATE (igual folha_mestre)
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

# ✅ PROCESSA DADOS PARA O REACT
pontos_unicos = df['NomePonto'].unique().tolist() if 'NomePonto' in df.columns else []

# Agrupa dados por ponto
dados_por_ponto = {}
for ponto in pontos_unicos:
    df_ponto = df[df['NomePonto'] == ponto]
    
    medicoes = []
    for _, row in df_ponto.iterrows():
        medicoes.append({
            'eixo': str(row.get('Eixo', '')),
            'nominal': float(row.get('Nominal', 0)) if row.get('Nominal') else 0,
            'medido': float(row.get('Medido', 0)) if row.get('Medido') else 0,
            'desvio': float(row.get('Desvio', 0)) if row.get('Desvio') else 0,
            'tol_mais': float(row.get('Tol+', 0)) if row.get('Tol+') else 0,
            'tol_menos': float(row.get('Tol-', 0)) if row.get('Tol-') else 0,
        })
    
    dados_por_ponto[ponto] = {
        'localizacao': str(df_ponto['Localização'].iloc[0]) if 'Localização' in df_ponto.columns else '',
        'tipo_geo': str(df_ponto['TipoGeométrico'].iloc[0]) if 'TipoGeométrico' in df_ponto.columns else '',
        'medicoes': medicoes
    }

info_peca = {
    'nome': str(peca.get('Nome', 'N/A')),
    'part_number': str(peca.get('PartNumber', 'N/A')),
    'modelo': str(peca.get('Modelo', 'N/A'))
}

# ✅ SALVA OS DADOS PROCESSADOS NO SESSION_STATE PARA O COMPONENTE USAR
st.session_state['react_data'] = {
    'pontos': pontos_unicos,
    'dadosPorPonto': dados_por_ponto,
    'infoPeca': info_peca,
    'totalMedicoes': len(df)
}

# 1. Add dir src ao path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 2. Import
try:
    from components.action import action_plan_component
    
    # ✅ PASSA OS DADOS PARA O COMPONENTE
    action_plan_component(
        pontos=pontos_unicos,
        dados_por_ponto=dados_por_ponto,
        info_peca=info_peca,
        key="action_plan_main"
    )
    
except ImportError as e:
    st.error(f"Erro ao importar: {e}")
    st.info(f"Diretório src: {src_dir}")
    st.info(f"sys.path: {sys.path}")