
export function calcularEstatisticasPonto(medicoes) {
  if (!medicoes || medicoes.length === 0) {
    return null;
  }

  const desvios = medicoes.map(m => parseFloat(m.Desvio) || 0);
  const medidos = medicoes.map(m => parseFloat(m.Medido) || 0);
  
  const primeira = medicoes[0];
  const LSE = parseFloat(primeira['Tol+']) || 0; 
  const LIE = parseFloat(primeira['Tol-']) || 0;  
  const nominal = parseFloat(primeira.Nominal) || 0;

  const xMedio = desvios.reduce((a, b) => a + b, 0) / desvios.length;
  const maxMedido = Math.max(...medidos);
  const minMedido = Math.min(...medidos);
  const range = maxMedido - minMedido;

  const mediaDosDesvios = desvios.reduce((a, b) => a + b, 0) / desvios.length;
  const variancia = desvios.reduce((sum, val) => sum + Math.pow(val - mediaDosDesvios, 2), 0) / (desvios.length - 1);
  const sigma = Math.sqrt(variancia);

  //tol
  const toleranciaTotal = LSE - LIE;

  //CP
  const cp = sigma > 0 ? toleranciaTotal / (6 * sigma) : 0;

  //CPK
  const cpkSuperior = (LSE - xMedio) / (3 * sigma);
  const cpkInferior = (xMedio - LIE) / (3 * sigma);
  const cpk = sigma > 0 ? Math.min(cpkSuperior, cpkInferior) : 0;

  //conformidade
  const conformidade = classificarConformidade(xMedio, LSE, LIE, cp, cpk);

  //RISK
  const foraLimites = desvios.filter(d => d < LIE || d > LSE).length;
  const riskDeviation = (foraLimites / desvios.length) * 100;

  // root cause
  const margem = toleranciaTotal * 0.2;  // 20% da tol
  const proximosLimites = desvios.filter(d => 
    d <= (LIE + margem) || d >= (LSE - margem)
  ).length;
  const riskRootCause = (proximosLimites / desvios.length) * 100;

  return {
    xMedio: xMedio.toFixed(3),
    range: range.toFixed(3),
    cp: cp.toFixed(2),
    cpk: cpk.toFixed(2),
    lse: LSE.toFixed(3),
    lie: LIE.toFixed(3),
    sigma: sigma.toFixed(3),
    conformidade: conformidade,
    riskDeviation: riskDeviation.toFixed(1),
    riskRootCause: riskRootCause.toFixed(1),
    totalMedicoes: medicoes.length,
    foraLimites: foraLimites
  };
}

export function classificarConformidade(xMedio, LSE, LIE, cp, cpk) {
  if (xMedio < LIE || xMedio > LSE || cpk < 1) {
    return 'red';
  }
  
  if (cpk >= 1 && cpk < 1.33) {
    return 'yellow';
  }
  return 'green';
}

export function processarTodosPontos(dataframe) {
  if (!dataframe || dataframe.length === 0) {
    return {};
  }

  const pontosPorEixo = {};

  //nomeponto + eixo
  dataframe.forEach(row => {
    const chave = `${row.NomePonto} - ${row.Eixo}`;
    
    if (!pontosPorEixo[chave]) {
      pontosPorEixo[chave] = {
        nomePonto: row.NomePonto,
        eixo: row.Eixo,
        localizacao: row.Localização,
        tipoGeometrico: row.TipoGeométrico,
        medicoes: []
      };
    }
    
    pontosPorEixo[chave].medicoes.push(row);
  });
  const resultado = {};
  
  Object.keys(pontosPorEixo).forEach(chave => {
    const ponto = pontosPorEixo[chave];
    const stats = calcularEstatisticasPonto(ponto.medicoes);
    
    resultado[chave] = {
      ...ponto,
      stats: stats,
      seq: chave.split(' - ')[0],  //posso smudar para um número sequencial depois
      label: ponto.nomePonto,
      axis: ponto.eixo
    };
  });

  return resultado;
}


export function filtrarPorConformidade(pontosProcessados, filtro) {
  if (filtro === 'all') {
    return Object.keys(pontosProcessados);
  }

  return Object.keys(pontosProcessados).filter(chave => {
    const ponto = pontosProcessados[chave];
    return ponto.stats && ponto.stats.conformidade === filtro;
  });
}


export function filtrarPorCPK(pontosProcessados, filtro) {
  if (filtro === 'all') {
    return Object.keys(pontosProcessados);
  }

  return Object.keys(pontosProcessados).filter(chave => {
    const ponto = pontosProcessados[chave];
    if (!ponto.stats) return false;

    const cpk = parseFloat(ponto.stats.cpk);

    switch(filtro) {
      case 'approved':
        return cpk >= 1.33;
      case 'alert':
        return cpk >= 1 && cpk < 1.33;
      case 'rejected':
        return cpk < 1;
      default:
        return true;
    }
  });
}


export function gerarLinhaTabelaAction(pontoProcessado, seq) {
  const stats = pontoProcessado.stats;
  
  return {
    seq: seq,
    label: pontoProcessado.label,
    axis: pontoProcessado.axis,
    lse: stats.lse,
    lie: stats.lie,
    symbol: pontoProcessado.tipoGeometrico,
    xMedio: stats.xMedio,
    cp: stats.cp,
    cpk: stats.cpk,
    range: stats.range,
    riskDeviation: stats.riskDeviation,
    riskRootCause: stats.riskRootCause,
    conformidade: stats.conformidade,
    actionPlan: '',  
    responsible: '',  
    data: '',  
    status: '',  
    semanas: {}  //X, NOK, R
  };
}