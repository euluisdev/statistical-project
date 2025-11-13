import os
import streamlit.components.v1 as components

# Caminho do build
_component_dir = os.path.dirname(os.path.abspath(__file__))
_build_dir = os.path.join(_component_dir, "frontend", "dist")

# Declara o componente UMA VEZ
_component_func = None

def action_plan_component(pontos=None, dados_por_ponto=None, info_peca=None, key=None):
    """Componente ACTION PLAN"""
    global _component_func
    
    # Valores padrão
    if pontos is None:
        pontos = []
    if dados_por_ponto is None:
        dados_por_ponto = {}
    if info_peca is None:
        info_peca = {}
    
    # Declara apenas uma vez
    if _component_func is None:
        try:
            _component_func = components.declare_component(
                "action_plan",
                path=_build_dir
            )
        except Exception as e:
            import streamlit as st
            st.error(f"Erro ao declarar componente: {e}")
            st.stop()
    
    # Chama o componente passando os dados como argumentos
    return _component_func(
        pontos=pontos,
        dados_por_ponto=dados_por_ponto,
        info_peca=info_peca,
        key=key,
        default=None
    )