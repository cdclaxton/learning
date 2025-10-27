import { formatProbability  } from './utilities';
import ShowMath from './ShowMath';

const ComponentFails = ({id, probability, setProbability, name, letter, image}) => {
    const updateProbability = (event) => {
        const value = event.target.value;
        setProbability(formatProbability(value));
    }

    const equation = `p_{${letter}} = ${probability}`; 

    return (
        <>
        <img src={image} className="img-fluid rounded" style={{opacity: 1-probability}}/>
        <label htmlFor={id} className="form-label">Probability the {name} fails:</label>
        <input type="range" className="form-range" min="0" max="1" step="0.01" 
            id={id} onChange={updateProbability} value={probability}/>
        <p><ShowMath content={equation}/></p>
        </>
    )
}

export default ComponentFails;