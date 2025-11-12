import React, { useEffect, useState } from "react";
import { Streamlit } from "streamlit-component-lib";

function App() {
  const [selectedYear, setSelectedYear] = useState(2025);
  const [selectedWeek, setSelectedWeek] = useState(1);

  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(900);
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

  return (
    <div style={{ fontFamily: "Arial, sans-serif", fontSize: "11px" }}>
      {/*toolbar */}
      <div
        style={{
          display: "flex",
          gap: "5px",
          marginBottom: "10px",
          alignItems: "center",
          backgroundColor: "#f0f0f0",
          padding: "5px",
          border: "1px solid #ccc",
        }}
      >
        <select
          value={selectedYear}
          onChange={handleYearChange}
          style={{
            padding: "5px",
            border: "1px solid #999",
            backgroundColor: "white",
            width: "100px",
          }}
        >
          <option value={2024}>Year 2024</option>
          <option value={2025}>Year 2025</option>
          <option value={2026}>Year 2026</option>
        </select>

        <select
          value={selectedWeek}
          onChange={handleWeekChange}
          style={{
            padding: "5px",
            border: "1px solid #999",
            backgroundColor: "white",
            width: "100px",
          }}
        >
          {Array.from({ length: 52 }, (_, i) => i + 1).map((week) => (
            <option key={week} value={week}>
              {week}
            </option>
          ))}
        </select>

        <button style={btnStyle}>📖</button>
        <button style={btnStyle}>🏆</button>
        <label style={{ display: "flex", alignItems: "center", gap: "3px" }}>
          <input type="checkbox" /> Point to point
        </label>
        <select style={selectStyle}>
          <option>CPK</option>
        </select>
        <select style={selectStyle}>
          <option>All</option>
        </select>
        <button style={btnStyle}>🖨️</button>
        <button style={btnStyle}>🔍</button>
        <button style={btnStyle}>📊</button>
        <button style={btnStyle}>⚠️ RISK</button>
        <button style={btnStyle}>📋</button>
        <button style={btnStyle}>🏠</button>
        <button style={btnStyle}>➕</button>
      </div>

      {/*title */}
      <div
        style={{
          backgroundColor: "#e0e0e0",
          padding: "5px 10px",
          marginBottom: "5px",
          border: "1px solid #999",
          fontWeight: "bold",
          fontSize: "13px",
        }}
      >
        534895200 - REAR RAIL RT
      </div>

      {/*table */}
      <div style={{ overflowX: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            fontSize: "11px",
          }}
        >
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
              <th rowSpan={2} style={headerStyle}>RISK - Desviation</th>
              <th rowSpan={2} style={headerStyle}>RISK - Root Cause</th>
              <th rowSpan={2} style={{ ...headerStyle, width: "150px" }}>ACTION PLAN</th>
              <th rowSpan={2} style={{ ...headerStyle, width: "120px" }}>RESPONSIBLE</th>
              <th rowSpan={2} style={{ ...headerStyle, width: "70px" }}>DATA</th>
              <th colSpan={10} style={{ ...headerStyle, backgroundColor: "#d3d3d3" }}>SEMANA</th>
              <th rowSpan={2} style={{ ...headerStyle, width: "80px" }}>STATUS</th>
            </tr>
            <tr>
              {weeks.map((week) => (
                <th
                  key={week}
                  style={{
                    ...headerStyle,
                    width: "30px",
                    backgroundColor: week === selectedWeek ? "#808080" : "#d3d3d3",
                    color: week === selectedWeek ? "white" : "#000",
                    fontWeight: "bold",
                  }}
                >
                  {week}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: 15 }).map((_, i) => (
              <tr key={i} style={{ height: "35px" }}>
                {Array.from({ length: 15 + weeks.length + 1 }).map((_, j) => (
                  <td key={j} style={cellStyle}></td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/*legend*/}
      <div style={{ marginTop: "10px", fontSize: "12px" }}>
        <strong>X</strong> - Ação programada; <strong>NOK</strong> - Ação não efetiva;{" "}
        <strong>R</strong> - Ação reprogramada
      </div>
    </div>
  );
}

const btnStyle = {
  padding: "5px 10px",
  border: "1px solid #999",
  backgroundColor: "#e0e0e0",
  cursor: "pointer",
};

const selectStyle = {
  padding: "5px",
  border: "1px solid #999",
  backgroundColor: "white",
  width: "80px",
};

const headerStyle = {
  backgroundColor: "#c0c0c0",
  border: "1px solid #000",
  padding: "8px 4px",
  textAlign: "center",
  fontWeight: "bold",
  color: "#000",
  verticalAlign: "middle",
};

const cellStyle = {
  border: "1px solid #000",
  padding: "8px 4px",
  textAlign: "center",
  backgroundColor: "#fff",
  verticalAlign: "middle",
};

export default App;
