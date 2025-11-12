import os
import streamlit.components.v1 as components

# Obtém o diretório do componente
_component_dir = os.path.dirname(os.path.abspath(__file__))
_build_dir = os.path.join(_component_dir, "frontend", "dist")

# Declara FORA da função para evitar re-declaração
_component_func = None

def action_plan_component(key=None):
    """Componente ACTION PLAN"""
    global _component_func
    
    if _component_func is None:
        try:
            _component_func = components.declare_component(
                "action_plan_comp",
                path=_build_dir
            )
        except:
            index_path = os.path.join(_build_dir, "index.html")
            with open(index_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            return components.html(html_content, height=900, scrolling=True)
    
    return _component_func(key=key)