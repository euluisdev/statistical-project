import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="ACTION PLAN", layout="wide")

#1
st.markdown("""
<style>
    /* Remover padding padrão do Streamlit */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .toolbar {
        display: flex;
        gap: 5px;
        margin-bottom: 10px;
        align-items: center;
        background-color: #f0f0f0;
        padding: 5px;
        border: 1px solid #ccc;
    }
    
    .toolbar select, .toolbar input {
        padding: 5px;
        border: 1px solid #999;
        background-color: white;
    }
    
    .toolbar button {
        padding: 5px 10px;
        border: 1px solid #999;
        background-color: #e0e0e0;
        cursor: pointer;
    }
    
    /* Estilo da tabela - cópia exata da imagem */
    .action-plan-table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
        font-size: 11px;
        margin-top: 0;
    }
    
    .action-plan-table th {
        background-color: #c0c0c0;
        border: 1px solid #000;
        padding: 8px 4px;
        text-align: center;
        font-weight: bold;
        color: #000;
        vertical-align: middle;
    }
    
    .action-plan-table td {
        border: 1px solid #000;
        padding: 8px 4px;
        text-align: center;
        background-color: #fff;
        vertical-align: middle;
    }
    
    /* Header da semana */
    .semana-header {
        background-color: #d3d3d3 !important;
        font-weight: bold;
        writing-mode: horizontal-tb;
    }
    
    /* Semana atual destacada */
    .semana-atual {
        background-color: #808080 !important;
        color: white !important;
        font-weight: bold;
    }
    
    /* Colunas rotacionadas */
    .vertical-text {
        writing-mode: vertical-rl;
        transform: rotate(180deg);
        white-space: nowrap;
        padding: 4px 2px;
    }
    
    /* Larguras específicas das colunas */
    .col-seq { width: 35px; }
    .col-label { width: 70px; }
    .col-jms { width: 40px; }
    .col-lse { width: 40px; }
    .col-lie { width: 40px; }
    .col-symbol { width: 50px; }
    .col-limit { width: 45px; }
    .col-cp { width: 40px; }
    .col-cpk { width: 40px; }
    .col-range { width: 50px; }
    .col-data-inc { width: 60px; }
    .col-mes-inicio { width: 60px; }
    .col-action { width: 150px; }
    .col-responsible { width: 120px; }
    .col-data { width: 70px; }
    .col-week { width: 30px; }
    .col-status { width: 80px; }
    
    /* Altura das linhas */
    .action-plan-table tbody tr {
        height: 35px;
    }
    
    /* Título do projeto */
    .project-title {
        background-color: #e0e0e0;
        padding: 5px 10px;
        margin-bottom: 5px;
        border: 1px solid #999;
        font-weight: bold;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

#2
if 'action_plans' not in st.session_state:
    st.session_state.action_plans = []

if 'current_week' not in st.session_state:
    st.session_state.current_week = datetime.now().isocalendar()[1]

if 'current_year' not in st.session_state:
    st.session_state.current_year = datetime.now().year

toolbar_html = """
<div class="toolbar">
    <select style="width: 100px;">
        <option>Year 2025</option>
        <option>Year 2024</option>
        <option>Year 2026</option>
    </select>
    <select style="width: 80px;">
        <option>Week</option>
    </select>
        <select style="width: 100px;">
        <option>45</option>
        <option>46</option>
        <option>47</option>
    </select>
    <button>📖</button>
    <button>🏆</button>
    <label><input type="checkbox" /> Point to point</label>
    <select style="width: 80px;">
        <option>CPK</option>
    </select>
    <select style="width: 80px;">
        <option>All</option>
    </select>
    <button>🖨️</button>
    <button>🔍</button>
    <button>📊</button>
    <button>⚠️ RISK</button>
    <button>📋</button>
    <button>🏠</button>
    <button>➕</button>
</div>
"""

st.markdown(toolbar_html, unsafe_allow_html=True)
st.markdown('<div class="project-title">534895200 - REAR RAIL RT</div>', unsafe_allow_html=True)

current_week = st.session_state.current_week

table_html = """
<table class="action-plan-table">
    <thead>
        <tr>
            <th class="col-seq" rowspan="2">SEQ</th>
            <th class="col-label" rowspan="2">LABEL</th>
            <th class="col-jms" rowspan="2">AXIS</th>
            <th class="col-lse" rowspan="2">LSE</th>
            <th class="col-lie" rowspan="2">LIE</th>
            <th class="col-symbol" rowspan="2">SYMBOL</th>
            <th class="col-limit" rowspan="2">X-MÉDIO</th>
            <th class="col-cp" rowspan="2">CP</th>
            <th class="col-cpk" rowspan="2">CPK</th>
            <th class="col-range" rowspan="2">RANGE</th>
            <th class="col-data-inc" rowspan="2"><div class="vertical-text">RISK - Desviation</div></th>
            <th class="col-mes-inicio" rowspan="2"><div class="vertical-text">RISK - Root Cause</div></th>
            <th class="col-action" rowspan="2">ACTION PLAN</th>
            <th class="col-responsible" rowspan="2">RESPONSIBLE</th>
            <th class="col-data" rowspan="2">DATA</th>
            <th colspan="10" class="semana-header">SEMANA</th>
            <th class="col-status" rowspan="2">STATUS</th>
        </tr>
        <tr>
"""

#3
for week in range(43, 53):
    if week == 47:  
        table_html += f'<th class="col-week semana-atual">{week}</th>'
    else:
        table_html += f'<th class="col-week semana-header">{week}</th>'

table_html += '</tr></thead><tbody>'

for i in range(15):
    table_html += '<tr>'
    table_html += '<td></td>' * 15  
    table_html += '<td></td>' * 10  
    table_html += '<td></td>'  
    table_html += '</tr>'

table_html += '</tbody></table>'


st.markdown(table_html, unsafe_allow_html=True)

st.markdown("")
st.markdown("**X** - Ação programada; **NOK** - Ação não efetiva; **R** - Ação reprogramada")

