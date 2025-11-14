import React from "react";
import ReactDOM from "react-dom/client";
import { Streamlit } from "streamlit-component-lib";
import App from "./App";

class StreamlitComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { args: {} };
  }

  componentDidMount() {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(900);
    
    window.addEventListener("message", this.onMessage);
  }

  componentWillUnmount() {
    window.removeEventListener("message", this.onMessage);
  }

  onMessage = (event) => {
    const data = event.data;
    if (data.type === "streamlit:render") {
      console.log('Mensagem recebida:', data);
      this.setState({ args: data.args || {} });
    }
  };

  render() {
    return <App args={this.state.args} />;
  }
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <StreamlitComponent />
  </React.StrictMode>
);