import React, { useEffect, useState } from "react";
import { Streamlit } from "streamlit-component-lib";
import "./App.css";
import { 
  processarTodosPontos, 
  filtrarPorConformidade, 
  filtrarPorCPK 
} from "./utils";
import Modal from "./Modal";

function App({ args = {} }) {
  const [selectedYear, setSelectedYear] = useState(2025);
  const [selectedWeek, setSelectedWeek] = useState(1);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [pontos, setPontos] = useState([]);
  const [pontosFiltrados, setPontosFiltrados] = useState([]);
  const [selectedPoints, setSelectedPoints] = useState([]);
  const [dadosPorPonto, setDadosPorPonto] = useState({});
  const [dataframeCompleto, setDataframeCompleto] = useState([]);
  const [actionPoints, setActionPoints] = useState([]);
  const [pontosProcessados, setPontosProcessados] = useState({});
  
  // Filtros
  const [tipoFiltro, setTipoFiltro] = useState('conformidade'); // 'cp', 'cpk', 'conformidade'
  const [valorFiltro, setValorFiltro] = useState('all');

  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(900);
  }, []);

  // Recebe dados do Streamlit
  useEffect(() => {
    if (args) {
      console.log('📦 Args recebidos:', args);
      
      if (args.pontos) {
        setPontos(args.pontos);
        setPontosFiltrados(args.pontos);
        console.log('✅ Pontos:', args.pontos);
      }
      if (args.dadosPorPonto) {
        setDadosPorPonto(args.dadosPorPonto);
      }
      if (args.dataframeCompleto) {
        setDataframeCompleto(args.dataframeCompleto);
        console.log('📋 Total registros:', args.dataframeCompleto.length);
        
        // 🔥 PROCESSA TODOS OS PONTOS COM CÁLCULOS
        const processados = processarTodosPontos(args.dataframeCompleto);
        setPontosProcessados(processados);
        console.log('📊 Pontos processados com stats:', processados);
      }
    }
  }, [args]);

  // 🔥 APLICA FILTROS AUTOMATICAMENTE
  useEffect(() => {
    if (Object.keys(pontosProcessados).length === 0) {
      setPontosFiltrados(pontos);
      return;
    }

    let filtrados = Object.keys(pontosProcessados);

    if (valorFiltro === 'all') {
      setPontosFiltrados(filtrados);
      return;
    }

    // Filtra baseado no tipo escolhido
    filtrados = filtrados.filter(chave => {
      const ponto = pontosProcessados[chave];
      if (!ponto.stats) return false;

      const { cp, cpk, conformidade } = ponto.stats;

      switch(tipoFiltro) {
        case 'conformidade':
          return conformidade === valorFiltro;
        
        case 'cpk':
          const cpkVal = parseFloat(cpk);
          switch(valorFiltro) {
            case 'approved': return cpkVal >= 1.33;
            case 'alert': return cpkVal >= 1 && cpkVal < 1.33;
            case 'rejected': return cpkVal < 1;
            default: return true;
          }
        
        case 'cp':
          const cpVal = parseFloat(cp);
          switch(valorFiltro) {
            case 'approved': return cpVal >= 1.33;
            case 'alert': return cpVal >= 1 && cpVal < 1.33;
            case 'rejected': return cpVal < 1;
            default: return true;
          }
        
        default:
          return true;
      }
    });

    setPontosFiltrados(filtrados);
    console.log(`🔍 Filtro ${tipoFiltro} = ${valorFiltro}: ${filtrados.length} pontos`);
  }, [tipoFiltro, valorFiltro, pontosProcessados, pontos]);

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
    setSelectedWeek(parseInt(e.target.value));
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
        
        {/* 🔥 FILTRO 1: VALOR (muda baseado no tipo) */}
        <select 
          className="select-small"
          value={valorFiltro}
          onChange={(e) => setValorFiltro(e.target.value)}
        >
          <option value="all">All</option>
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
        
        {/* 🔥 FILTRO 2: TIPO (CP, CPK, Conformidade) */}
        <select 
          className="select-small"
          value={tipoFiltro}
          onChange={(e) => {
            setTipoFiltro(e.target.value);
            setValorFiltro('all'); // Reset valor ao mudar tipo
          }}
        >
          <option value="conformidade">Conformidade</option>
          <option value="cpk">CPK</option>
          <option value="cp">CP</option>
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
        {pontosFiltrados.length > 0 && (
          <span style={{ marginLeft: '20px', color: '#666' }}>
            | {pontosFiltrados.length} pontos exibidos
          </span>
        )}
      </div>

      {/* MODAL */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        pontosFiltrados={pontosFiltrados}
        selectedPoints={selectedPoints}
        togglePoint={togglePoint}
        valorFiltro={valorFiltro}
        setValorFiltro={setValorFiltro}
        tipoFiltro={tipoFiltro}
        setTipoFiltro={setTipoFiltro}
        pontosProcessados={pontosProcessados}
        addSelectedToAction={addSelectedToAction}
        removeSelectedFromAction={removeSelectedFromAction}
        actionPoints={actionPoints}
        setActionPoints={setActionPoints}
      />

    </div>
  );
}

export default App;