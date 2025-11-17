import React from "react";

function Modal({ 
  isOpen, 
  onClose, 
  tipoFiltro,
  valorFiltro,
  setTipoFiltro,
  setValorFiltro,
  pontosFiltrados,
  pontosProcessados,
  selectedPoints,
  togglePoint,
  addSelectedToAction,
  removeSelectedFromAction,
  actionPoints,
  setActionPoints
}) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Action Plan</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {/*1 plano */}
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
                <select 
                  className="filter-select"
                  value={valorFiltro}
                  onChange={(e) => setValorFiltro(e.target.value)}
                >
                  <option value="all">Todos</option>
                  {tipoFiltro === 'conformidade' && (
                    <>
                      <option value="green">✅ Aprovado</option>
                      <option value="yellow">⚠️ Alerta</option>
                      <option value="red">❌ Reprovado</option>
                    </>
                  )}
                  {(tipoFiltro === 'cpk' || tipoFiltro === 'cp') && (
                    <>
                      <option value="approved">≥ 1.33</option>
                      <option value="alert">1.0-1.33</option>
                      <option value="rejected">&lt; 1.0</option>
                    </>
                  )}
                </select>
                
                {/* filtro */}
                <select 
                  className="filter-select"
                  value={tipoFiltro}
                  onChange={(e) => {
                    setTipoFiltro(e.target.value);
                    setValorFiltro('all');
                  }}
                >
                  <option value="conformidade">Conformidade</option>
                  <option value="cpk">CPK</option>
                  <option value="cp">CP</option>
                </select>
              </div>
            </div>

            {/* Pontos com filtros */}
            <div className="points-box">
              {pontosFiltrados.length > 0 ? (
                pontosFiltrados.map((ponto, idx) => {
                  const stats = pontosProcessados[ponto]?.stats;
                  
                  return (
                    <div 
                      key={idx}
                      className={`point-item ${selectedPoints.includes(ponto) ? 'selected' : ''}`}
                      onClick={() => togglePoint(ponto)}
                      style={{ cursor: 'pointer' }}
                      title={stats ? 
                        `CPK: ${stats.cpk} | CP: ${stats.cp}\nX-Médio: ${stats.xMedio} | Range: ${stats.range}\nRISK Dev: ${stats.riskDeviation}% | RISK Root: ${stats.riskRootCause}%` : 
                        ponto
                      }
                    >
                      {ponto}
                    </div>
                  );
                })
              ) : (
                <div style={{ opacity: 0.7, fontStyle: 'italic', textAlign: 'center', padding: '20px' }}>
                  Nenhum ponto neste filtro
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

            <div className="number-display">{selectedPoints.length}</div>
          </div>

          {/* 2 acao */}
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

                <button className="btn-remove" onClick={() => setActionPoints([])}>
                  Remover todos
                </button>
              </div>

              <div className="history-right">
                <h5>Ação de execução</h5>
                <textarea 
                  className="action-textarea"
                  placeholder="Descreva a ação corretiva..."
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
                  <option>Parts</option>
                  <option>Process</option>
                  <option>Investigation</option>
                </select>
              </div>
            </div>
          </div>

          {/* 3 responsabilidade */}
          <div className="modal-section">
            <h4>Responsabilidade</h4>

            <div className="form-group">
              <div className="name-control">
                <div className="name-box">ITEM DE CONTA TRABALHO (QUALIDADE METROLOGIA)</div>
                <div className="nav-buttons">
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
  );
}

export default Modal;