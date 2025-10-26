import pandas as pd
import re

def ler_relatorio_pcdmis(caminho_arquivo):
    # Tenta abrir com UTF-8, se falhar tenta Latin-1 (ISO-8859-1)
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except UnicodeDecodeError:
        with open(caminho_arquivo, "r", encoding="latin-1") as f:
            linhas = f.readlines()

    data, hora, bloco = None, None, None
    dados = []

    for linha in linhas:
        linha = linha.strip()
        if linha.startswith("DATA:") or linha.startswith(" DATA:"):
            data = linha.split(":")[1].strip()
        elif linha.startswith("HORA:") or linha.startswith(" HORA:"):
            hora = linha.split(":")[1].strip()
        elif linha.startswith("DIM LOC"):
            bloco = re.search(r"DIM (LOC\d+)", linha)
            bloco = bloco.group(1) if bloco else "DESCONHECIDO"
        elif re.match(r"^[XYZD]\s", linha):
            partes = linha.split()
            if len(partes) >= 6:
                eixo = partes[0]
                nominal = float(partes[1])
                medido = float(partes[2])
                desvio = float(partes[3])
                tol_plus = float(partes[4])
                tol_minus = float(partes[5])
                dados.append([data, hora, bloco, eixo, nominal, medido, desvio, tol_plus, tol_minus])

    df = pd.DataFrame(
        dados,
        columns=["Data", "Hora", "Localização", "Eixo", "Nominal", "Medido", "Desvio", "Tol+", "Tol-"]
    )
    return df
