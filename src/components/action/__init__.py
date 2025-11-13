import os
import streamlit.components.v1 as components
import json

def action_plan_component(pontos=None, dados_por_ponto=None, info_peca=None, key=None):
    """Componente ACTION PLAN"""
    
    if pontos is None:
        pontos = []
    if dados_por_ponto is None:
        dados_por_ponto = {}
    if info_peca is None:
        info_peca = {}
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, "frontend", "dist")
    index_path = os.path.join(build_dir, "index.html")
    
    if not os.path.exists(index_path):
        import streamlit as st
        st.error(f"❌ Build não encontrado: {index_path}")
        st.info("Execute: cd src/components/action/frontend && npm run build")
        st.stop()
    
    with open(index_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    html_with_data = f"""
    {html_content}
    <script>
        window.STREAMLIT_DATA = {json.dumps({
            'pontos': pontos,
            'dadosPorPonto': dados_por_ponto,
            'infoPeca': info_peca
        })};
        console.log('📊 Dados carregados no React:', window.STREAMLIT_DATA);
    </script>
    """
    
    return components.html(html_with_data, height=900, scrolling=True)

