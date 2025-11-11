import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator
import os
import io

def calcular_cp_cpk(valores, lsl, usl):
    media = np.mean(valores)
    desvio = np.std(valores, ddof=1)
    if desvio == 0:
        return np.nan, np.nan, media, desvio
    cp = (usl - lsl) / (6 * desvio)
    cpk = min((usl - media), (media - lsl)) / (3 * desvio)
    return cp, cpk, media, desvio

#1
def trend_chart():
    st.title("CONTROLE ESTATÍSTICO - TREND CHART")

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

    #2
    df['NomePonto'] = df['NomePonto'].astype(str)
    df['Eixo'] = df['Eixo'].astype(str)
    df['PontoEixo'] = df['NomePonto'] + " - " + df['Eixo']

    st.markdown(f"### Peça atual:")
    st.code(str(peca))

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
    figuras_geradas = [] 

    if pontos_selecionados:
        df_filtrado = df[df['PontoEixo'].isin(pontos_selecionados)].copy()
        df_filtrado = df_filtrado.dropna(subset=['Desvio', 'DataHora']).copy()

        if df_filtrado.empty:
            st.warning("Nenhuma linha com Desvio e DataHora válidos para os pontos selecionados.")
            st.stop()

        st.subheader("Gráficos de Tendência")

        for pontoeixo in pontos_selecionados:
            dados_ponto = df_filtrado[df_filtrado['PontoEixo'] == pontoeixo].copy()
            if dados_ponto.empty:
                st.info(f"Sem dados válidos para {pontoeixo}.")
                continue

            dados_ponto['DataHora'] = pd.to_datetime(dados_ponto['DataHora'], errors='coerce')
            dados_ponto = dados_ponto.dropna(subset=['DataHora']).sort_values(by='DataHora')

            x_pos = np.arange(len(dados_ponto))
            x_labels = dados_ponto['DataHora'].dt.strftime("%d/%m %H:%M:%S")

            valores = dados_ponto['Desvio'].values

            usl = dados_ponto['Tol+'].iloc[0]
            lsl = -abs(dados_ponto['Tol-'].iloc[0])
            cp, cpk, media, desvio = calcular_cp_cpk(valores, lsl, usl)

            lsc = media + 3 * desvio
            lic = media - 3 * desvio

            fig = plt.figure(figsize=(12, 4))
            gs = fig.add_gridspec(1, 2, width_ratios=[3, 1])
            ax = fig.add_subplot(gs[0])

            ax.plot(x_pos, valores, marker='o', markersize=6, linewidth=2,
                    color='#007ACC', markerfacecolor='white', markeredgecolor='#007ACC', label=pontoeixo)

            ax.set_xticks(x_pos)
            ax.set_xticklabels(x_labels, rotation=45, ha='right')

            ax.axhline(usl, color="#FF3333", linestyle="--", linewidth=1, label='LSE')
            ax.axhline(lsl, color="#FF3333", linestyle="--", linewidth=1, label='LIE')
            ax.axhline(media, color='green', linewidth=2, label='AVERAGE')
            ax.axhline(lsc, color='blue', linestyle='--', linewidth=1.5, label='LSC')
            ax.axhline(lic, color='blue', linestyle='--', linewidth=1.5, label='LIC')

            for spine in ['top', 'right', 'bottom']:  
                ax.spines[spine].set_visible(False)
            ax.spines['left'].set_visible(True)

            ax.set_facecolor('white')
            ax.set_ylim(min(lsl*1.2, lic*1.2), max(usl*1.2, lsc*1.2))
            ax.legend(
                loc='upper center',
                bbox_to_anchor=(0.5, 1.25), 
                ncol=5,                     
                fontsize=10,
                frameon=False
            )

            #3
            ax2 = fig.add_subplot(gs[1])
            ax2.axis('off')
            tabela = [
                ["CP", f"{cp:.2f}"], ["CPK", f"{cpk:.2f}"], ["AVERAGE", f"{media:.2f}"],
                ["RANGE", f"{valores.max() - valores.min():.2f}"],
                ["LSE", f"{usl:.2f}"], ["LIE", f"{lsl:.2f}"],
                ["LSC", f"{lsc:.2f}"], ["LIC", f"{lic:.2f}"],
            ]
            tabela_plot = ax2.table(cellText=tabela, cellLoc='center', loc='center', colWidths=[0.4, 0.3])
            tabela_plot.auto_set_font_size(False)
            tabela_plot.set_fontsize(9)
            for (i, j), cell in tabela_plot.get_celld().items():
                cell.set_linewidth(0.6)
                if j == 0:
                    cell.set_text_props(fontweight='bold', color='black')
                    cell.set_facecolor('#F8F8F8')
                else:
                    cell.set_facecolor('white')

            plt.tight_layout(pad=1)
            st.pyplot(fig, use_container_width=True)
            
            figuras_geradas.append((pontoeixo, fig))

            
        if figuras_geradas and st.button("Salvar os gráficos selecionados"): 
            pasta = "trend_images"
            os.makedirs(pasta, exist_ok=True)

            if "trend_pages" not in st.session_state:
                st.session_state["trend_pages"] = []

            for nome, figura in figuras_geradas:
                caminho_arquivo = os.path.join(pasta, f"{nome.replace(' ', '_')}.png")
                figura.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')

                st.session_state["trend_pages"].append({
                    "nome": nome,
                    "arquivo": caminho_arquivo
                })

            st.success(f"✅ {len(figuras_geradas)} gráfico(s) salvo(s) com sucesso!")



        st.subheader("📏 Indicadores Estatísticos")
        resultados = []

        for pontoeixo in pontos_selecionados:
            dados_ponto = df[df['PontoEixo'] == pontoeixo].copy()
            if dados_ponto.empty:
                continue

            usl = dados_ponto['Tol+'].iloc[0]
            lsl = -abs(dados_ponto['Tol-'].iloc[0])
            valores = dados_ponto['Desvio'].dropna().values
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
                return 'background-color: #00FF66'
            elif val >= 1.0:
                return 'background-color: #FFFF33' 
            else:
                return 'background-color: #FF3333'

        st.dataframe(df_result.style.map(cor_cpk, subset=['Cp', 'Cpk']), use_container_width=True)

    else:
        st.info("Selecione ao menos um ponto para gerar o gráfico.")
