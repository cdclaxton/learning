import { MathJax } from 'better-react-mathjax';
import { formatProbability } from './utilities';

const NoisyOR = ({pEngineFails, pBatteryFails}) => {

    const pNeitherFails = (1-pEngineFails)*(1-pBatteryFails);

    return (
        <>
            <p className="my-2">The probability that the engine doesn't fail is</p>
            <MathJax>{"\\(1 - p_{e} = 1 - " + pEngineFails + " = " + formatProbability(1-pEngineFails) + "\\)"}</MathJax>
            <p className="my-2">The probability that the battery doesn't fail is</p>
            <MathJax>{"\\(1 - p_{b} = 1 - " + pBatteryFails + " = " + formatProbability(1-pBatteryFails) + "\\)"}</MathJax>
            <p className="my-2">The probability that the engine AND the battery don't fail is</p>
            <MathJax>{"\\((1 - p_{e})(1 - p_{b}) = (" + formatProbability(1-pEngineFails) + ")(" + formatProbability(1-pBatteryFails) + ") = " + formatProbability(pNeitherFails) + "\\)"}</MathJax>
            <p className="my-2">Therefore, the probability that either the engine <strong>or</strong> the battery <strong>or</strong> both fail is</p>
            <MathJax>{"\\(1 - (1 - p_{e})(1 - p_{b}) = 1 - (" + formatProbability(1-pEngineFails) + ")(" + formatProbability(1-pBatteryFails) + ") = " + formatProbability(1-pNeitherFails) + "\\)"}</MathJax>
        </>
    )
}

export default NoisyOR;