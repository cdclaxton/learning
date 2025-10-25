import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import ComponentFails from './ComponentFails';
import NoisyOR from './NoisyOR';
import engineImage from './assets/engine.jpg';
import batteryImage from './assets/battery.jpg';

function App() {
  const [pEngineFails, setPEngineFails] = React.useState(0.6);
  const [pBatteryFails, setPBatteryFails] = React.useState(0.4);

  return (
    <div className="container my-3">
      <h1 className="display-1">Noisy OR</h1>  
      <p className="lead text-secondary">The Noisy OR function returns the probability that at least one of a number of independent events occurs.</p>
      <p>Suppose that a car can only be driven if the engine and the battery are both working.</p>

      <div className="row">
        <div className="col-sm border m-2 p-2 rounded">
          <ComponentFails id="engineFails" probability={pEngineFails} 
            setProbability={setPEngineFails} name="engine" letter="e"
            image={engineImage}></ComponentFails>
        </div>
        <div className="col-sm border m-2 p-2 rounded">
          <ComponentFails id="batteryFails" probability={pBatteryFails} 
            setProbability={setPBatteryFails} name="battery" letter="b"
            image={batteryImage}></ComponentFails>
        </div>
      </div>
      <NoisyOR pEngineFails={pEngineFails} pBatteryFails={pBatteryFails}/>
    </div>
  )
}

export default App
