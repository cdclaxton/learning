import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps,
  StreamlitComponentBase,
} from "streamlit-component-lib"
import React from "react";
import logo from './cat.jpg'

function Button({text}: {text: string}): any {
    const [hover, setHover] = React.useState(false);

    let buttonStyle: React.CSSProperties = {
        backgroundColor: "rgb(25, 124, 159)",
        color: "white",
        border: "0px",
        borderRadius: "20px",
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: "14px",
        padding: "8px 20px",
        marginLeft: "5px",
        cursor: "pointer"
    }

    if (hover) {
        buttonStyle = {
            ...buttonStyle, 
            backgroundColor: "red"
        }
        console.log(buttonStyle)
    }

    return (
        <button style={buttonStyle} 
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}>{text}</button>
    )
}

function HeaderComponent({title}: {title: string}): any {
    const headerDivStyle: React.CSSProperties = {
        //position: "fixed",
        height: "70px",
        background: "rgb(106, 160, 133)",
        left: "0px",
        right: "0px",
        top: "0px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        paddingLeft: "20px",
        paddingRight: "20px"
    }

    const headerLeftStyle: React.CSSProperties = {
        display: "flex",
        flexDirection: "row",
        alignItems: "center"
    }

    const nameStyle: React.CSSProperties = {
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: "16px",
    }

    const logoStyle: React.CSSProperties = {
        width: "50px",
        height: "50px",
        borderRadius: "10px",
        objectFit: "cover",
        marginRight: "10px"
    }

    return(
        <div style={headerDivStyle}>
            <div style={headerLeftStyle}>
                <img style={logoStyle} src={logo} />
                <p style={nameStyle}>{title}</p>
            </div>
            <div>
                <Button text="Sign out" />
            </div>
        </div>
    )
}

class Header extends StreamlitComponentBase {
  public render = (): React.ReactNode => {
    const title = this.props.args['title']
    return(
        <HeaderComponent title={title}/>
    )
  }
}

export default withStreamlitConnection(Header)