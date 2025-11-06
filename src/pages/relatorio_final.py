import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent  # src/
HTML_FILE = BASE_DIR / "assets" / "html" / "index.html"
CSS_FILE  = BASE_DIR / "assets" / "css"  / "styles.css"
JS_FILE   = BASE_DIR / "assets" / "js"   / "main.js"

def relatorio_final():
    st.set_page_config(page_title="Relatório Final", layout="wide")

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css_content = f"<style>{f.read()}</style>"

    with open(JS_FILE, "r", encoding="utf-8") as f:
        js_content = f"<script>{f.read()}</script>"

    st.components.v1.html(css_content + html_content + js_content,
                         height=900, scrolling=True)

if __name__ == "__main__":
    relatorio_final()

