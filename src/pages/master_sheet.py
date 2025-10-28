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

    if "Eixo" in df.columns:
        df["PontoEixo"] = df["NomePonto"].astype(str) + " - " + df["Eixo"].astype(str)
    else:
        df["PontoEixo"] = df["NomePonto"].astype(str)

    # aprovação
    dentro_tol = (df["Desvio"] >= df["Tol-"]) & (df["Desvio"] <= df["Tol+"])
    df["DentroTol"] = dentro_tol

    def proximos(grupo):
        tol_superior = grupo["Tol+"].max()
        tol_inferior = grupo["Tol-"].min()
        faixa = tol_superior - tol_inferior
        limite_superior = tol_superior - 0.2 * faixa
        limite_inferior = tol_inferior + 0.2 * faixa
        return any((grupo["Desvio"] <= limite_inferior) | (grupo["Desvio"] >= limite_superior)) \
            and all((grupo["Desvio"] >= tol_inferior) & (grupo["Desvio"] <= tol_superior))

    pontos = df.groupby("PontoEixo")["DentroTol"].all()
    total_pontos = len(pontos)
    pontos_aprovados = pontos.sum()
    pontos_reprovados = total_pontos - pontos_aprovados
    pct_aprovado = (pontos_aprovados / total_pontos * 100) if total_pontos > 0 else 0
    pct_reprovado = (pontos_reprovados / total_pontos * 100) if total_pontos > 0 else 0

    proximos_count = df.groupby("PontoEixo").apply(proximos).sum()
    pct_proximos = (proximos_count / total_pontos * 100) if total_pontos > 0 else 0


    # CP CPK global
    if not df.empty:
        sigma = df["Desvio"].std(ddof=1)
        media = df["Desvio"].mean()
        USL = df["Tol+"].max()
        LSL = df["Tol-"].min()
        cp = (USL - LSL) / (6 * sigma) if sigma > 0 else 0
        cpk = min((USL - media) / (3 * sigma), (media - LSL) / (3 * sigma)) if sigma > 0 else 0
    else:
        cp, cpk = 0, 0

    # CP e CPK individual
    def cp_val(grupo):
        std = grupo["Desvio"].std(ddof=0) if len(grupo) > 1 else 1
        return (grupo["Tol+"].max() - grupo["Tol-"].min()) / (6 * std)

    def cpk_val(grupo):
        std = grupo["Desvio"].std(ddof=0) if len(grupo) > 1 else 1
        media = grupo["Desvio"].mean()
        return min(grupo["Tol+"].max() - media, media - grupo["Tol-"].min()) / (3 * std)

    cps = df.groupby("PontoEixo").apply(cp_val)
    cpks = df.groupby("PontoEixo").apply(cpk_val)

    cp_bom_count = (cps >= 1.33).sum()
    cpk_bom_count = (cpks >= 1.33).sum()
    cp_medio_count = ((cps >= 1) & (cps < 1.33)).sum()
    cpk_medio_count = ((cpks >= 1) & (cpks < 1.33)).sum()

    pct_cp_bom = (cp_bom_count / total_pontos * 100) if total_pontos > 0 else 0
    pct_cpk_bom = (cpk_bom_count / total_pontos * 100) if total_pontos > 0 else 0
    pct_cp_medio = (cp_medio_count / total_pontos * 100) if total_pontos > 0 else 0
    pct_cpk_medio = (cpk_medio_count / total_pontos * 100) if total_pontos > 0 else 0

    #tabela final
    tabela = pd.DataFrame({
        "Indicador": ["QH", "CP", "CPK"],
        "Pontos Aprovados": [pontos_aprovados, cp_bom_count, cpk_bom_count],
        "Porcentagem Aprov.": [pct_aprovado, pct_cp_bom, pct_cpk_bom],
        "Pontos Médios": [proximos_count, cp_medio_count, cpk_medio_count],
        "Porcentagem Médios": [pct_proximos, pct_cp_medio, pct_cpk_medio],
        "Pontos Reprovados": [pontos_reprovados, total_pontos - cp_bom_count, total_pontos - cpk_bom_count],
        "Porcentagem Reprov.": [pct_reprovado, 100 - pct_cp_bom, 100 - pct_cpk_bom],
    }).set_index("Indicador")

    # style
    def verde(val): return 'background-color: #8fcf79'
    def amarelo(val): return 'background-color: #fff59d'
    def vermelho(val): return 'background-color: #f28b82'

    for col in ["Porcentagem Aprov.", "Porcentagem Médios", "Porcentagem Reprov."]:
        tabela[col] = tabela[col].apply(lambda x: f"{x:.1f}%")

    tabela_style = (
        tabela.style
        .applymap(verde, subset=["Pontos Aprovados", "Porcentagem Aprov."])
        .applymap(amarelo, subset=["Pontos Médios", "Porcentagem Médios"])
        .applymap(vermelho, subset=["Pontos Reprovados", "Porcentagem Reprov."])
    )

    st.dataframe(tabela_style, use_container_width=True)

    st.write("📈 Resumo")
    st.write(f"Total de pontos analisados: {total_pontos}")
    st.write(f"🟩 Dentro da tolerância (QH): {pontos_aprovados} ({pct_aprovado:.1f}%)")
    st.write(f"🟨 Próximos da tolerância (ainda aprovados): {proximos_count} ({pct_proximos:.1f}%)")
    st.write(f"🟥 Fora da tolerância: {pontos_reprovados} ({pct_reprovado:.1f}%)")
    st.write(f"📊 CP global = {cp:.2f} | CPK global = {cpk:.2f}")
