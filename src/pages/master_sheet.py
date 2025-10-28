import streamlit as st
import pandas as pd

def folha_mestre():
    if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
        st.warning("❗ Nenhuma peça carregada. Vá para 'Gerenciar Relatórios' primeiro.")
        return

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca']

    for col in ["Desvio", "Tol+", "Tol-"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors='coerce')

    st.title(f"📊 Folha Mestre - {peca['Nome']} ({peca['PartNumber']})")

    pontos = df.groupby("NomePonto").apply(
        lambda g: all((g["Desvio"] >= g["Tol-"]) & (g["Desvio"] <= g["Tol+"]))
    )
    total_pontos = len(pontos)
    pontos_aprovados = pontos.sum()
    pct_aprovado = (pontos_aprovados / total_pontos * 100) if total_pontos > 0 else 0

    if not df.empty:
        sigma = df["Desvio"].std(ddof=1)  
        media = df["Desvio"].mean()
        USL = df["Tol+"].max()
        LSL = df["Tol-"].min()

        cp = (USL - LSL) / (6 * sigma) if sigma > 0 else 0
        cpk = min((USL - media) / (3 * sigma), (media - LSL) / (3 * sigma)) if sigma > 0 else 0
    else:
        cp, cpk = 0, 0

    def cp_bom(grupo):
        std = grupo["Desvio"].std(ddof=0) if len(grupo) > 1 else 1
        return ((grupo["Tol+"].max() - grupo["Tol-"].min()) / (6 * std)) >= 1.33

    def cpk_bom(grupo):
        std = grupo["Desvio"].std(ddof=0) if len(grupo) > 1 else 1
        media = grupo["Desvio"].mean()
        return (min(grupo["Tol+"].max() - media, media - grupo["Tol-"].min()) / (3 * std)) >= 1.33

    cp_bom_count = df.groupby("NomePonto").apply(cp_bom).sum()
    cpk_bom_count = df.groupby("NomePonto").apply(cpk_bom).sum()

    pct_cp_bom = (cp_bom_count / total_pontos * 100) if total_pontos > 0 else 0
    pct_cpk_bom = (cpk_bom_count / total_pontos * 100) if total_pontos > 0 else 0

    tabela = pd.DataFrame({
        "Indicador": ["QH", "CP", "CPK"],
        "Pontos Aprovados": [pontos_aprovados, cp_bom_count, cpk_bom_count],
        "Porcentagem": [pct_aprovado, pct_cp_bom, pct_cpk_bom]
    })
    tabela = tabela.set_index("Indicador")

    def colorir_verde(val):
        return 'background-color: #8fcf79' 

    tabela["Porcentagem"] = tabela["Porcentagem"].apply(lambda x: f"{x:.1f}%")
    tabela_style = tabela.style.applymap(colorir_verde, subset=["Pontos Aprovados", "Porcentagem"])

    st.dataframe(tabela_style, use_container_width=True)

    st.write("📈 Resumo")
    st.write(f"Total de pontos analisados: {total_pontos}")
    st.write(f"🟩 Dentro da tolerância (QH): {pontos_aprovados} ({pct_aprovado:.1f}%)")
    st.write(f"🟥 Fora da tolerância: {total_pontos - pontos_aprovados}")
    st.write(f"📊 Total de pontos com CP bom: {cp_bom_count} ({pct_cp_bom:.1f}%)")
    st.write(f"📊 Total de pontos com CPK bom: {cpk_bom_count} ({pct_cpk_bom:.1f}%)")
    st.write(f"📊 CP global = {cp:.2f} | CPK global = {cpk:.2f}")
