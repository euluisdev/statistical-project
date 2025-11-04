import streamlit as st

#estrutura final
if "relatorio_final" not in st.session_state:
    st.session_state["relatorio_final"] = [
        {"id": 1, "titulo": "Página 1", "imagem": None, "texto": ""}
    ]

#Lista imagens 
if "trend_pages" not in st.session_state:
    st.session_state["trend_pages"] = []

def criar_nova_pagina():
    nova_id = len(st.session_state["relatorio_final"]) + 1
    st.session_state["relatorio_final"].append({
        "id": nova_id, "titulo": f"Página {nova_id}", "imagem": None, "texto": ""
    })

#Layout
st.title("📄 Relatório Final")

col1, col2 = st.columns([1, 3])

#Miniaturas
with col1:
    st.subheader("🖼️ Miniaturas")
    for idx, pagina in enumerate(st.session_state["relatorio_final"]):
        if st.button(pagina["titulo"], key=f"thumb_{idx}"):
            st.session_state["pagina_selecionada"] = idx

if "pagina_selecionada" not in st.session_state:
    st.session_state["pagina_selecionada"] = 0

pagina_atual = st.session_state["relatorio_final"][st.session_state["pagina_selecionada"]]


#Edição da Página
with col2:
    st.subheader(f"📌 {pagina_atual['titulo']}")

    if pagina_atual["imagem"]:
        st.image(pagina_atual["imagem"], use_container_width=True)
    else:
        st.info("Nenhuma imagem adicionada ainda.")

    nomes_imagens = [img["nome"] for img in st.session_state["trend_pages"]]
    arquivos_imagens = {img["nome"]: img["arquivo"] for img in st.session_state["trend_pages"]}

    if nomes_imagens:
        img_escolhida = st.selectbox("Selecionar gráfico salvo:", nomes_imagens)
        if st.button("📌 Inserir imagem nesta página"):
            pagina_atual["imagem"] = arquivos_imagens[img_escolhida]
            st.success("Imagem adicionada!")
    else:
        st.warning("Nenhuma imagem disponível. Gere gráficos na página Trend.")

    pagina_atual["texto"] = st.text_area("Texto nesta página:", pagina_atual["texto"], height=100)

    if st.button("➕ Criar nova página"):
        criar_nova_pagina()
        st.rerun()
