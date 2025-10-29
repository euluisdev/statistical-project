import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ========================= FUNÇÃO: CALCULAR CP e CPK =========================
def calcular_cp_cpk(valores, lsl, usl):
    media = np.mean(valores)
    desvio = np.std(valores, ddof=1)
    if desvio == 0:
        return np.nan, np.nan, media, desvio
    cp = (usl - lsl) / (6 * desvio)
    cpk = min((usl - media), (media - lsl)) / (3 * desvio)
    return cp, cpk, media, desvio


# ========================= PAGE: TREND CHART =========================
def trend_chart():
    st.title("📈 Trend Chart - Controle Estatístico")

    # Verifica se os dados da peça estão carregados
    if 'df_peca' not in st.session_state or 'peca_atual' not in st.session_state:
        st.warning("⚠️ Nenhuma peça carregada. Volte e carregue uma peça primeiro.")
        st.stop()

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca'].copy()

    st.markdown(f"### Peça atual:")
    st.code(str(peca))

    # ================== ETAPA 1 - Selecionar pontos ==================
    st.subheader("Selecionar pontos para gerar o gráfico:")
    if not {'NomePonto', 'Eixo', 'Desvio'}.issubset(df.columns):
        st.error("❌ O DataFrame precisa conter as colunas 'NomePonto', 'Eixo' e 'Desvio'.")
        st.stop()

    pontos_unicos = df[['NomePonto', 'Eixo']].drop_duplicates()
    pontos_selecionados = st.multiselect(
        "Escolha os pontos:",
        options=pontos_unicos['NomePonto'].unique(),
        format_func=lambda x: f"{x} ({pontos_unicos.loc[pontos_unicos['NomePonto']==x, 'Eixo'].values[0]})"
    )

    if pontos_selecionados:
        df_filtrado = df[df['NomePonto'].isin(pontos_selecionados)]

        # ================== ETAPA 2 - Limites ==================
        col1, col2 = st.columns(2)
        with col1:
            lsl = st.number_input("LIE (Limite Inferior)", value=-0.5, step=0.01)
        with col2:
            usl = st.number_input("LSE (Limite Superior)", value=0.5, step=0.01)

        # ================== ETAPA 3 - Gráfico ==================
        st.subheader("📊 Gráfico de Tendência")

        fig, ax = plt.subplots(figsize=(10, 5))
        for ponto in pontos_selecionados:
            dados_ponto = df_filtrado[df_filtrado['NomePonto'] == ponto]
            eixo = dados_ponto['Eixo'].iloc[0]
            ax.plot(
                dados_ponto.index,
                dados_ponto['Desvio'],
                marker='o',
                label=f"{ponto} ({eixo})"
            )

        ax.axhline(usl, color="red", linestyle="--", linewidth=1, label="LSE")
        ax.axhline(lsl, color="red", linestyle="--", linewidth=1, label="LIE")
        ax.axhline(0, color="black", linestyle="--", linewidth=1, label="Nominal")
        ax.set_xlabel("Amostra")
        ax.set_ylabel("Desvio (mm)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        # ================== ETAPA 4 - Calcular Cp e Cpk ==================
        st.subheader("📏 Indicadores Estatísticos")
        resultados = []

        for ponto in pontos_selecionados:
            dados_ponto = df_filtrado[df_filtrado['NomePonto'] == ponto]['Desvio'].dropna()
            eixo = df_filtrado.loc[df_filtrado['NomePonto'] == ponto, 'Eixo'].values[0]
            cp, cpk, media, desvio = calcular_cp_cpk(dados_ponto.values, lsl, usl)
            resultados.append([
                ponto, eixo, round(media, 5), round(desvio, 5),
                round(cp, 3) if not np.isnan(cp) else None,
                round(cpk, 3) if not np.isnan(cpk) else None
            ])

        df_result = pd.DataFrame(resultados, columns=["NomePonto", "Eixo", "Média", "Desvio", "Cp", "Cpk"])

        # ================== COLORAÇÃO AUTOMÁTICA ==================
        def cor_cpk(val):
            if pd.isna(val):
                return ''
            if val >= 1.33:
                return 'background-color: #d9fbd9'  # verde
            elif val >= 1.0:
                return 'background-color: #fff5b5'  # amarelo
            else:
                return 'background-color: #f5b5b5'  # vermelho

        st.dataframe(
            df_result.style.map(cor_cpk, subset=['Cp', 'Cpk']),
            use_container_width=True
        )

    else:
        st.info("Selecione ao menos um ponto para gerar o gráfico.")
