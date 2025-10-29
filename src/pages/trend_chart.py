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

    df['NomePonto'] = df['NomePonto'].astype(str)
    df['Eixo'] = df['Eixo'].astype(str)
    df['PontoEixo'] = df['NomePonto'] + " - " + df['Eixo']

    st.markdown(f"### Peça atual:")
    st.code(str(peca))

    #Selecionar pontos
    st.subheader("Selecione um ponto para gerar o gráfico:")
    if not {'PontoEixo', 'NomePonto', 'Eixo', 'Desvio'}.issubset(df.columns):
        st.error("❌ O DataFrame precisa conter as colunas 'NomePonto', 'Eixo' e 'Desvio'.")
        st.stop()

    opcoes = df['PontoEixo'].drop_duplicates().sort_values().tolist()
    pontos_selecionados = st.multiselect(
        "Escolha os pontos (ex: CÍR1 - X):",
        options=opcoes,
        default=[]
    )

    if pontos_selecionados:
        df_filtrado = df[df['PontoEixo'].isin(pontos_selecionados)].copy()

        #limite fixo
        col1, col2 = st.columns(2)
        with col1:
            lsl = st.number_input("LIE (Limite Inferior)", value=-0.5, step=0.01)
        with col2:
            usl = st.number_input("LSE (Limite Superior)", value=0.5, step=0.01)

        #gráfico
        st.subheader("📊 Gráfico de Tendência")

        fig, ax = plt.subplots(figsize=(10, 5))

        df_filtrado = df_filtrado.dropna(subset=['Desvio', 'DataHora']).copy()
        if df_filtrado.empty:
            st.warning("Nenhuma linha com Desvio e DataHora válidos para os pontos selecionados.")
            st.stop()

        all_dates = []
        for pontoeixo in pontos_selecionados:
            dados_ponto = df_filtrado[df_filtrado['PontoEixo'] == pontoeixo].copy()
            if dados_ponto.empty:
                continue
            dados_ponto = dados_ponto.sort_values(by='DataHora')
            all_dates.extend(dados_ponto['DataHora'].tolist())

        if len(all_dates) == 0:
            st.warning("Nenhuma data válida para plotar.")
        else:

            unique_dates = sorted(list(dict.fromkeys(all_dates)))

            max_ticks = 12 
            if len(unique_dates) > max_ticks:
                step = max(1, int(np.ceil(len(unique_dates) / max_ticks)))
                unique_dates = unique_dates[::step]

            #number matplotlib
            date_nums = mdates.date2num(unique_dates)

            for pontoeixo in pontos_selecionados:
                dados_ponto = df_filtrado[df_filtrado['PontoEixo'] == pontoeixo].copy()
                if dados_ponto.empty:
                    continue
                dados_ponto = dados_ponto.sort_values(by='DataHora')
                x_nums = mdates.date2num(dados_ponto['DataHora'])
                ax.plot(
                    x_nums,
                    dados_ponto['Desvio'],
                    marker='o',
                    linestyle='-',
                    linewidth=1.5,
                    label=pontoeixo
                )
                #st.write(dados_ponto[['NomePonto', 'Eixo', 'Data', 'Hora', 'DataHora', 'Desvio']])

            ax.xaxis.set_major_locator(FixedLocator(date_nums))
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M:%S"))

            ax.axhline(usl, color="red", linestyle="--", linewidth=1, label="LSE")
            ax.axhline(lsl, color="red", linestyle="--", linewidth=1, label="LIE")
            ax.axhline(0, color="black", linestyle="--", linewidth=1, label="Nominal")

            #eixo Y fixo 2 de range
            ax.set_ylim(-1, 1)
            ax.set_yticks(np.arange(-1, 1.1, 0.5))
            ax.set_ylabel("Desvio (mm)")

            ax.set_xlim(date_nums[0], date_nums[-1])

            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')

            st.pyplot(fig, use_container_width=True)

        #calcular cp cpk
        st.subheader("📏 Indicadores Estatísticos")
        resultados = []

        for pontoeixo in pontos_selecionados:
            dados_ponto = df[df['PontoEixo'] == pontoeixo]['Desvio'].dropna().values
            nomep, eixo = pontoeixo.rsplit(" - ", 1)
            cp, cpk, media, desvio = calcular_cp_cpk(dados_ponto, lsl, usl)
            resultados.append([
                nomep, eixo, pontoeixo, round(media, 5), round(desvio, 5),
                (round(cp, 3) if (cp is not None and not np.isnan(cp)) else None),
                (round(cpk, 3) if (cpk is not None and not np.isnan(cpk)) else None)
            ])

        df_result = pd.DataFrame(resultados, columns=[
            "NomePonto", "Eixo", "PontoEixo", "Média", "Desvio", "Cp", "Cpk"
        ])

        def cor_cpk(val):
            if pd.isna(val):
                return ''
            if val >= 1.33:
                return 'background-color: #d9fbd9'  # verde
            elif val >= 1.0:
                return 'background-color: #fff5b5'  # amarelo
            else:
                return 'background-color: #f5b5b5'  # vermelho

        st.dataframe(df_result.style.map(cor_cpk, subset=['Cp', 'Cpk']), use_container_width=True)

    else:
        st.info("Selecione ao menos um ponto para gerar o gráfico.")
