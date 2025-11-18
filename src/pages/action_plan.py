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

if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
    st.warning("Nenhuma peça carregada. Vá para 'Gerenciar Relatórios' primeiro.")
    if st.button("← Voltar para Reports"):
        st.switch_page("pages/reports.py")
    st.stop()

peca = st.session_state['peca_atual']
df = st.session_state['df_peca'].copy()

col1, col2 = st.columns([5, 1])
with col1:
    st.title(f"Action Plan - {peca.get('Nome', 'N/A')} ({peca.get('PartNumber', 'N/A')})")
with col2:
    if st.button("← Voltar", use_container_width=True):
        st.switch_page("pages/reports.py")

st.divider()

if "Eixo" in df.columns and "NomePonto" in df.columns:
    df["PontoEixo"] = df["NomePonto"].astype(str) + " - " + df["Eixo"].astype(str)
    pontos_unicos = df["PontoEixo"].unique().tolist()
else:
    pontos_unicos = df['NomePonto'].unique().tolist() if 'NomePonto' in df.columns else []

df_json = df.to_dict('records')

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

part_number = peca.get('PartNumber', 'N/A')
pasta_peca = f"dados/peca_{part_number}"
arquivo_acoes = os.path.join(pasta_peca, "action_plans.json")

acoes_salvas = []
if os.path.exists(arquivo_acoes):
    try:
        with open(arquivo_acoes, 'r', encoding='utf-8') as f:
            acoes_salvas = json.load(f)
        st.success(f"✅ {len(acoes_salvas)} ação(ões) carregada(s)")
    except Exception as e:
        st.error(f"Erro ao carregar ações: {e}")

#callback p salvar ações - vindo do react pelo streamlit 
if 'save_action_trigger' in st.session_state and st.session_state.save_action_trigger:
    action_data = st.session_state.get('action_to_save', None)
    
    if action_data:
        try:
            #create folder
            os.makedirs(pasta_peca, exist_ok=True)
            
            # load actions
            if os.path.exists(arquivo_acoes):
                with open(arquivo_acoes, 'r', encoding='utf-8') as f:
                    acoes_salvas = json.load(f)
            else:
                acoes_salvas = []
            
            #add new actions
            acoes_salvas.append(action_data)
            
            #  save file
            with open(arquivo_acoes, 'w', encoding='utf-8') as f:
                json.dump(acoes_salvas, f, ensure_ascii=False, indent=2)
            
            st.success("Plano de Ação salvo com sucesso!")
            st.session_state.save_action_trigger = False
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erro ao salvar ação: {e}")

# 1
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

#2 import
try:
    from components.action import action_plan_component
    
    result = action_plan_component(
        pontos=pontos_unicos,
        dados_por_ponto=dados_por_ponto,
        info_peca=info_peca,
        dataframe_completo=df_json,  #df
        acoes_salvas=acoes_salvas, 
        pasta_peca=pasta_peca, 
        key="action_plan_main"
    )

    if result and isinstance(result, dict) and result.get('action') == 'save':
      st.session_state.action_to_save = result.get('data')
      st.session_state.save_action_trigger = True
      st.rerun()
    
except ImportError as e:
    st.error(f"Erro ao importar: {e}")
    st.info(f"Diretório src: {src_dir}")
    st.info(f"sys.path: {sys.path}")
