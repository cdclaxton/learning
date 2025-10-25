import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import { MathJaxContext } from 'better-react-mathjax'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <MathJaxContext>
      <App />
    </MathJaxContext>
  </StrictMode>,
)
