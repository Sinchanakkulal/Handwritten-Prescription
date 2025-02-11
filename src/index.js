import React from 'react';
import ReactDOM from 'react-dom/client';  // Notice the different import
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));  // Create root
root.render(  // Use `render` on the root
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
