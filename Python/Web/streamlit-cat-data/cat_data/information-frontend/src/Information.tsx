import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps,
  StreamlitComponentBase,
} from "streamlit-component-lib"
import React from 'react';
import "./Information.css";

// This component uses CSS from a single CSS file

class Information extends StreamlitComponentBase {
  public render = (): React.ReactNode => {

    const title = this.props.args["title"];
    const text = this.props.args["text"];

    return(
        <div className={"information"}>
            <p className="title">
                <span className="information-icon">ⓘ</span> {title}</p>
            <p className="body-text">{text}</p>
        </div>
    )
  }
}

export default withStreamlitConnection(Information)