/**
 * Funções de cálculo para o Action Plan
 */

/**
 * Calcula estatísticas de um ponto baseado em múltiplas medições
 * @param {Array} medicoes - Array de objetos com medições do DataFrame
 * @returns {Object} - Estatísticas calculadas
 */
export function calcularEstatisticasPonto(medicoes) {
  if (!medicoes || medicoes.length === 0) {
    return null;
  }

  // Extrai valores de desvio
  const desvios = medicoes.map(m => parseFloat(m.Desvio) || 0);
  const medidos = medicoes.map(m => parseFloat(m.Medido) || 0);
  
  // Pega limites (assume que são iguais em todas as medições do ponto)
  const primeira = medicoes[0];
  const LSE = parseFloat(primeira['Tol+']) || 0;  // Limite Superior
  const LIE = parseFloat(primeira['Tol-']) || 0;  // Limite Inferior
  const nominal = parseFloat(primeira.Nominal) || 0;

  // Calcula X-MÉDIO (média dos desvios)
  const xMedio = desvios.reduce((a, b) => a + b, 0) / desvios.length;

  // 🔥 CALCULA RANGE CORRETO (diferença entre max e min dos DESVIOS)
  const maxDesvio = Math.max(...desvios);
  const minDesvio = Math.min(...desvios);
  const range = maxDesvio - minDesvio;

  // Calcula desvio padrão (sigma)
  const mediaDosDesvios = desvios.reduce((a, b) => a + b, 0) / desvios.length;
  const variancia = desvios.reduce((sum, val) => sum + Math.pow(val - mediaDosDesvios, 2), 0) / (desvios.length - 1);
  const sigma = Math.sqrt(variancia);

  // Calcula tolerância total
  const toleranciaTotal = LSE - LIE;

  // Calcula CP (Capability Process)
  const cp = sigma > 0 ? toleranciaTotal / (6 * sigma) : 0;

  // Calcula CPK (Capability Process Index)
  const cpkSuperior = (LSE - xMedio) / (3 * sigma);
  const cpkInferior = (xMedio - LIE) / (3 * sigma);
  const cpk = sigma > 0 ? Math.min(cpkSuperior, cpkInferior) : 0;

  // Classifica conformidade
  const conformidade = classificarConformidade(xMedio, LSE, LIE, cp, cpk);

  // Calcula RISK - Deviation (% de medições fora dos limites)
  const foraLimites = desvios.filter(d => d < LIE || d > LSE).length;
  const riskDeviation = (foraLimites / desvios.length) * 100;

  // Calcula RISK - Root Cause (proximidade dos limites)
  const margem = toleranciaTotal * 0.2;  // 20% da tolerância
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

/**
 * Classifica a conformidade baseado nos índices
 * @param {number} xMedio - Média dos desvios
 * @param {number} LSE - Limite Superior
 * @param {number} LIE - Limite Inferior
 * @param {number} cp - Índice CP
 * @param {number} cpk - Índice CPK
 * @returns {string} - 'green', 'yellow', ou 'red'
 */
export function classificarConformidade(xMedio, LSE, LIE, cp, cpk) {
  // REPROVADO (Red): Fora dos limites ou CPK < 1
  if (xMedio < LIE || xMedio > LSE || cpk < 1) {
    return 'red';
  }
  
  // ALERTA (Yellow): Dentro dos limites mas CPK entre 1 e 1.33
  if (cpk >= 1 && cpk < 1.33) {
    return 'yellow';
  }
  
  // APROVADO (Green): CPK >= 1.33
  return 'green';
}

/**
 * Processa todos os pontos do DataFrame
 * @param {Array} dataframe - DataFrame completo vindo do Streamlit
 * @returns {Object} - Objeto com dados processados por ponto
 */
export function processarTodosPontos(dataframe) {
  if (!dataframe || dataframe.length === 0) {
    return {};
  }

  const pontosPorEixo = {};

  // Agrupa medições por NomePonto + Eixo
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

  // Calcula estatísticas para cada ponto
  const resultado = {};
  
  Object.keys(pontosPorEixo).forEach(chave => {
    const ponto = pontosPorEixo[chave];
    const stats = calcularEstatisticasPonto(ponto.medicoes);
    
    resultado[chave] = {
      ...ponto,
      stats: stats,
      seq: chave.split(' - ')[0],  // Pode ser um número sequencial depois
      label: ponto.nomePonto,
      axis: ponto.eixo
    };
  });

  return resultado;
}

/**
 * Filtra pontos por conformidade
 * @param {Object} pontosProcessados - Objeto com pontos processados
 * @param {string} filtro - 'all', 'red', 'yellow', 'green'
 * @returns {Array} - Array de chaves dos pontos filtrados
 */
export function filtrarPorConformidade(pontosProcessados, filtro) {
  if (filtro === 'all') {
    return Object.keys(pontosProcessados);
  }

  return Object.keys(pontosProcessados).filter(chave => {
    const ponto = pontosProcessados[chave];
    return ponto.stats && ponto.stats.conformidade === filtro;
  });
}

/**
 * Filtra pontos por CPK
 * @param {Object} pontosProcessados - Objeto com pontos processados
 * @param {string} filtro - 'all', 'approved' (>=1.33), 'alert' (1-1.33), 'rejected' (<1)
 * @returns {Array} - Array de chaves dos pontos filtrados
 */
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

/**
 * Gera dados para preencher a linha da tabela
 * @param {Object} pontoProcessado - Dados de um ponto processado
 * @param {number} seq - Número sequencial
 * @returns {Object} - Dados formatados para a tabela
 */
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
    actionPlan: '',  // Será preenchido pelo usuário
    responsible: '',  // Será preenchido pelo usuário
    data: '',  // Será preenchido pelo usuário
    status: '',  // Será preenchido pelo usuário
    semanas: {}  // Será preenchido com X, NOK, R
  };
}