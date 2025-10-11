import React from 'react';
import "./Information.css";

// This component uses CSS from a single CSS file

export default function Information({text, title}: 
    {text: string;
        title: string;
    }): any {

    return(
        <div className={"information"}>
            <p className="title">
                <span className="information-icon">ⓘ</span> {title}</p>
            <p className="body-text">{text}</p>
        </div>
    )
}