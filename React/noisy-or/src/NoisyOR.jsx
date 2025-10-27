import { formatProbability } from './utilities';
import ShowMath from './ShowMath';

const NoisyOR = ({pEngineFails, pBatteryFails}) => {

    const pNeitherFails = (1-pEngineFails)*(1-pBatteryFails);

    return (
        <>
            <p className="my-2">The probability that the engine doesn't fail is</p>
            <ShowMath content={`1 - p_{e} = 1 - ${pEngineFails} = ${formatProbability(1-pEngineFails)}`}/>

            <p className="my-2">The probability that the battery doesn't fail is</p>
            <ShowMath content={`1 - p_{b} = 1 - ${pBatteryFails} = ${formatProbability(1-pBatteryFails)}`} />

            <p className="my-2">The probability that the engine AND the battery don't fail is</p>
            <ShowMath content={`(1 - p_{e})(1 - p_{b}) = (${formatProbability(1-pEngineFails)})(${formatProbability(1-pBatteryFails)}) = ${formatProbability(pNeitherFails)}`}/>

            <p className="my-2">Therefore, the probability that either the engine <strong>or</strong> the battery <strong>or</strong> both fail is</p>
            <ShowMath content={`1 - (1 - p_{e})(1 - p_{b}) = 1 - (${formatProbability(1-pEngineFails)})(${formatProbability(1-pBatteryFails)}) = ${formatProbability(1-pNeitherFails)}`} />
        </>
    )
}

export default NoisyOR;