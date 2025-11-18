import React, { useState, useEffect } from "react";

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
  setActionPoints,
  saveAction,
  selectedWeek,
  selectedYear,
  nextActionNumber
}) {
  const [numeroAcao, setNumeroAcao] = useState(String(nextActionNumber).padStart(3, '0'));
  const [statusAcao, setStatusAcao] = useState('X');
  const [acaoExecucao, setAcaoExecucao] = useState('');
  const [analysis, setAnalysis] = useState('Process');
  const [responsible, setResponsible] = useState('ITEM DE CONTA TRABALHO');
  const [department, setDepartment] = useState('QUALIDADE METROLOGIA');
  const [prazo, setPrazo] = useState(new Date().toISOString().split('T')[0]);
  const [year, setYear] = useState(selectedYear);
  const [week, setWeek] = useState(selectedWeek);

  useEffect(() => {
    setNumeroAcao(String(nextActionNumber).padStart(3, '0'));
  }, [nextActionNumber]);

  useEffect(() => {
    setWeek(selectedWeek);
    setYear(selectedYear);
  }, [selectedWeek, selectedYear]);

  const handleSave = async () => {
    if (actionPoints.length === 0) {
      alert('Adicione pelo menos um ponto à ação!');
      return;
    }

    if (!acaoExecucao.trim()) {
      alert('Descreva a ação de execução!');
      return;
    }

    const actionData = {
      numeroAcao,
      pontos: actionPoints,
      statusAcao,
      acaoExecucao,
      analysis,
      responsible,
      department,
      prazo,
      year,
      week
    };

    const success = await saveAction(actionData);
    
    if (success) {
      // Limpa o formulário
      setActionPoints([]);
      setAcaoExecucao('');
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Action Plan</h3>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          {/* 1. Plano */}
          <div className="modal-section">
            <h4>Plano</h4>
            
            <div className="form-group">
              <label>Número da Ação</label>
              <div className="number-control">
                <input 
                  type="text" 
                  className="action-select" 
                  value={numeroAcao}
                  onChange={(e) => setNumeroAcao(e.target.value)}
                  style={{ width: '100%', padding: '4px' }}
                />
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
                        `CPK: ${stats.cpk} | CP: ${stats.cp}\nX-Médio: ${stats.xMedio} | Range: ${stats.range}` : 
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

          {/* 2. Ação */}
          <div className="modal-section wide">
            <h4>Ação</h4>

            <div className="radio-group">
              <label>
                <input 
                  type="radio" 
                  name="status" 
                  value="X"
                  checked={statusAcao === 'X'}
                  onChange={(e) => setStatusAcao(e.target.value)}
                /> X - Ação programada
              </label>
              <label>
                <input 
                  type="radio" 
                  name="status" 
                  value="R"
                  checked={statusAcao === 'R'}
                  onChange={(e) => setStatusAcao(e.target.value)}
                /> R - Ação reprogramada
              </label>
              <label>
                <input 
                  type="radio" 
                  name="status" 
                  value="NOK"
                  checked={statusAcao === 'NOK'}
                  onChange={(e) => setStatusAcao(e.target.value)}
                /> NOK - Ação não efetiva
              </label>
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
                  value={acaoExecucao}
                  onChange={(e) => setAcaoExecucao(e.target.value)}
                />
              </div>
            </div>

            <div className="status-grid">
              <div className="status-item">
                <label>Status</label>
                <div className="status-box"></div>
              </div>
              <div className="status-item">
                <label>Analysis</label>
                <select 
                  className="analysis-select"
                  value={analysis}
                  onChange={(e) => setAnalysis(e.target.value)}
                >
                  <option>Parts</option>
                  <option>Process</option>
                  <option>Investigation</option>
                </select>
              </div>
            </div>
          </div>

          {/* 3. Responsabilidade */}
          <div className="modal-section">
            <h4>Responsabilidade</h4>

            <div className="form-group">
              <label>Nome</label>
              <div className="dept-control">
                <input 
                  type="text"
                  className="dept-select"
                  value={responsible}
                  onChange={(e) => setResponsible(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Departamento</label>
              <div className="dept-control">
                <input 
                  type="text"
                  className="dept-select"
                  value={department}
                  onChange={(e) => setDepartment(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* 4. Prazo e Registro */}
          <div className="modal-section-right">
            <div className="modal-section">
              <h4>Prazo</h4>
              <input 
                type="date" 
                className="date-input" 
                value={prazo}
                onChange={(e) => setPrazo(e.target.value)}
              />
              <select 
                className="year-select"
                value={year}
                onChange={(e) => setYear(parseInt(e.target.value))}
              >
                <option value={2024}>Year 2024</option>
                <option value={2025}>Year 2025</option>
                <option value={2026}>Year 2026</option>
              </select>
              <input 
                type="number" 
                className="week-input" 
                value={week}
                onChange={(e) => setWeek(parseInt(e.target.value))}
                min="1"
                max="52"
              />
            </div>

            <div className="modal-section">
              <h4>Registro</h4>
              <button className="btn-save" onClick={handleSave}>Gravar</button>
              <button className="btn-export">Exportar</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Modal;