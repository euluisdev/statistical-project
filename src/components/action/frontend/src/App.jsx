import React, { useEffect } from "react";
import { Streamlit } from "streamlit-component-lib";

function App() {
  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(900);
  }, []);

  const currentWeek = 47;
  const weeks = Array.from({ length: 10 }, (_, i) => i + 43);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', fontSize: '11px' }}>
      {/* Toolbar */}
      <div style={{
        display: 'flex',
        gap: '5px',
        marginBottom: '10px',
        alignItems: 'center',
        backgroundColor: '#f0f0f0',
        padding: '5px',
        border: '1px solid #ccc'
      }}>
        <select style={{ padding: '5px', border: '1px solid #999', backgroundColor: 'white', width: '100px' }}>
          <option>Year 2025</option>
          <option>Year 2024</option>
          <option>Year 2026</option>
        </select>
        <select style={{ padding: '5px', border: '1px solid #999', backgroundColor: 'white', width: '80px' }}>
          <option>Week</option>
        </select>
        <select style={{ padding: '5px', border: '1px solid #999', backgroundColor: 'white', width: '100px' }}>
          <option>45</option>
          <option>46</option>
          <option>47</option>
        </select>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>📖</button>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>🏆</button>
        <label style={{ display: 'flex', alignItems: 'center', gap: '3px' }}>
          <input type="checkbox" /> Point to point
        </label>
        <select style={{ padding: '5px', border: '1px solid #999', backgroundColor: 'white', width: '80px' }}>
          <option>CPK</option>
        </select>
        <select style={{ padding: '5px', border: '1px solid #999', backgroundColor: 'white', width: '80px' }}>
          <option>All</option>
        </select>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>🖨️</button>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>🔍</button>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>📊</button>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>⚠️ RISK</button>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>📋</button>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>🏠</button>
        <button style={{ padding: '5px 10px', border: '1px solid #999', backgroundColor: '#e0e0e0', cursor: 'pointer' }}>➕</button>
      </div>

      {/* Project Title */}
      <div style={{
        backgroundColor: '#e0e0e0',
        padding: '5px 10px',
        marginBottom: '5px',
        border: '1px solid #999',
        fontWeight: 'bold',
        fontSize: '13px'
      }}>
        534895200 - REAR RAIL RT
      </div>

      {/* Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontSize: '11px'
        }}>
          <thead>
            <tr>
              <th rowSpan={2} style={headerStyle}>SEQ</th>
              <th rowSpan={2} style={headerStyle}>LABEL</th>
              <th rowSpan={2} style={headerStyle}>AXIS</th>
              <th rowSpan={2} style={headerStyle}>LSE</th>
              <th rowSpan={2} style={headerStyle}>LIE</th>
              <th rowSpan={2} style={headerStyle}>SYMBOL</th>
              <th rowSpan={2} style={headerStyle}>X-MÉDIO</th>
              <th rowSpan={2} style={headerStyle}>CP</th>
              <th rowSpan={2} style={headerStyle}>CPK</th>
              <th rowSpan={2} style={headerStyle}>RANGE</th>
              <th rowSpan={2} style={headerStyle}>
                <div style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)', whiteSpace: 'nowrap' }}>
                  RISK - Desviation
                </div>
              </th>
              <th rowSpan={2} style={headerStyle}>
                <div style={{ writingMode: 'vertical-rl', transform: 'rotate(180deg)', whiteSpace: 'nowrap' }}>
                  RISK - Root Cause
                </div>
              </th>
              <th rowSpan={2} style={{ ...headerStyle, width: '150px' }}>ACTION PLAN</th>
              <th rowSpan={2} style={{ ...headerStyle, width: '120px' }}>RESPONSIBLE</th>
              <th rowSpan={2} style={{ ...headerStyle, width: '70px' }}>DATA</th>
              <th colSpan={10} style={{ ...headerStyle, backgroundColor: '#d3d3d3' }}>SEMANA</th>
              <th rowSpan={2} style={{ ...headerStyle, width: '80px' }}>STATUS</th>
            </tr>
            <tr>
              {weeks.map(week => (
                <th key={week} style={{
                  ...headerStyle,
                  width: '30px',
                  backgroundColor: week === currentWeek ? '#808080' : '#d3d3d3',
                  color: week === currentWeek ? 'white' : '#000'
                }}>
                  {week}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: 15 }).map((_, i) => (
              <tr key={i} style={{ height: '35px' }}>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                <td style={cellStyle}></td>
                {weeks.map(week => (
                  <td key={week} style={cellStyle}></td>
                ))}
                <td style={cellStyle}></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div style={{ marginTop: '10px', fontSize: '12px' }}>
        <strong>X</strong> - Ação programada; <strong>NOK</strong> - Ação não efetiva; <strong>R</strong> - Ação reprogramada
      </div>
    </div>
  );
}

const headerStyle = {
  backgroundColor: '#c0c0c0',
  border: '1px solid #000',
  padding: '8px 4px',
  textAlign: 'center',
  fontWeight: 'bold',
  color: '#000',
  verticalAlign: 'middle'
};

const cellStyle = {
  border: '1px solid #000',
  padding: '8px 4px',
  textAlign: 'center',
  backgroundColor: '#fff',
  verticalAlign: 'middle'
};

export default App;