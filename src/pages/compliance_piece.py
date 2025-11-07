import os
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def compliance_piece():
    st.title("📊 Relatório CG por Semana")

    # 1
    if 'peca_atual' not in st.session_state or 'df_peca' not in st.session_state:
        st.warning("❗ Vá para 'Gerenciar Relatórios' e carregue uma peça primeiro.")
        return

    peca = st.session_state['peca_atual']
    df = st.session_state['df_peca'].copy()

    titulo = peca.get("Nome", "")
    codigo = str(peca.get("PartNumber", ""))

    st.subheader(f"📌 Peça: {titulo} ({codigo})")
    st.success(f"✅ {len(df)} medições carregadas do dataframe.")

    # 2
    df["CG"] = (df["Desvio"].abs() / df["Tol+"].abs()) * 100

    if "NomePonto" not in df.columns:
        st.error("❌ Coluna 'NomePonto' não encontrada no dataframe.")
        return

    df_medias = df.groupby("NomePonto", as_index=False)["CG"].mean()

    total = len(df_medias)
    cg_75 = len(df_medias[df_medias["CG"] <= 75])
    cg_100 = len(df_medias[(df_medias["CG"] > 75) & (df_medias["CG"] <= 100)])
    cg_acima = len(df_medias[df_medias["CG"] > 100])

    perc_75 = round((cg_75 / total) * 100, 1)
    perc_100 = round((cg_100 / total) * 100, 1)
    perc_acima = round((cg_acima / total) * 100, 1)

    # 3
    pasta_historico = os.path.join(os.path.dirname(peca["PastaTXT"]), "historico")
    os.makedirs(pasta_historico, exist_ok=True)
    arquivo = os.path.join(pasta_historico, f"historico_{codigo}.csv")

    grafico_placeholder = st.empty()

    # 4
    if os.path.exists(arquivo):
        historico = pd.read_csv(arquivo)

        # 🔹 Ordena o histórico antes de exibir
        historico = historico.sort_values(
            by="Semana",
            key=lambda x: x.astype(str).str.extract(r'(\d+)')[0].astype(float),
            ascending=True
        )

        st.info("Histórico encontrado. Mostrando gráfico acumulado:")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="CG ≤ 75%",
            x=historico["Semana"],
            y=historico["CG<=75%"],
            marker_color="green",
            text=[f"{cg_75}"] * len(historico),  
            textposition="inside", 
            insidetextanchor="middle",  
            textfont=dict(color="black", size=12)
        ))
        fig.add_trace(go.Bar(
            name="75% < CG ≤ 100%",
            x=historico["Semana"],
            y=historico["75%<CG<=100%"],
            marker_color="yellow",
            text=[f"{cg_100}"] * len(historico),
            textposition="inside", 
            insidetextanchor="middle",  
            textfont=dict(color="black", size=12)
        ))
        fig.add_trace(go.Bar(
            name="CG > 100%",
            x=historico["Semana"],
            y=historico["CG>100%"],
            marker_color="red",
            text=[f"{cg_acima}"] * len(historico),
            textposition="inside", 
            insidetextanchor="middle",  
            textfont=dict(color="black", size=12)
        ))

        fig.update_layout(
            barmode='stack',
            title=f"CG - {codigo} - {titulo}",
            xaxis_title="Semana",
            yaxis_title="Percentual (%)",
            template="plotly_white",
            height=600,
            xaxis=dict(
                tickangle=45,
                tickfont=dict(color="black")
            )
        )


        with grafico_placeholder.container():
            st.plotly_chart(fig, use_container_width=True)
            st.download_button(
                label="💾 Baixar histórico CSV",
                data=historico.to_csv(index=False).encode('utf-8'),
                file_name=f"historico_{codigo}.csv",
                mime="text/csv",
                key=f"download_{codigo}"
            )
    else:
        st.info("📂 Nenhum histórico encontrado ainda.")

    # 5
    semana = st.text_input("📅 Informe a semana (ex: 45) e pressione Enter:")

    if semana:
        if os.path.exists(arquivo):
            historico = pd.read_csv(arquivo)
        else:
            historico = pd.DataFrame(columns=["Semana", "CG<=75%", "75%<CG<=100%", "CG>100%"])

        nova_linha = {
            "Semana": semana,
            "CG<=75%": perc_75,
            "75%<CG<=100%": perc_100,
            "CG>100%": perc_acima
        }

        historico = historico[historico["Semana"] != semana]
        historico = pd.concat([historico, pd.DataFrame([nova_linha])], ignore_index=True)

        # 🔹 Ordena antes de salvar e exibir
        historico["Semana"] = historico["Semana"].astype(str)
        historico = historico.sort_values(
            by="Semana",
            key=lambda x: x.astype(str).str.extract(r'(\d+)')[0].astype(float),
            ascending=True
)


        historico.to_csv(arquivo, index=False)

        st.success(f"✅ Semana '{semana}' salva no histórico!")

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="CG ≤ 75%",
            x=historico["Semana"],
            y=historico["CG<=75%"],
            marker_color="green",
            text=[f"{cg_75}"] * len(historico), 
            textposition="inside", 
            insidetextanchor="middle",  
            textfont=dict(color="black", size=12)
        ))
        fig2.add_trace(go.Bar(
            name="75% < CG ≤ 100%",
            x=historico["Semana"],
            y=historico["75%<CG<=100%"],
            marker_color="yellow",
            text=[f"{cg_100}"] * len(historico),
            textposition="inside", 
            insidetextanchor="middle",  
            textfont=dict(color="black", size=12)
        ))
        fig2.add_trace(go.Bar(
            name="CG > 100%",
            x=historico["Semana"],
            y=historico["CG>100%"],
            marker_color="red",
            text=[f"{cg_acima}"] * len(historico),
            textposition="inside", 
            insidetextanchor="middle",  
            textfont=dict(color="black", size=12)
        ))

        fig2.update_layout(
            barmode='stack',
            title=f"CG - {codigo} - {titulo}",
            yaxis_title="(%)",
            template="plotly_white",
            height=700,
            xaxis=dict(
                tickangle=45,
                tickfont=dict(color="black")
            )
        )

        with grafico_placeholder.container():
            st.plotly_chart(fig2, use_container_width=True)
            st.download_button(
                label="💾 Baixar histórico CSV",
                data=historico.to_csv(index=False).encode('utf-8'),
                file_name=f"historico_{codigo}.csv",
                mime="text/csv",
                key=f"download_{codigo}_novo"
            )
