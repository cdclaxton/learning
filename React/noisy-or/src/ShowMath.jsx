import { MathJax } from 'better-react-mathjax';

const ShowMath = ({content}) => {
    return <MathJax className="formula" inline dynamic>
        {"\\(" + content + "\\)"}
    </MathJax>
}
export default ShowMath;