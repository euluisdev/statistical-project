import React, { useEffect, useState } from "react";
import { Streamlit } from "streamlit-component-lib";
import "./App.css";

function App({ args = {} }) {
  const [selectedYear, setSelectedYear] = useState(2025);
  const [selectedWeek, setSelectedWeek] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [pontos, setPontos] = useState([]);
  const [selectedPoints, setSelectedPoints] = useState([]);
  const [dadosPorPonto, setDadosPorPonto] = useState({});
  const [dataframeCompleto, setDataframeCompleto] = useState([]); 
  const [actionPoints, setActionPoints] = useState([]); 

  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(900);
  })

  useEffect(() => {
    if (args) {
      console.log('Args recebidos:', args);
      
      if (args.pontos) {
        setPontos(args.pontos);
        console.log('Pontos:', args.pontos);
      }
      if (args.dadosPorPonto) {
        setDadosPorPonto(args.dadosPorPonto);
      }
      if (args.dataframeCompleto) {
        setDataframeCompleto(args.dataframeCompleto);
        console.log('Total registros:', args.dataframeCompleto.length);
      }
    }
  }, [args]);

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

  const addSelectedToAction = () => {
  if (selectedPoints.length === 0) return;

  setActionPoints(prev => [
    ...prev,
    ...selectedPoints.filter(p => !prev.includes(p))
  ]);
  setSelectedPoints([]);
  };
  const removeSelectedFromAction = () => {
  if (selectedPoints.length === 0) return;

  setActionPoints(prev =>
    prev.filter(p => !selectedPoints.includes(p))
  );

  setSelectedPoints([]);
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
            <div className="modal-header">
              <h3>Action Plan</h3>
              <button className="modal-close" onClick={() => setIsModalOpen(false)}>×</button>
            </div>

            <div className="modal-body">
              <div className="modal-section">
                <h4>Plano</h4>
                
                <div className="form-group">
                  <label>Número da Ação</label>
                  <div className="number-control">
                    <select className="action-select">
                      <option>001</option>
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
                    </select>
                    <select className="filter-select">
                      <option>Red</option>
                    </select>
                  </div>
                </div>

                {/* pnt eixo */}
                <div className="points-box">
                  {pontos.length > 0 ? (
                    pontos.map((ponto, idx) => (
                      <div 
                        key={idx}
                        className={`point-item ${selectedPoints.includes(ponto) ? 'selected' : ''}`}
                        onClick={() => togglePoint(ponto)}
                        style={{ cursor: 'pointer' }}
                        title={dadosPorPonto[ponto] ? 
                          `${dadosPorPonto[ponto].localizacao} - ${dadosPorPonto[ponto].tipo_geo}` : 
                          ''
                        }
                      >
                        {ponto}
                      </div>
                    ))
                  ) : (
                    <div style={{ opacity: 0.7, fontStyle: 'italic', textAlign: 'center' }}>
                      Nenhum ponto carregado
                    </div>
                  )}
                </div>

                <div className="scroll-buttons">
                  <button className="btn-scroll" onClick={addSelectedToAction}>&gt;</button>
                  <button className="btn-scroll" onClick={removeSelectedFromAction}>&lt;</button>
                </div>

                <label className="checkbox-label">
                  <input type="checkbox" defaultChecked />
                  Somente pontos cálculo
                </label>

                {/*contador */}
                <div className="number-display">{selectedPoints.length}</div>
              </div>

              {/* 2history */}
              <div className="modal-section wide">
                <h4>Ação</h4>

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
                      {actionPoints.length === 0 ? (
                        <div style={{ opacity: 0.6, fontStyle: "italic" }}>Nenhum ponto</div>
                      ) : (
                        actionPoints.map((ponto, idx) => (
                          <div
                            key={idx}
                            className={`point-item ${selectedPoints.includes(ponto) ? "selected" : ""}`}
                            onClick={() => togglePoint(ponto)}
                          >
                            {ponto}
                          </div>
                        ))
                      )}
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