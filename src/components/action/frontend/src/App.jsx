import React, { useEffect } from "react";
import { Streamlit } from "streamlit-component-lib";

function App() {
  useEffect(() => {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(200);
    Streamlit.setComponentValue("✅ React carregado com sucesso!");
  }, []);

  return (
    <div style={{ 
      padding: '30px', 
      textAlign: 'center', 
      background: '#f0f0f0',
      borderRadius: '8px'
    }}>
      <h2>Meu componente no streamlit</h2>
      <p>Interaja aqui</p>
    </div>
  );
}

export default App;