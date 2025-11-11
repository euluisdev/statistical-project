import streamlit as st
import pandas as pd
import os
from utils.parser_txt import ler_relatorio_pcdmis  


def reports():
    st.title("GERENCIAR REPORTS")

    base_path = "dados/base_pecas.xlsx"
    if not os.path.exists(base_path):
        st.warning("❗ Base de peças não encontrada.")
        return

    base = pd.read_excel(base_path)
    base["PartNumber"] = base["PartNumber"].astype(str)
    opcoes = base["PartNumber"].astype(str).tolist()

    if not opcoes:
        st.warning("❗ Nenhuma peça cadastrada ainda.")
        st.stop()

    col_sel, col_btn = st.columns([3, 1])

    with col_sel:
        escolha = st.selectbox(
            "",
            options=["Selecione a peça..."] + opcoes,
            index=0,
            label_visibility="collapsed"
        )

    with col_btn:
        if st.button("🔍 Exibir", use_container_width=True):
            if escolha != "Selecione a peça...":
                st.session_state["part_number_selected"] = escolha
            else:
                st.warning("Escolha uma peça válida antes de exibir.")

    part_number = st.session_state.get("part_number_selected", None)

    if not part_number:
        st.info("Selecione uma peça e clique em 'Exibir' para continuar.")
        return

    peca = base.loc[base["PartNumber"] == str(part_number)]
    if peca.empty:
        st.warning("Peça não encontrada.")
        return

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
        uploads = st.file_uploader(
            "📥 Importar novos relatórios TXT",
            type=["txt"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        if uploads:
            for file in uploads:
                caminho = os.path.join(pasta_txt, file.name)
                with open(caminho, "wb") as f:
                    f.write(file.read())
            st.success(f"{len(uploads)} arquivo(s) importado(s) com sucesso!")
            st.rerun()

    with col2:
        if arquivos:
            col_excluir1, col_excluir2 = st.columns([3, 1])
            with col_excluir1:
                excluir = st.multiselect("Selecione relatórios para excluir:", arquivos)
            with col_excluir2:
                if st.button("🗑️ Excluir"):
                    if not excluir:
                        st.warning("❗ Nenhum relatório selecionado para exclusão.")
                    else:
                        for arq in excluir:
                            caminho = os.path.join(pasta_txt, arq)
                            if os.path.exists(caminho):
                                os.remove(caminho)
                        st.success(f"{len(excluir)} arquivo(s) excluído(s) com sucesso!")
                        st.rerun()
        else:
            st.info("Nenhum relatório disponível para exclusão.")

    st.divider()
    st.subheader("📈 Extrair Dados dos Relatórios TXT")

    if arquivos:
        if st.button("📤 Ler e Extrair Dados"):
            df_total = pd.DataFrame()
            for nome_arquivo in arquivos:
                caminho = os.path.join(pasta_txt, nome_arquivo)
                df = ler_relatorio_pcdmis(caminho)
                df["Relatorio"] = nome_arquivo
                df_total = pd.concat([df_total, df], ignore_index=True)

            arquivo_analise = os.path.join(os.path.dirname(pasta_txt), "analise.xlsx")
            df_total.to_excel(arquivo_analise, index=False)
            st.success(f"✅ Dados extraídos e salvos em '{arquivo_analise}'")

            st.session_state["peca_atual"] = peca
            st.session_state["df_peca"] = df_total
            st.dataframe(df_total)
        else:
            arquivo_analise = os.path.join(os.path.dirname(pasta_txt), "analise.xlsx")
            if os.path.exists(arquivo_analise):
                st.info("📊 Dados extraídos anteriormente:")
                st.dataframe(pd.read_excel(arquivo_analise))
    else:
        st.info("Nenhum relatório disponível para extração.")
