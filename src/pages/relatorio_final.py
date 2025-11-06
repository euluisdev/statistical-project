import streamlit as st
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent  # volta de /pages para /src

def load_template():
    template_path = BASE_PATH / "assets/html/template.html"
    return template_path.read_text(encoding="utf-8")

def load_css():
    css_path = BASE_PATH / "assets/css/styles.css"
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

def load_js():
    js_path = BASE_PATH / "assets/js/script.js"
    st.markdown(f"<script>{js_path.read_text()}</script>", unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide", page_title="Relatório estilo PowerPoint")

    load_css()
    load_js()
    html_template = load_template()

    st.markdown(html_template, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
