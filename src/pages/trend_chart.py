import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator

def calcular_cp_cpk(valores, lsl, usl):
    media = np.mean(valores)
    desvio = np.std(valores, ddof=1)
    if desvio == 0:
        return np.nan, np.nan, media, desvio
    cp = (usl - lsl) / (6 * desvio)
    cpk = min((usl - media), (media - lsl)) / (3 * desvio)
    return cp, cpk, media, desvio

def trend_chart():
    st.title("📈 Trend Chart - Controle Estatístico")

    if 'df_peca' not in st.session_state or 'peca_atual' not in st.session_state:
        st.warning("⚠️ Nenhuma peça carregada. Volte e carregue uma peça primeiro.")
        st.stop()

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca'].copy()

    # ========================== DATA E HORA ==========================
    if 'Data' in df.columns and 'Hora' in df.columns:
        df['DataHora'] = pd.to_datetime(
            df['Data'].astype(str).str.strip() + ' ' + df['Hora'].astype(str).str.strip(),
            format='%d/%m/%Y %H:%M:%S',
            errors='coerce'
        )
        mask_na = df['DataHora'].isna()
        if mask_na.any():
            df.loc[mask_na, 'DataHora'] = pd.to_datetime(
                df.loc[mask_na, 'Data'].astype(str).str.strip() + ' ' + df.loc[mask_na, 'Hora'].astype(str).str.strip(),
                errors='coerce'
            )
    else:
        st.error("❌ O DataFrame não contém colunas 'Data' e 'Hora'.")
        st.stop()

    # ========================== CAMPOS BASE ==========================
    df['NomePonto'] = df['NomePonto'].astype(str)
    df['Eixo'] = df['Eixo'].astype(str)
    df['PontoEixo'] = df['NomePonto'] + " - " + df['Eixo']

    st.markdown(f"### Peça atual:")
    st.code(str(peca))

    # ========================== SELECIONAR PONTOS ==========================
    st.subheader("Selecione um ponto para gerar o gráfico:")
    if not {'PontoEixo', 'NomePonto', 'Eixo', 'Desvio', 'Tol+', 'Tol-'}.issubset(df.columns):
        st.error("❌ O DataFrame precisa conter as colunas 'NomePonto', 'Eixo', 'Desvio', 'Tol+' e 'Tol-'.")
        st.stop()

    opcoes = df['PontoEixo'].drop_duplicates().sort_values().tolist()
    pontos_selecionados = st.multiselect(
        "Escolha os pontos:",
        options=opcoes,
        default=[]
    )

    if pontos_selecionados:
        df_filtrado = df[df['PontoEixo'].isin(pontos_selecionados)].copy()
        df_filtrado = df_filtrado.dropna(subset=['Desvio', 'DataHora']).copy()

        if df_filtrado.empty:
            st.warning("Nenhuma linha com Desvio e DataHora válidos para os pontos selecionados.")
            st.stop()

        # ========================== GRÁFICOS POR PONTO ==========================
        st.subheader("Gráficos de Tendência")

        for pontoeixo in pontos_selecionados:
            dados_ponto = df_filtrado[df_filtrado['PontoEixo'] == pontoeixo].copy()
            if dados_ponto.empty:
                st.info(f"Sem dados válidos para {pontoeixo}.")
                continue

            dados_ponto = dados_ponto.sort_values(by='DataHora')

            usl = dados_ponto['Tol+'].iloc[0]
            lsl = -abs(dados_ponto['Tol-'].iloc[0])  

            x_nums = mdates.date2num(dados_ponto['DataHora'])
            date_nums = mdates.date2num(sorted(dados_ponto['DataHora'].unique()))

            fig, ax = plt.subplots(figsize=(12, 3))

            ax.plot(
                x_nums,
                dados_ponto['Desvio'],
                marker='o',
                linestyle='-',
                linewidth=1.5,
                label=pontoeixo
            )

            ax.xaxis.set_major_locator(FixedLocator(date_nums))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M:%S"))

            # --- Linhas horizontais usando as tolerâncias automáticas ---
            ax.axhline(usl, color="#FF3333", linestyle="--", linewidth=1, label=f"LSE ({usl:.3f})")
            ax.axhline(lsl, color="#FF3333", linestyle="--", linewidth=1, label=f"LIE ({lsl:.3f})")
            ax.axhline(0, color="#00FF66", linestyle="--", linewidth=1, label="Especificado")

            ax.set_ylim(-1, 1)
            ax.set_yticks([-1, -0.6, -0.3, 0, 0.3, 0.6, 1])
            ax.set_xlim(date_nums[0], date_nums[-1])

            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            plt.tight_layout(pad=0.5)
            ax.grid(False)
            ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')

            st.pyplot(fig, use_container_width=True)
            st.markdown("<hr style='margin: 6px 0;'>", unsafe_allow_html=True)

        # ========================== CÁLCULOS Cp / Cpk ==========================
        st.subheader("📏 Indicadores Estatísticos")
        resultados = []

        for pontoeixo in pontos_selecionados:
            dados_ponto = df[df['PontoEixo'] == pontoeixo].copy()
            if dados_ponto.empty:
                continue

            usl = dados_ponto['Tol+'].iloc[0]
            lsl = -abs(dados_ponto['Tol-'].iloc[0])
            valores = dados_ponto['Desvio'].dropna().values

            #nomep, eixo = pontoeixo.rsplit(" - ", 1)
            cp, cpk, media, desvio = calcular_cp_cpk(valores, lsl, usl)

            resultados.append([
                pontoeixo, round(media, 5), round(desvio, 5),
                (round(cp, 3) if (cp is not None and not np.isnan(cp)) else None),
                (round(cpk, 3) if (cpk is not None and not np.isnan(cpk)) else None)
            ])

        df_result = pd.DataFrame(resultados, columns=[
            "PontoEixo", "Média", "Desvio", "Cp", "Cpk"
        ])

        def cor_cpk(val):
            if pd.isna(val):
                return ''
            if val >= 1.33:
                return 'background-color: #00FF66'  # verde
            elif val >= 1.0:
                return 'background-color: #FFFF33'  # amarelo
            else:
                return 'background-color: #FF3333'  # vermelho

        st.dataframe(df_result.style.map(cor_cpk, subset=['Cp', 'Cpk']), use_container_width=True)

    else:
        st.info("Selecione ao menos um ponto para gerar o gráfico.")
