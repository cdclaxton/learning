import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps,
  StreamlitComponentBase,
} from "streamlit-component-lib"
import React from "react";
import Slider from '@mui/material/Slider';
import { styled } from '@mui/material/styles';

const options = ["low", "medium", "higher", "high"];
const createMarks = (labels: string[]): any[] => {
  return labels.map((label, index) => {
    return {
      value: index,
      label: label,
    }
  })
}


class DiscreteSlider extends StreamlitComponentBase {
  public render = (): React.ReactNode => {
    const vMargin = 7;
    const hMargin = 40;

    const StyledSlider = styled(Slider)({
      margin: `${vMargin}px ${hMargin}px`,
      width: this.props.width - (hMargin * 2),
    })

    const options = this.props.args["options"]

    return(
      <StyledSlider
        aria-label="Custom marks"
        defaultValue={0}
        min={0}
        max={options.length - 1}
        step={null}
        valueLabelDisplay="off"
        marks={createMarks(options)}
        onChangeCommitted={(event,value) => {
          const selectedOption = options[Number(value)]
          Streamlit.setComponentValue(selectedOption)
        }}
        disabled={this.props.disabled}
      />
    )
  }
}

// /**
//  * A template for creating Streamlit components with React
//  *
//  * This component demonstrates the essential structure and patterns for
//  * creating interactive Streamlit components, including:
//  * - Accessing props and args sent from Python
//  * - Managing component state with React hooks
//  * - Communicating back to Streamlit via Streamlit.setComponentValue()
//  * - Using the Streamlit theme for styling
//  * - Setting frame height for proper rendering
//  *
//  * @param {ComponentProps} props - The props object passed from Streamlit
//  * @param {Object} props.args - Custom arguments passed from the Python side
//  * @param {string} props.args.name - Example argument showing how to access Python-defined values
//  * @param {boolean} props.disabled - Whether the component is in a disabled state
//  * @param {Object} props.theme - Streamlit theme object for consistent styling
//  * @returns {ReactElement} The rendered component
//  */
// function DiscreteSlider({ args, disabled, theme }: ComponentProps): React.ReactElement {
//   // Extract custom arguments passed from Python
//   const { name, greeting } = args

//   // Component state
//   const [isFocused, setIsFocused] = React.useState(false)
//   const [numClicks, setNumClicks] = React.useState(0)

//   /**
//    * Dynamic styling based on Streamlit theme and component state
//    * This demonstrates how to use the Streamlit theme for consistent styling
//    */
//   const style: React.CSSProperties = React.useMemo(() => {
//     if (!theme) return {}

//     // Use the theme object to style the button border
//     // Access theme properties like primaryColor, backgroundColor, etc.
//     const borderStyling = `1px solid ${isFocused ? theme.primaryColor : "gray"}`
//     return { border: borderStyling, outline: borderStyling }
//   }, [theme, isFocused])

//   /**
//    * Tell Streamlit the height of this component
//    * This ensures the component fits properly in the Streamlit app
//    */
//   React.useEffect(() => {
//     // Call this when the component's size might change
//     Streamlit.setFrameHeight()
//     // Adding the style and theme as dependencies since they might
//     // affect the visual size of the component.
//   }, [style, theme])

//   /**
//    * Click handler for the button
//    * Demonstrates how to update component state and send data back to Streamlit
//    */
//   const onClicked = React.useCallback((): void => {
//     const newNumClicks = numClicks + 1
//     // Update local state
//     setNumClicks(newNumClicks)
//     // Send value back to Streamlit (will be available in Python)
//     Streamlit.setComponentValue({clicks: newNumClicks})
//   }, [numClicks])

//   /**
//    * Focus handler for the button
//    * Updates visual state when the button receives focus
//    */
//   const onFocus = React.useCallback((): void => {
//     setIsFocused(true)
//   }, [])

//   /**
//    * Blur handler for the button
//    * Updates visual state when the button loses focus
//    */
//   const onBlur = React.useCallback((): void => {
//     setIsFocused(false)
//   }, [])

//   return (
//     <span>
//       {greeting}, {name}! &nbsp;
//       <button
//         style={style}
//         onClick={onClicked}
//         disabled={disabled}
//         onFocus={onFocus}
//         onBlur={onBlur}
//       >
//         Click Me!
//       </button>
//     </span>
//   )
// }

/**
 * withStreamlitConnection is a higher-order component (HOC) that:
 * 1. Establishes communication between this component and Streamlit
 * 2. Passes Streamlit's theme settings to your component
 * 3. Handles passing arguments from Python to your component
 * 4. Handles component re-renders when Python args change
 *
 * You don't need to modify this wrapper unless you need custom connection behavior.
 */
export default withStreamlitConnection(DiscreteSlider)
