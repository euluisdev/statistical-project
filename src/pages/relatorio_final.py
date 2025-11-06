import streamlit as st
import json
import streamlit.components.v1 as components

def relatorio_final():
    st.title("📄 Relatório Final (Custom HTML)")

    if "trend_pages" not in st.session_state or len(st.session_state["trend_pages"]) == 0:
        st.warning("⚠️ Nenhum gráfico salvo ainda. Salve gráficos na página Trend Chart.")
        st.stop()

    # dados para o frontend
    dados_graficos = json.dumps(st.session_state["trend_pages"])

    html = f"""
    <style>
      body {{ font-family: Arial, Helvetica, sans-serif; margin: 0; padding: 8px; }}
      .container {{ max-width: 1100px; margin: 0 auto; }}
      .controls {{ display:flex; gap:12px; align-items:center; margin-bottom:12px; }}
      .list {{ width: 320px; height: 220px; overflow:auto; border:1px solid #ddd; padding:8px; border-radius:6px; }}
      .preview {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(280px,1fr)); gap:12px; margin-top:12px; }}
      .card img {{ width:100%; height:auto; border-radius:6px; box-shadow: 0 1px 6px rgba(0,0,0,0.08); }}
      .btn {{ background:#007acc; color:white; border:none; padding:8px 12px; border-radius:6px; cursor:pointer; }}
      .btn:active{{}}
    </style>

    <div class="container">
      <div class="controls">
        <div>
          <strong>📌 Gráficos disponíveis</strong>
          <div class="list" id="lista"></div>
        </div>
        <div style="flex:1">
          <button class="btn" id="addBtn">✅ Adicionar ao relatório</button>
          <div style="margin-top:8px; color:#666; font-size:13px;">Selecione os itens na lista à esquerda</div>
        </div>
      </div>

      <h4>🖼 Pré-visualização</h4>
      <div class="preview" id="preview"></div>
    </div>

    <script>
    const graficos = {dados_graficos};
    const lista = document.getElementById('lista');
    const preview = document.getElementById('preview');
    // popular lista com checkboxes
    graficos.forEach((g, idx) => {{
      const id = 'chk_' + idx;
      const row = document.createElement('div');
      row.style.marginBottom = '6px';
      row.innerHTML = `
        <label style="display:flex;align-items:center;gap:8px;">
          <input id="${{id}}" type="checkbox" value="${{g.nome}}" data-path="${{g.arquivo}}">
          <span style="font-size:13px">${{g.nome}}</span>
        </label>
      `;
      lista.appendChild(row);
      // clique para mostrar preview ao marcar/desmarcar
      document.getElementById(id).addEventListener('change', atualizarPreview);
    }});

    function atualizarPreview() {{
      preview.innerHTML = '';
      const checks = Array.from(document.querySelectorAll('#lista input[type=checkbox]'));
      checks.forEach(ch => {{
        if (ch.checked) {{
          const src = ch.getAttribute('data-path');
          const nome = ch.value;
          const card = document.createElement('div');
          card.className = 'card';
          card.innerHTML = `<img src="${{src}}" alt="${{nome}}"><div style="font-weight:600;margin-top:6px">${{nome}}</div>`;
          preview.appendChild(card);
        }}
      }});
    }}

    // Ao clicar em "Adicionar", enviamos uma message para o parent (iframe -> streamlit)
    document.getElementById('addBtn').addEventListener('click', () => {{
      const selecionados = Array.from(document.querySelectorAll('#lista input[type=checkbox]:checked')).map(c => c.value);
      if (selecionados.length === 0) {{
        alert('Selecione ao menos um gráfico.');
        return;
      }}
      // envia dados para o parent do iframe (Streamlit)
      window.parent.postMessage({{ type: 'relatorio_final_selecionados', selecionados }}, '*');
      // opcional: feedback visual
      alert(selecionados.length + ' gráfico(s) selecionado(s) e enviados ao app Streamlit (ver console Python).');
    }});
    </script>
    """

    # Renderiza HTML+JS dentro de um iframe — scripts irão rodar aqui
    components.html(html, height=550, scrolling=True)