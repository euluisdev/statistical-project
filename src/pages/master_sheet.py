import streamlit as st
import pandas as pd
import numpy as np

def folha_mestre():
    if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
        st.warning("❗ Nenhuma peça carregada. Vá para 'Gerenciar Relatórios' primeiro.")
        return

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca'].copy()

    for col in ["Desvio", "Tol+", "Tol-"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors='coerce')

    st.title(f"📊 Folha Mestre - {peca['Nome']} ({peca['PartNumber']})")

    imagem = st.file_uploader("📷 Carregue a imagem da peça", type=["png", "jpg", "jpeg"])
    if imagem:
        st.image(imagem, use_container_width=True)

    if "Eixo" in df.columns:
        df["PontoEixo"] = df["NomePonto"].astype(str) + " - " + df["Eixo"].astype(str)
    else:
        df["PontoEixo"] = df["NomePonto"].astype(str)

    df_media = (
        df.groupby("PontoEixo", as_index=False)
        .agg({
            "Desvio": "mean",
            "Tol+": "max",
            "Tol-": "min"
        })
    )

    df_media["DentroTol"] = (df_media["Desvio"] >= df_media["Tol-"]) & (df_media["Desvio"] <= df_media["Tol+"])

    def eh_proximo(row):
        if not row["DentroTol"]:
            return False
        tol_sup = row["Tol+"]
        tol_inf = row["Tol-"]
        faixa = tol_sup - tol_inf
        if faixa == 0:
            return False
        limite_superior = tol_sup - 0.2 * faixa
        limite_inferior = tol_inf + 0.2 * faixa
        return (row["Desvio"] >= limite_superior) or (row["Desvio"] <= limite_inferior)

    df_media["ProximoTol"] = df_media.apply(eh_proximo, axis=1)
    df_media["Aprovado_Exclusivo"] = df_media["DentroTol"] & (~df_media["ProximoTol"])
    df_media["Reprovado"] = ~df_media["DentroTol"]

    total_pontos = len(df_media)
    qh_aprovados = int(df_media["Aprovado_Exclusivo"].sum())
    qh_proximos = int(df_media["ProximoTol"].sum())
    qh_reprovados = int(df_media["Reprovado"].sum())

    pct_qh_aprov = (qh_aprovados / total_pontos * 100) if total_pontos else 0
    pct_qh_prox = (qh_proximos / total_pontos * 100) if total_pontos else 0
    pct_qh_rep = (qh_reprovados / total_pontos * 100) if total_pontos else 0

    cp_list, cpk_list = [], []

    for ponto in df["PontoEixo"].unique():
        df_ponto = df[df["PontoEixo"] == ponto]

        desvios = df_ponto["Desvio"].values
        sigma = np.std(desvios, ddof=1) if len(desvios) > 1 else 0
        media = np.mean(desvios) if len(desvios) > 0 else 0

        LSL = df_ponto["Tol-"].iloc[0]
        USL = df_ponto["Tol+"].iloc[0]
        tolerancia_total = USL - LSL

        cp_val = tolerancia_total / (6 * sigma) if sigma > 0 else 0
        cpk_val = min((USL - media) / (3 * sigma), (media - LSL) / (3 * sigma)) if sigma > 0 else 0

        cp_list.append((ponto, cp_val))
        cpk_list.append((ponto, cpk_val))

    df_cp = pd.DataFrame(cp_list, columns=["PontoEixo", "CP"])
    df_cpk = pd.DataFrame(cpk_list, columns=["PontoEixo", "CPK"])

    def classifica(val):
        if val < 1:
            return "Reprovado"
        elif 1 <= val < 1.33:
            return "Alerta"
        else:
            return "Aprovado"

    df_cp["Status"] = df_cp["CP"].apply(classifica)
    df_cpk["Status"] = df_cpk["CPK"].apply(classifica)

    cp_aprov = (df_cp["Status"] == "Aprovado").sum()
    cp_alerta = (df_cp["Status"] == "Alerta").sum()
    cp_reprov = (df_cp["Status"] == "Reprovado").sum()
    cp_total = len(df_cp)
    pct_cp_aprov = cp_aprov / cp_total * 100
    pct_cp_alerta = cp_alerta / cp_total * 100
    pct_cp_reprov = cp_reprov / cp_total * 100

    cpk_aprov = (df_cpk["Status"] == "Aprovado").sum()
    cpk_alerta = (df_cpk["Status"] == "Alerta").sum()
    cpk_reprov = (df_cpk["Status"] == "Reprovado").sum()
    cpk_total = len(df_cpk)
    pct_cpk_aprov = cpk_aprov / cpk_total * 100
    pct_cpk_alerta = cpk_alerta / cpk_total * 100
    pct_cpk_reprov = cpk_reprov / cpk_total * 100

    tabela = pd.DataFrame({
        "Indicador": ["QH", "CP", "CPK"],
        "Aprovados": [qh_aprovados, cp_aprov, cpk_aprov],
        "% Aprov.": [f"{pct_qh_aprov:.1f}%", f"{pct_cp_aprov:.1f}%", f"{pct_cpk_aprov:.1f}%"],
        "Alerta": [qh_proximos, cp_alerta, cpk_alerta],
        "% Alerta": [f"{pct_qh_prox:.1f}%", f"{pct_cp_alerta:.1f}%", f"{pct_cpk_alerta:.1f}%"],
        "Reprovados": [qh_reprovados, cp_reprov, cpk_reprov],
        "% Reprov.": [f"{pct_qh_rep:.1f}%", f"{pct_cp_reprov:.1f}%", f"{pct_cpk_reprov:.1f}%"]
    }).set_index("Indicador")

    #style 
    def verde(val): return 'background-color: #8fcf79; color: black'
    def amarelo(val): return 'background-color: #fff59d; color: black'
    def vermelho(val): return 'background-color: #f28b82; color: black'

    tabela_style = (
        tabela.style
        .applymap(verde, subset=["Aprovados", "% Aprov."])
        .applymap(amarelo, subset=["Alerta", "% Alerta"])
        .applymap(vermelho, subset=["Reprovados", "% Reprov."])
    )

    st.dataframe(tabela_style, use_container_width=True)
    st.write("📈 Resumo")
    st.write(f"Total de pontos analisados: {total_pontos}")
    st.write(f"🟩 Aprovados: {qh_aprovados} ({pct_qh_aprov:.1f}%)")
    st.write(f"🟨 Em alerta: {qh_proximos} ({pct_qh_prox:.1f}%)")
    st.write(f"🟥 Fora da tolerância: {qh_reprovados} ({pct_qh_rep:.1f}%)")