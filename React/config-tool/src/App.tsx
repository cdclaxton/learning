import React from 'react';
import './App.css';
import Phases from './components/Phases';
import Model from './lib/model';
import { create } from 'zustand';

// Create a model
const model = new Model();
model.addPhase("phase-1", "Phase 1");
model.addPhase("phase-2", "Phase 2");

interface ModelState {
  model: Model
}

export const useModelStore = create<ModelState>()((set) => ({
  model: model,
}));

export default function App() {
  return (
    <>
      <div className="title">
        <h1>Probabilistic model configuration</h1>
      </div>
      <Phases/>
    </>
  );
}
