import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="React Test", layout="wide")
_RELEASE = True 

if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "..", "components", "action", "frontend", "dist")
    build_dir = os.path.abspath(build_dir) 
else:
    build_dir = "http://localhost:5173"

if _RELEASE and not os.path.exists(build_dir):
    st.error(f"❌ Diretório não encontrado: {build_dir}")
    st.stop()

st.write("📂 Caminho do build_dir:", build_dir)
if _RELEASE:
    st.write("📁 Conteúdo da pasta:", os.listdir(build_dir))

action_component = components.declare_component(
    "action",
    path=build_dir if _RELEASE else None,
    url=build_dir if not _RELEASE else None
)

valor = action_component(default="Aguardando...", key="action_comp")
st.write("Valor retornado:", valor)