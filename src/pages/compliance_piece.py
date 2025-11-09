
import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

def compliance_piece():
    st.set_page_config(page_title="CG POR PEÇA", layout="wide")
    st.title("CONFORMIDADE GERAL POR PEÇA")
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

    #1
    if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
        st.warning("❗ Vá para 'Gerenciar Relatórios' e carregue uma peça primeiro.")
        return

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca'].copy()

    titulo = peca.get("Nome", "")
    codigo = str(peca.get("PartNumber", ""))

    # 2
    df["CG"] = (df["Desvio"].abs() / df["Tol+"].abs()) * 100

    if "NomePonto" not in df.columns:
        st.error("❌ Coluna 'NomePonto' não encontrada no dataframe.")
        return

    if "Eixo" in df.columns:
        df["PontoEixo"] = df["NomePonto"].astype(str) + " - " + df["Eixo"].astype(str)
    else:
        df["PontoEixo"] = df["NomePonto"].astype(str)

    df_medias = df.groupby("PontoEixo", as_index=False)["CG"].mean()
    
    st.success(f"✅ {len(df_medias)} pontos únicos carregados do dataframe.")

    total = len(df_medias)
    cg_75 = len(df_medias[df_medias["CG"] <= 75])
    cg_100 = len(df_medias[(df_medias["CG"] > 75) & (df_medias["CG"] <= 100)])
    cg_acima = len(df_medias[df_medias["CG"] > 100])

    perc_75 = round((cg_75 / total) * 100, 1)
    perc_100 = round((cg_100 / total) * 100, 1)
    perc_acima = round((cg_acima / total) * 100, 1)

    #3
    pasta_historico = os.path.join(os.path.dirname(peca["PastaTXT"]), "historico")
    os.makedirs(pasta_historico, exist_ok=True)
    arquivo = os.path.join(pasta_historico, f"historico_{codigo}.csv")

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
            
            if os.path.exists(arquivo):
                historico = pd.read_csv(arquivo)
            else:
                historico = pd.DataFrame(columns=["AnoSemana", "Semana", "CG<=75%", "75%<CG<=100%", "CG>100%"])
            
            nova_linha = {
                "AnoSemana": semana_chave,
                "Semana": semana_selecionada,
                "CG<=75%": perc_75,
                "75%<CG<=100%": perc_100,
                "CG>100%": perc_acima
            }

            historico = historico[historico["AnoSemana"] != semana_chave]
            historico = pd.concat([historico, pd.DataFrame([nova_linha])], ignore_index=True)
            historico["AnoSemana"] = historico["AnoSemana"].astype(str)
            historico = historico.sort_values(
                by="AnoSemana",
                key=lambda x: x.str.extract(r'(\d+)-Week (\d+)').astype(float).apply(tuple, axis=1),
                ascending=True
            ).tail(22).reset_index(drop=True)
            historico.to_csv(arquivo, index=False)
            st.success(f"✅ Semana '{semana_selecionada}' de {ano_selecionado} salva no histórico!")
            st.rerun()

    #4
    if os.path.exists(arquivo):
        historico = pd.read_csv(arquivo)
    else:
        historico = pd.DataFrame(columns=["AnoSemana", "Semana", "CG<=75%", "75%<CG<=100%", "CG>100%"])

    if not historico.empty:
        texto_verde = []
        texto_amarelo = []
        texto_vermelho = []
        
        for idx, row in historico.iterrows():
            perc_75_hist = row["CG<=75%"]
            perc_100_hist = row["75%<CG<=100%"]
            perc_acima_hist = row["CG>100%"]
            
            qnt_75 = int(round(perc_75_hist * total / 100))
            qnt_100 = int(round(perc_100_hist * total / 100))
            qnt_acima = int(round(perc_acima_hist * total / 100))
            
            texto_verde.append(f"{qnt_75}")
            texto_amarelo.append(f"{qnt_100}")
            texto_vermelho.append(f"{qnt_acima}")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="CG ≤ 75%",
            x=historico["Semana"],
            y=historico["CG<=75%"],
            marker_color="green",
            width=[0.5]*len(historico),
            text=texto_verde,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="black", size=14)
        ))
        fig.add_trace(go.Bar(
            name="75% < CG ≤ 100%",
            x=historico["Semana"],
            y=historico["75%<CG<=100%"],
            marker_color="yellow",
            width=[0.5]*len(historico),
            text=texto_amarelo,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="black", size=14)
        ))
        fig.add_trace(go.Bar(
            name="CG > 100%",
            x=historico["Semana"],
            y=historico["CG>100%"],
            marker_color="red",
            width=[0.5]*len(historico),
            text=texto_vermelho,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white", size=14)
        ))

        fig.update_layout(
            barmode='stack',
            title=f"CG - {codigo} - {titulo}",
            xaxis_title="",
            yaxis_title="%",
            template="plotly_white",
            height=700,
            xaxis=dict(tickangle=45, tickfont=dict(color="black")),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        
        st.download_button(
            label="Baixar histórico CSV",
            data=historico.to_csv(index=False).encode('utf-8'),
            file_name=f"historico_{codigo}.csv",
            mime="text/csv"
        )
    else:
        st.info("Nenhum histórico encontrado ainda.")