import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import "./App.css";
import logo from "./assets/1.png"; // Import the logo

function App() {
  const [showMainPage, setShowMainPage] = useState(false);

  const handleStartClick = () => {
    setShowMainPage(true);
  };

  return (
    <div className="App">
      {!showMainPage ? (
        <div className="welcome-screen">
          <img src={logo} alt="Prescripto Logo" className="logo-large" />
          <h1><u>Prescripto</u></h1>
          <h4><i>Handwritten Prescription Recognition</i></h4>
          <button onClick={handleStartClick} className="start-button">
            Start
          </button>
        </div>
      ) : (
        <>
          <header className="App-header">
            <div className="logo-container">
              <img src={logo} alt="Prescripto Logo" className="logo" />
              <h1><u>Prescripto</u></h1>
            </div>
            <h4><i>Handwritten Prescription Recognition</i></h4>
          </header>
          <main>
            <FileUpload />
          </main>
        </>
      )}
    </div>
  );
}

export default App;
