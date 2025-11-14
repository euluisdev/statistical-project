import os
import streamlit.components.v1 as components

_component_dir = os.path.dirname(os.path.abspath(__file__))
_build_dir = os.path.join(_component_dir, "frontend", "dist")

_component_func = None

def action_plan_component(pontos=None, dados_por_ponto=None, info_peca=None, dataframe_completo=None, key=None):
    """Componente ACTION PLAN"""
    global _component_func
    
    if pontos is None:
        pontos = []
    if dados_por_ponto is None:
        dados_por_ponto = {}
    if info_peca is None:
        info_peca = {}
    if dataframe_completo is None:
        dataframe_completo = []
    
    if _component_func is None:
        _component_func = components.declare_component(
            "action_plan",
            path=_build_dir
        )

    return _component_func(
        pontos=pontos,
        dadosPorPonto=dados_por_ponto,
        infoPeca=info_peca,
        dataframeCompleto=dataframe_completo,
        key=key,
        default=None
    )