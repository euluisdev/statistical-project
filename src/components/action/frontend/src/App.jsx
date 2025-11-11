import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Streamlit, StreamlitComponentBase } from "streamlit-component-lib";
import React, { useEffect } from "react";

function ActionComponent() {
  useEffect(() => {
    Streamlit.setComponentValue("✅ React carregado com sucesso!");
  }, []);

  return (
    <div style={{ padding: 30, textAlign: "center" }}>
      <h2>Componente React integrado ao Streamlit</h2>
      <p>Clique em algo ou interaja — posso mandar dados pro Python!</p>
    </div>
  );
}

export default ActionComponent;