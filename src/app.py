import streamlit as st
import pandas as pd
import os

def cadastrar_peca():
    st.title("🧾 Cadastrar Peça")

    nome = st.text_input("Part Name")
    col1, col2 = st.columns([1, 1])

    with col1:
        numero = st.text_input("Part Number (único)")
    with col2:
        modelo = st.text_input("Modelo")

    if st.button("Salvar"):
        if not nome or not numero or not modelo:
            st.warning("❗ Todos os campos são obrigatórios!")
            return

        base_path = "dados/base_pecas.xlsx"
        df = pd.read_excel(base_path) if os.path.exists(base_path) else pd.DataFrame(
            columns=["ID","Nome","PartNumber","Modelo","DataCadastro","PastaTXT","Status"]
        )

        if numero in df["PartNumber"].astype(str).values:
            st.warning("❗ Já existe uma peça com esse Part Number.")
            return

        new_id = 1 if df.empty else df["ID"].max() + 1
        pasta_txt = f"dados/peca_{new_id}/txt"
        os.makedirs(pasta_txt, exist_ok=True)

        nova = {
            "ID": new_id,
            "Nome": nome,
            "PartNumber": numero,
            "Modelo": modelo,
            "DataCadastro": pd.Timestamp.now(),
            "PastaTXT": pasta_txt,
            "Status": "Ativa"
        }

        df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
        df.to_excel(base_path, index=False)

        st.success(f"Peça '{nome}' cadastrada com sucesso!")

def gerenciar_relatorios():
    st.title("⚙️ Gerenciar Relatórios TXT da Peça")

    base_path = "dados/base_pecas.xlsx"
    if not os.path.exists(base_path):
        st.warning("❗ Base de peças não encontrada.")
        return

    base = pd.read_excel(base_path)
    base["PartNumber"] = base["PartNumber"].astype(str)

    part_number = st.text_input("Digite o Part Number da peça:")
    if not part_number:
        st.stop()

    peca = base.loc[base["PartNumber"] == str(part_number)]
    if peca.empty:
        st.warning("Peça não encontrada.")
        st.stop()

    peca = peca.iloc[0]
    pasta_txt = peca["PastaTXT"]
    os.makedirs(pasta_txt, exist_ok=True)

    st.subheader(f"📄 {peca['Nome']} ({peca['PartNumber']}) - {peca['Modelo']}")

    arquivos = os.listdir(pasta_txt)
    if arquivos:
        st.write("Relatórios armazenados:")
        st.table(pd.DataFrame(arquivos, columns=["Arquivos TXT"]))
    else:
        st.info("Nenhum relatório importado ainda.")

    col1, col2 = st.columns([1, 2])

    with col1:
        uploads = st.file_uploader("📥 Importar novos relatórios TXT", type=["txt"], accept_multiple_files=True, label_visibility="collapsed")
        if uploads:
            for file in uploads:
                caminho = os.path.join(pasta_txt, file.name)
                with open(caminho, "wb") as f:
                    f.write(file.read())
            st.success(f"{len(uploads)} arquivo(s) importado(s) com sucesso!")

    with col2:
        if arquivos:
            excluir = st.multiselect("Selecione relatórios para excluir:", arquivos)
            if st.button("🗑️"):
                if not excluir:
                    st.warning("❗ Nenhum relatório selecionado para exclusão.")
                else:
                    for arq in excluir:
                        caminho = os.path.join(pasta_txt, arq)
                        if os.path.exists(caminho):
                            os.remove(caminho)
                    st.success(f"{len(excluir)} arquivo(s) excluído(s) com sucesso!")
        else:
            st.info("Nenhum relatório disponível para exclusão.")

# ---------------------- Layout principal ----------------------
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Escolha uma opção:", ["Cadastrar Peça", "Gerenciar Relatórios"])

if opcao == "Cadastrar Peça":
    cadastrar_peca()
else:
    gerenciar_relatorios()
