import streamlit as st
import pandas as pd

def folha_mestre():
    if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
        st.warning("❗ Nenhuma peça carregada. Vá para 'Gerenciar Relatórios' primeiro.")
        return

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca']

    # Convertendo as colunas Desvio, Tol+, Tol- para numéricas, tratando vírgula como separador decimal
    for col in ["Desvio", "Tol+", "Tol-"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors='coerce')

    st.title(f"📊 Folha Mestre - {peca['Nome']} ({peca['PartNumber']})")

    # Verificando se o desvio está dentro da tolerância para cada ponto
    pontos = df.groupby("NomePonto").apply(
        lambda g: all((g["Desvio"] >= g["Tol-"]) & (g["Desvio"] <= g["Tol+"]))  
    )
    total_pontos = len(pontos)
    pontos_aprovados = pontos.sum()
    pct_aprovado = (pontos_aprovados / total_pontos * 100) if total_pontos > 0 else 0

    if not df.empty:
        sigma = df["Desvio"].std(ddof=1)  # Desvio padrão
        media = df["Desvio"].mean()  # Média
        USL = df["Tol+"].max()  # Limite Superior de Tolerância
        LSL = df["Tol-"].min()  # Limite Inferior de Tolerância

        # Cálculo do CP (Índice de Capacidade de Processo)
        cp = (USL - LSL) / (6 * sigma) if sigma > 0 else 0

        # Cálculo do CPK (Índice de Capacidade de Processo em termos de desvio médio)
        cpk = min((USL - media) / (3 * sigma), (media - LSL) / (3 * sigma)) if sigma > 0 else 0
    else:
        cp, cpk = 0, 0

    # Função para verificar se CP é bom (≥ 1.33)
    def cp_bom(grupo):
        std = grupo["Desvio"].std(ddof=0) if len(grupo) > 1 else 1
        return ((grupo["Tol+"].max() - grupo["Tol-"].min()) / (6 * std)) >= 1.33

    # Função para verificar se CPK é bom (≥ 1.33)
    def cpk_bom(grupo):
        std = grupo["Desvio"].std(ddof=0) if len(grupo) > 1 else 1
        media = grupo["Desvio"].mean()
        return (min(grupo["Tol+"].max() - media, media - grupo["Tol-"].min()) / (3 * std)) >= 1.33

    cp_bom_count = df.groupby("NomePonto").apply(cp_bom).sum()
    cpk_bom_count = df.groupby("NomePonto").apply(cpk_bom).sum()

    pct_cp_bom = (cp_bom_count / total_pontos * 100) if total_pontos > 0 else 0
    pct_cpk_bom = (cpk_bom_count / total_pontos * 100) if total_pontos > 0 else 0

    # -------------------------------
    # Sua Tabela Original
    # -------------------------------
    tabela = pd.DataFrame({
        "Indicador": ["QH", "CP", "CPK"],
        "Pontos Aprovados": [pontos_aprovados, cp_bom_count, cpk_bom_count],
        "Porcentagem": [pct_aprovado, pct_cp_bom, pct_cpk_bom]
    })
    tabela = tabela.set_index("Indicador")

    # -------------------------------
    # Adicionando as novas colunas para "Pontos Fora da Tolerância" e CP/CPK ruim
    # -------------------------------
    pontos_fora_tol = ((df["Desvio"] < df["Tol-"]) | (df["Desvio"] > df["Tol+"])).sum()
    pontos_cp_ruim = df.groupby("NomePonto").apply(lambda g: not cp_bom(g)).sum()
    pontos_cpk_ruim = df.groupby("NomePonto").apply(lambda g: not cpk_bom(g)).sum()

    pct_fora_tol = (pontos_fora_tol / len(df) * 100) if len(df) > 0 else 0
    pct_cp_ruim = (pontos_cp_ruim / total_pontos * 100) if total_pontos > 0 else 0
    pct_cpk_ruim = (pontos_cpk_ruim / total_pontos * 100) if total_pontos > 0 else 0

    # Adicionando as novas colunas na tabela
    tabela["Pontos Fora Tolerância"] = [pontos_fora_tol, "", ""]
    tabela["% Fora Tolerância"] = [f"{pct_fora_tol:.1f}%", "", ""]
    tabela["Pontos CP Ruim"] = [pontos_cp_ruim, "", ""]
    tabela["% CP Ruim"] = [f"{pct_cp_ruim:.1f}%", "", ""]
    tabela["Pontos CPK Ruim"] = [pontos_cpk_ruim, "", ""]
    tabela["% CPK Ruim"] = [f"{pct_cpk_ruim:.1f}%", "", ""]

    # Reorganiza a tabela com as novas colunas
    tabela = tabela[[
        "Pontos Aprovados", "Porcentagem", 
        "Pontos Fora Tolerância", "% Fora Tolerância", 
        "Pontos CP Ruim", "% CP Ruim", 
        "Pontos CPK Ruim", "% CPK Ruim"
    ]]

    # Estilizando a tabela (mantendo o verde para os "Aprovados")
    def colorir_verde(val):
        return 'background-color: #8fcf79'

    tabela["Porcentagem"] = tabela["Porcentagem"].apply(lambda x: f"{x:.1f}%")
    tabela_style = tabela.style.applymap(colorir_verde, subset=["Pontos Aprovados", "Porcentagem"])

    # Exibindo a tabela
    st.dataframe(tabela_style, use_container_width=True)

    # -------------------------------
    # Resumo
    # -------------------------------
    st.write("📈 Resumo")
    st.write(f"Total de pontos analisados: {total_pontos}")
    st.write(f"🟩 Dentro da tolerância (QH): {pontos_aprovados} ({pct_aprovado:.1f}%)")
    st.write(f"🟥 Fora da tolerância: {pontos_fora_tol} ({pct_fora_tol:.1f}%)")
    st.write(f"📊 Total de pontos com CP bom: {cp_bom_count} ({pct_cp_bom:.1f}%)")
    st.write(f"📊 Total de pontos com CPK bom: {cpk_bom_count} ({pct_cpk_bom:.1f}%)")
    st.write(f"📊 CP global = {cp:.2f} | CPK global = {cpk:.2f}")
