import React, { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import Result from "./Result"

const rootElement = document.getElementById("root")

if (!rootElement) {
  throw new Error("Root element not found")
}

const root = createRoot(rootElement)

root.render(
  <StrictMode>
    <Result />
  </StrictMode>
)
