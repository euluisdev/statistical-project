import streamlit as st
import streamlit.components.v1 as components
import os
import sys

st.set_page_config(page_title="ACTION PLAN", layout="wide")

#1 add dir src ao path
src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# 2import
try:
    from components.action import action_plan_component
    action_plan_component(key="action_plan_main")
except ImportError as e:
    st.error(f"Erro ao importar: {e}")
    st.info(f"Diretório src: {src_dir}")
    st.info(f"sys.path: {sys.path}")