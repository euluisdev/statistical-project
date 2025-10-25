import streamlit as st
import pandas as pd
import os

def cadastrar_peca():
    st.title("🧾 Cadastrar Peça")

    nome = st.text_input("Part Name")
    numero = st.text_input("Part Number")
    modelo = st.text_input("Modelo")

    if st.button("Salvar"):
        base_path = "dados/base_pecas.xlsx"
        df = pd.read_excel(base_path) if os.path.exists(base_path) else pd.DataFrame(columns=["ID","Nome","PartNumber","Modelo","DataCadastro","PastaTXT","Status"])

        # Verifica se o número já existe
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
cadastrar_peca()

st.write("Finished!")