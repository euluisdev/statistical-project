import streamlit as st
import pandas as pd
import os
from utils.parser_txt import ler_relatorio_pcdmis  
from pages.master_sheet import folha_mestre
from pages.trend_chart import trend_chart
from pages.reports import reports
from pages.relatorio_final import relatorio_final
from pages.compliance_piece import compliance_piece
from pages.compliance_cp_cpk import compliance_cp_cpk

# ========================== FUNÇÃO: CADASTRAR PEÇA ==========================
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
        df = (
            pd.read_excel(base_path)
            if os.path.exists(base_path)
            else pd.DataFrame(columns=["ID", "Nome", "PartNumber", "Modelo", "DataCadastro", "PastaTXT", "Status"])
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
            "Status": "Ativa",
        }

        df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
        df.to_excel(base_path, index=False)

        st.success(f"✅ Peça '{nome}' cadastrada com sucesso!")


#GERENCIAR RELATÓRIOS
st.sidebar.title("Menu")
opcao = st.sidebar.radio(
    "Escolha uma opção:",
    ["Cadastrar Peça", "Gerenciar Relatórios", "Folha Mestre", "Trend Chart", "Relatório Final", "Conformidade Peça", "CP / CPK PEÇA"]
)

if opcao == "Cadastrar Peça":
    cadastrar_peca()
elif opcao == "Gerenciar Relatórios":
    reports()
elif opcao == "Folha Mestre":
    folha_mestre()
elif opcao == "Trend Chart":
    trend_chart()
elif opcao == "Relatório Final":
    relatorio_final()
elif opcao == "Conformidade Peça":
    compliance_piece()
elif opcao == "CP / CPK PEÇA":
    compliance_cp_cpk()

