import React, { useEffect, useState } from "react";
import { Streamlit } from "streamlit-component-lib";
import "./App.css";

function App() {
  const [selectedYear, setSelectedYear] = useState(2025);
  const [selectedWeek, setSelectedWeek] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [pontos, setPontos] = useState([]);
  const [selectedPoints, setSelectedPoints] = useState([]);
  const [dadosPorPonto, setDadosPorPonto] = useState({});

  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(900);

    //listner receber dados st
    window.addEventListener("message", (event) => {
      const data = event.data;
      
      //mensagem com args?
      if (data.type === "streamlit:render" && data.args) {
        console.log("Recebi args do streamlit:", data.args);
        
        if (data.args.pontos) {
          setPontos(data.args.pontos);
        }
        if (data.args.dados_por_ponto) {
          setDadosPorPonto(data.args.dados_por_ponto);
        }
      }
    });

    //fallback
    if (window.STREAMLIT_DATA) {
      console.log("Usando window.STREAMLIT_DATA:", window.STREAMLIT_DATA);
      setPontos(window.STREAMLIT_DATA.pontos || []);
      setDadosPorPonto(window.STREAMLIT_DATA.dadosPorPonto || {});
    }
  }, []);

  const getWeeksRange = (startWeek) => {
    const weeks = [];
    for (let i = 0; i < 10; i++) {
      let week = startWeek + i;
      if (week > 52) week = week - 52;
      weeks.push(week);
    }
    return weeks;
  };

  const weeks = getWeeksRange(selectedWeek);

  const handleWeekChange = (e) => {
    const newWeek = parseInt(e.target.value);
    setSelectedWeek(newWeek);
  };

  const handleYearChange = (e) => {
    setSelectedYear(parseInt(e.target.value));
  };

  const togglePoint = (ponto) => {
    setSelectedPoints(prev => 
      prev.includes(ponto) 
        ? prev.filter(p => p !== ponto)
        : [...prev, ponto]
    );
  };
  return (
    <div className="app-container">
      {/*toolbar */}
      <div className="toolbar">
        <select value={selectedYear} onChange={handleYearChange} className="select-year">
          <option value={2024}>Year 2024</option>
          <option value={2025}>Year 2025</option>
          <option value={2026}>Year 2026</option>
        </select>

        <select value={selectedWeek} onChange={handleWeekChange} className="select-week">
          {Array.from({ length: 52 }, (_, i) => i + 1).map((week) => (
            <option key={week} value={week}>
              {week}
            </option>
          ))}
        </select>

        <button className="btn">📖</button>
        <button className="btn">🏆</button>
        <label className="checkbox-label">
          <input type="checkbox" /> Point to point
        </label>
        <select className="select-small">
          <option>CPK</option>
        </select>
        <select className="select-small">
          <option>All</option>
        </select>
        <button className="btn">🖨️</button>
        <button className="btn">🔍</button>
        <button className="btn">📊</button>
        <button className="btn">⚠️ RISK</button>
        <button className="btn">📋</button>
        <button className="btn">🏠</button>
        <button className="btn" onClick={() => setIsModalOpen(true)}>➕</button>
      </div>

      {/*title */}
      <div className="title-bar">534895200 - REAR RAIL RT</div>

      {/*table*/}
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th rowSpan={2}>SEQ</th>
              <th rowSpan={2}>LABEL</th>
              <th rowSpan={2}>AXIS</th>
              <th rowSpan={2}>LSE</th>
              <th rowSpan={2}>LIE</th>
              <th rowSpan={2}>SYMBOL</th>
              <th rowSpan={2}>X-MÉDIO</th>
              <th rowSpan={2}>CP</th>
              <th rowSpan={2}>CPK</th>
              <th rowSpan={2}>RANGE</th>
              <th rowSpan={2}>RISK - Desviation</th>
              <th rowSpan={2}>RISK - Root Cause</th>
              <th rowSpan={2} style={{ width: "150px" }}>ACTION PLAN</th>
              <th rowSpan={2} style={{ width: "120px" }}>RESPONSIBLE</th>
              <th rowSpan={2} style={{ width: "70px" }}>DATA</th>
              <th colSpan={10} className="week-header">SEMANA</th>
              <th rowSpan={2} style={{ width: "80px" }}>STATUS</th>
            </tr>
            <tr>
              {weeks.map((week) => (
                <th
                  key={week}
                  className={`week-cell ${week === selectedWeek ? "selected-week" : ""}`}
                >
                  {week}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: 15 }).map((_, i) => (
              <tr key={i}>
                {Array.from({ length: 15 + weeks.length + 1 }).map((_, j) => (
                  <td key={j}></td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/*legend */}
      <div className="legend">
        <strong>X</strong> - Ação programada; <strong>NOK</strong> - Ação não efetiva;{" "}
        <strong>R</strong> - Ação reprogramada
      </div>

      {/* MODAL */}
      {isModalOpen && (
        <div className="modal-overlay" onClick={() => setIsModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            {/* Header */}
            <div className="modal-header">
              <h3>Action Plan</h3>
              <button className="modal-close" onClick={() => setIsModalOpen(false)}>×</button>
            </div>

            <div className="modal-body">
              {/* 1 action */}
              <div className="modal-section">
                <h4>Ação</h4>
                
                <div className="form-group">
                  <label>Número da Ação</label>
                  <div className="number-control">
                    <select className="action-select">
                      <option>001</option>
                      <option>002</option>
                      <option>003</option>
                    </select>
                    <button className="btn-control">-</button>
                    <button className="btn-control">+</button>
                  </div>
                </div>

                <div className="form-group">
                  <label>Filtro</label>
                  <div className="filter-group">
                    <select className="filter-select">
                      <option>Conformity</option>
                      <option>CPK</option>
                    </select>
                    <select className="filter-select">
                      <option>Red</option>
                      <option>Yellow</option>
                    </select>
                  </div>
                </div>

                {/*pnt dinamicos */}
                <div className="points-box">
                  {pontos.length > 0 ? (
                    pontos.map((ponto, idx) => (
                      <div 
                        key={idx}
                        className={`point-item ${selectedPoints.includes(ponto) ? 'selected' : ''}`}
                        onClick={() => togglePoint(ponto)}
                        style={{ cursor: 'pointer' }}
                      >
                        {ponto}
                      </div>
                    ))
                  ) : (
                    <div style={{ opacity: 0.7, fontStyle: 'italic' }}>
                      Nenhum ponto carregado
                    </div>
                  )}
                </div>

                <div className="scroll-buttons">
                  <button className="btn-scroll">&gt;</button>
                  <button className="btn-scroll">&lt;</button>
                </div>

                <label className="checkbox-label">
                  <input type="checkbox" defaultChecked />
                  Somente pontos cálculo
                </label>

                {/*contador */}
                <div className="number-display">{selectedPoints.length}</div>

                <div className="scroll-buttons">
                  <button className="btn-scroll">&gt;</button>
                  <button className="btn-scroll">&lt;</button>
                </div>

                <label className="checkbox-label">
                  <input type="checkbox" defaultChecked />
                  Somente pontos cálculo
                </label>

                <div className="number-display">2</div>
              </div>

              {/* 2history */}
              <div className="modal-section wide">
                <h4>Histórico</h4>

                <div className="radio-group">
                  <label><input type="radio" name="status" defaultChecked /> X - Ação programada</label>
                  <label><input type="radio" name="status" /> R - Ação reprogramada</label>
                  <label><input type="radio" name="status" /> NOK - Ação não efetiva</label>
                  <label><input type="radio" name="status" /> Não definida</label>
                </div>

                <div className="history-content">
                  <div className="history-left">
                    <h5>Pontos da Ação</h5>
                    <div className="points-list">
                      <div>PT_187T</div>
                      <div>PT_125T</div>
                      <div className="selected">PT_125T</div>
                    </div>
                    <button className="btn-remove">Remover todos</button>
                  </div>

                  <div className="history-right">
                    <h5>Ação de execução</h5>
                    <textarea 
                      className="action-textarea"
                      defaultValue="corrigir material&#10;( TRIDENTE DX )"
                    />
                  </div>
                </div>

                <div className="status-grid">
                  <div className="status-item">
                    <label>Status</label>
                    <div className="status-box"></div>
                  </div>
                  <div className="status-item">
                    <label>Analisys</label>
                    <select className="analysis-select">
                      <option>Process</option>
                    </select>
                  </div>
                </div>
              </div>

              {/*3responsabilidade */}
              <div className="modal-section">
                <h4>Responsabilidade</h4>

                <div className="form-group">
                  <div className="name-control">
                    <div className="name-box">EVERTON (FERRAMENTARIA)</div>
                    <div className="nav-buttons">
                      <button className="btn-nav">&gt;</button>
                      <button className="btn-nav">&lt;</button>
                    </div>
                  </div>
                </div>

                <div className="form-group">
                  <label>Nome</label>
                  <div className="dept-control">
                    <select className="dept-select">
                      <option>ITEM DE CONTA TRABALHO</option>
                    </select>
                    <button className="btn-control">+</button>
                    <button className="btn-control">-</button>
                  </div>
                </div>

                <div className="form-group">
                  <label>Departamento</label>
                  <div className="dept-control">
                    <select className="dept-select">
                      <option>QUALIDADE METROLOGIA</option>
                    </select>
                    <button className="btn-control">+</button>
                    <button className="btn-control">-</button>
                  </div>
                </div>

                <div className="action-buttons">
                  <button className="btn-action">Remover</button>
                  <button className="btn-action">Limpar</button>
                </div>
              </div>

              {/*4 prazo */}
              <div className="modal-section-right">
                <div className="modal-section">
                  <h4>Prazo</h4>
                  <input type="date" className="date-input" defaultValue="2025-11-20" />
                  <select className="year-select">
                    <option>Year 2025</option>
                  </select>
                  <select className="week-label">
                    <option>Week</option>
                  </select>
                  <input type="number" className="week-input" defaultValue="47" />
                </div>

                <div className="modal-section">
                  <h4>Registro</h4>
                  <button className="btn-save">Gravar</button>
                  <button className="btn-export">Exportar</button>
                  <div className="icon-buttons">
                    <button className="btn-icon">📁</button>
                    <button className="btn-icon">🖨️</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;