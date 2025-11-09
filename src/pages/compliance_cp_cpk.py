import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def compliance_cp_cpk():
    st.set_page_config(page_title="CP/CPK POR PEÇA", layout="wide")
    st.title("CP/CPK POR PEÇA")
    st.markdown("""
     <style>
     .block-container {
          padding-top: 2rem;
          padding-bottom: 1rem;
          padding-left: 1rem;
          padding-right: 1rem;
      }
      </style>
    """, unsafe_allow_html=True)

    # 1. Verificar se há peça carregada
    if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
        st.warning("❗ Vá para 'Gerenciar Relatórios' e carregue uma peça primeiro.")
        return

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca'].copy()

    titulo = peca.get("Nome", "")
    codigo = str(peca.get("PartNumber", ""))

    # 2. Calcular CP e CPK
    if "NomePonto" not in df.columns:
        st.error("❌ Coluna 'NomePonto' não encontrada no dataframe.")
        return

    # Criar identificador único do ponto
    if "Eixo" in df.columns:
        df["PontoEixo"] = df["NomePonto"].astype(str) + " - " + df["Eixo"].astype(str)
    else:
        df["PontoEixo"] = df["NomePonto"].astype(str)

    # Calcular CP e CPK por ponto
    resultados_cp = []
    resultados_cpk = []
    
    for ponto in df["PontoEixo"].unique():
        df_ponto = df[df["PontoEixo"] == ponto]
        
        # Obter tolerâncias (assumindo que são simétricas)
        tol_sup = df_ponto["Tol+"].iloc[0]
        tol_inf = df_ponto["Tol-"].iloc[0]
        nominal = df_ponto["Nominal"].iloc[0]
        
        # Calcular desvio padrão
        desvios = df_ponto["Desvio"]
        std_dev = desvios.std()
        media = desvios.mean()
        
        # Calcular CP (Capacidade do Processo)
        # CP = (Tolerância Superior - Tolerância Inferior) / (6 * Desvio Padrão)
        tolerancia_total = abs(tol_sup - tol_inf)
        cp = tolerancia_total / (6 * std_dev) if std_dev > 0 else 0
        
        # Calcular CPK (Índice de Capacidade do Processo)
        # CPK = min[(LSL - média) / (3 * σ), (média - LIL) / (3 * σ)]
        lsl = nominal + tol_inf  # Limite Inferior
        usl = nominal + tol_sup  # Limite Superior
        valor_medio = nominal + media
        
        cpk_superior = (usl - valor_medio) / (3 * std_dev) if std_dev > 0 else 0
        cpk_inferior = (valor_medio - lsl) / (3 * std_dev) if std_dev > 0 else 0
        cpk = min(cpk_superior, cpk_inferior)
        
        resultados_cp.append({"PontoEixo": ponto, "CP": cp})
        resultados_cpk.append({"PontoEixo": ponto, "CPK": cpk})
    
    df_cp = pd.DataFrame(resultados_cp)
    df_cpk = pd.DataFrame(resultados_cpk)
    
    st.success(f"✅ {len(df_cp)} pontos únicos calculados.")

    # 3. Calcular estatísticas para CP
    total = len(df_cp)
    cp_133_acima = len(df_cp[df_cp["CP"] >= 1.33])
    cp_100_133 = len(df_cp[(df_cp["CP"] >= 1.0) & (df_cp["CP"] < 1.33)])
    cp_100_abaixo = len(df_cp[df_cp["CP"] < 1.0])

    perc_cp_133_acima = round((cp_133_acima / total) * 100, 1)
    perc_cp_100_133 = round((cp_100_133 / total) * 100, 1)
    perc_cp_100_abaixo = round((cp_100_abaixo / total) * 100, 1)

    # Calcular estatísticas para CPK
    cpk_133_acima = len(df_cpk[df_cpk["CPK"] >= 1.33])
    cpk_100_133 = len(df_cpk[(df_cpk["CPK"] >= 1.0) & (df_cpk["CPK"] < 1.33)])
    cpk_100_abaixo = len(df_cpk[df_cpk["CPK"] < 1.0])

    perc_cpk_133_acima = round((cpk_133_acima / total) * 100, 1)
    perc_cpk_100_133 = round((cpk_100_133 / total) * 100, 1)
    perc_cpk_100_abaixo = round((cpk_100_abaixo / total) * 100, 1)

    # 4. Configurar histórico
    pasta_historico = os.path.join(os.path.dirname(peca["PastaTXT"]), "historico")
    os.makedirs(pasta_historico, exist_ok=True)
    arquivo_cp = os.path.join(pasta_historico, f"historico_cp_{codigo}.csv")
    arquivo_cpk = os.path.join(pasta_historico, f"historico_cpk_{codigo}.csv")

    anos_disponiveis = list(range(2023, datetime.now().year + 2))
    col1, col2, col3 = st.columns([1, 1, 0.6])

    with col1:
        ano_selecionado = st.selectbox("YEAR:", sorted(anos_disponiveis),
                                       index=anos_disponiveis.index(datetime.now().year))
    with col2:
        semanas_disponiveis = [f"Week {i}" for i in range(1, 53)]
        semana_selecionada = st.selectbox("WEEK", semanas_disponiveis,
                                          index=datetime.now().isocalendar().week - 1)
    with col3:
        if st.button("GERAR", use_container_width=True):
            semana_chave = f"{ano_selecionado}-{semana_selecionada}"
            
            # Salvar histórico CP
            if os.path.exists(arquivo_cp):
                historico_cp = pd.read_csv(arquivo_cp)
            else:
                historico_cp = pd.DataFrame(columns=["AnoSemana", "Semana", "CP>=1.33", "1<=CP<1.33", "CP<1"])
            
            nova_linha_cp = {
                "AnoSemana": semana_chave,
                "Semana": semana_selecionada,
                "CP>=1.33": perc_cp_133_acima,
                "1<=CP<1.33": perc_cp_100_133,
                "CP<1": perc_cp_100_abaixo
            }

            historico_cp = historico_cp[historico_cp["AnoSemana"] != semana_chave]
            historico_cp = pd.concat([historico_cp, pd.DataFrame([nova_linha_cp])], ignore_index=True)
            historico_cp["AnoSemana"] = historico_cp["AnoSemana"].astype(str)
            historico_cp = historico_cp.sort_values(
                by="AnoSemana",
                key=lambda x: x.str.extract(r'(\d+)-Week (\d+)').astype(float).apply(tuple, axis=1),
                ascending=True
            ).tail(22).reset_index(drop=True)
            historico_cp.to_csv(arquivo_cp, index=False)
            
            # Salvar histórico CPK
            if os.path.exists(arquivo_cpk):
                historico_cpk = pd.read_csv(arquivo_cpk)
            else:
                historico_cpk = pd.DataFrame(columns=["AnoSemana", "Semana", "CPK>=1.33", "1<=CPK<1.33", "CPK<1"])
            
            nova_linha_cpk = {
                "AnoSemana": semana_chave,
                "Semana": semana_selecionada,
                "CPK>=1.33": perc_cpk_133_acima,
                "1<=CPK<1.33": perc_cpk_100_133,
                "CPK<1": perc_cpk_100_abaixo
            }

            historico_cpk = historico_cpk[historico_cpk["AnoSemana"] != semana_chave]
            historico_cpk = pd.concat([historico_cpk, pd.DataFrame([nova_linha_cpk])], ignore_index=True)
            historico_cpk["AnoSemana"] = historico_cpk["AnoSemana"].astype(str)
            historico_cpk = historico_cpk.sort_values(
                by="AnoSemana",
                key=lambda x: x.str.extract(r'(\d+)-Week (\d+)').astype(float).apply(tuple, axis=1),
                ascending=True
            ).tail(22).reset_index(drop=True)
            historico_cpk.to_csv(arquivo_cpk, index=False)
            
            st.success(f"✅ Semana '{semana_selecionada}' de {ano_selecionado} salva no histórico!")
            st.rerun()

    # 5. Exibir gráficos
    if os.path.exists(arquivo_cp):
        historico_cp = pd.read_csv(arquivo_cp)
    else:
        historico_cp = pd.DataFrame(columns=["AnoSemana", "Semana", "CP>=1.33", "1<=CP<1.33", "CP<1"])

    if os.path.exists(arquivo_cpk):
        historico_cpk = pd.read_csv(arquivo_cpk)
    else:
        historico_cpk = pd.DataFrame(columns=["AnoSemana", "Semana", "CPK>=1.33", "1<=CPK<1.33", "CPK<1"])

    # Gráfico CP
    if not historico_cp.empty:
        texto_verde_cp = []
        texto_amarelo_cp = []
        texto_vermelho_cp = []
        
        for idx, row in historico_cp.iterrows():
            qnt_verde = int(round(row["CP>=1.33"] * total / 100))
            qnt_amarelo = int(round(row["1<=CP<1.33"] * total / 100))
            qnt_vermelho = int(round(row["CP<1"] * total / 100))
            
            texto_verde_cp.append(f"{qnt_verde}")
            texto_amarelo_cp.append(f"{qnt_amarelo}")
            texto_vermelho_cp.append(f"{qnt_vermelho}")
        
        fig_cp = go.Figure()
        fig_cp.add_trace(go.Bar(
            name="CP ≥ 1,33",
            x=historico_cp["Semana"],
            y=historico_cp["CP>=1.33"],
            marker_color="green",
            width=[0.5]*len(historico_cp),
            text=texto_verde_cp,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12, family="Arial Black")
        ))
        fig_cp.add_trace(go.Bar(
            name="1 ≤ CP < 1,33",
            x=historico_cp["Semana"],
            y=historico_cp["1<=CP<1.33"],
            marker_color="yellow",
            width=[0.5]*len(historico_cp),
            text=texto_amarelo_cp,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="black", size=12, family="Arial Black")
        ))
        fig_cp.add_trace(go.Bar(
            name="CP < 1",
            x=historico_cp["Semana"],
            y=historico_cp["CP<1"],
            marker_color="red",
            width=[0.5]*len(historico_cp),
            text=texto_vermelho_cp,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12, family="Arial Black")
        ))

        fig_cp.update_layout(
            barmode='stack',
            title=f"CP - {codigo} - {titulo}",
            xaxis_title="",
            yaxis_title="%",
            yaxis=dict(range=[0, 100], ticksuffix="%"),
            template="plotly_white",
            height=400,
            xaxis=dict(tickangle=-45, tickfont=dict(color="black", size=10)),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig_cp, use_container_width=True)

    # Gráfico CPK
    if not historico_cpk.empty:
        texto_verde_cpk = []
        texto_amarelo_cpk = []
        texto_vermelho_cpk = []
        
        for idx, row in historico_cpk.iterrows():
            qnt_verde = int(round(row["CPK>=1.33"] * total / 100))
            qnt_amarelo = int(round(row["1<=CPK<1.33"] * total / 100))
            qnt_vermelho = int(round(row["CPK<1"] * total / 100))
            
            texto_verde_cpk.append(f"{qnt_verde}")
            texto_amarelo_cpk.append(f"{qnt_amarelo}")
            texto_vermelho_cpk.append(f"{qnt_vermelho}")
        
        fig_cpk = go.Figure()
        fig_cpk.add_trace(go.Bar(
            name="CPK ≥ 1,33",
            x=historico_cpk["Semana"],
            y=historico_cpk["CPK>=1.33"],
            marker_color="green",
            width=[0.5]*len(historico_cpk),
            text=texto_verde_cpk,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12, family="Arial Black")
        ))
        fig_cpk.add_trace(go.Bar(
            name="1 ≤ CPK < 1,33",
            x=historico_cpk["Semana"],
            y=historico_cpk["1<=CPK<1.33"],
            marker_color="yellow",
            width=[0.5]*len(historico_cpk),
            text=texto_amarelo_cpk,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="black", size=12, family="Arial Black")
        ))
        fig_cpk.add_trace(go.Bar(
            name="CPK < 1",
            x=historico_cpk["Semana"],
            y=historico_cpk["CPK<1"],
            marker_color="red",
            width=[0.5]*len(historico_cpk),
            text=texto_vermelho_cpk,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=12, family="Arial Black")
        ))

        fig_cpk.update_layout(
            barmode='stack',
            title=f"CPK - {codigo} - {titulo}",
            xaxis_title="",
            yaxis_title="%",
            yaxis=dict(range=[0, 100], ticksuffix="%"),
            template="plotly_white",
            height=400,
            xaxis=dict(tickangle=-45, tickfont=dict(color="black", size=10)),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig_cpk, use_container_width=True)
        
        # Botões de download
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Baixar histórico CP (CSV)",
                data=historico_cp.to_csv(index=False).encode('utf-8'),
                file_name=f"historico_cp_{codigo}.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="📥 Baixar histórico CPK (CSV)",
                data=historico_cpk.to_csv(index=False).encode('utf-8'),
                file_name=f"historico_cpk_{codigo}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("📊 Nenhum histórico encontrado ainda. Gere a primeira semana para começar!")

if __name__ == "__main__":
    compliance_cp_cpk()