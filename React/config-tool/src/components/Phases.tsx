import React from 'react';
import { useModelStore } from "../App"

function SinglePhase({id, name, updateId, updateName, deletePhase}: {
    id: string;
    name: string;
    updateId: (newId: string) => void;
    updateName: (newName: string) => void;
    deletePhase: () => void;
}) {
    return(
        <div key={`{id}-{name}`} className="single-phase-box">
            <div key={id} className="input-pair">
                <label htmlFor="phase-id">ID:</label>
                <input id="phase-id" type="text" placeholder="Phase ID" className="input-box" value={id} 
                    onChange={(event) => updateId(event.target.value)} />
            </div>
            <div key={name} className="input-pair">
                <label htmlFor="phase-name">Name:</label>
                <input id="phase-name" type="text" placeholder="Phase name" className="input-box" value={name} 
                    onChange={(event) => updateName(event.target.value)} />
            </div>
            <button className="delete-button" onClick={() => deletePhase()}>Delete</button>                   
        </div>        
    )
}

function Phases() {

    const model = useModelStore(store => store.model);

    return(
        <div className="main-section">
            <p className="section-title">Phases</p>
            <p className="help-text">A phase is a single step in a plan</p>  
            {model.phases.map((phase, index) => (
                <SinglePhase
                    key={phase.id + phase.name} 
                    id={phase.id} 
                    name={phase.name} 
                    updateId={(newId) => model.updatePhaseId(index, newId)}
                    updateName={(newName) => model.updatePhaseName(index, newName)} 
                    deletePhase={() => model.deletePhase(index)} />
            ))}
        </div>
    )
}

export default Phases;