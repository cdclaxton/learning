import React from 'react';
import { DateTime } from 'luxon';
import { createUseStyles } from 'react-jss';
import {
  Streamlit,
  withStreamlitConnection,
  ComponentProps,
  StreamlitComponentBase,
} from "streamlit-component-lib"

type ResultData = {
    id: number;
    datasetName: string;
    dateUploaded: string;
    numberOfRows: number;
    numberOfRowsWithErrors: number;
    numberOfUniqueCats: number;
}

const resultStyle = createUseStyles({
    box: {
        backgroundColor: "rgb(200, 209, 210)",
        display: "flex",
        margin: "5px 0px",
        borderRadius: "5px",
        paddingBottom: "10px",
    },
    idDiv: {
        color: "white",
        fontWeight: "600",
        fontFamily: "Arial, Helvetica, sans-serif",
        backgroundColor: "rgb(23, 25, 51)",
        boxShadow: "2px 2px 3px 0px rgb(0,0,0,0.2)",
        width: "30px",
        height: "30px",
        lineHeight: "30px",
        borderRadius: "15px",
        textAlign: "center",
        margin: "10px",
    },
    mainBody: {
        flex: "1",
    },
    datasetTitle: {
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: "16px",
        fontWeight: "600",
        padding: "0px",
        margin: "0px",
    },
    uploadDate: {
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: "14px",
        fontWeight: "500",        
        color: "gray",
    },
    resultsSummary: {
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: "14px",
        fontWeight: "500",        
        color: "black",
    },
    downloadButton: {
        backgroundColor: "rgb(25, 124, 159)",
        color: "white",
        border: "0px",
        borderRadius: "20px",
        fontFamily: "Arial, Helvetica, sans-serif",
        fontSize: "14px",
        padding: "8px 20px",
        marginLeft: "5px",
        cursor: "pointer",
        '&:hover': {
            backgroundColor: "red",
        }
    }
});

const roundToTwoDecimals = (value: number): number => {
    return(Math.round(value * 100) / 100);
}

const BuildResult = ({result}: {result: ResultData}) => {
    const styleClasses = resultStyle();
    
    // Parse the upload date
    const dateUploaded = DateTime.fromISO(result.dateUploaded)

    // Calculate the number of days ago that the data was uploaded
    const numberOfDaysAgo = Math.floor(DateTime.now().diff(
        dateUploaded, 'days').days);

    // Calculate the percentage of rows with errors
    const percentageErrors = roundToTwoDecimals(100 * result.numberOfRowsWithErrors / result.numberOfRows);

    return(
        <div className={styleClasses.box}>
            <div className={styleClasses.idDiv}>
                {result.id}
            </div>
            <div className={styleClasses.mainBody}>
                <div className={styleClasses.datasetTitle}>
                    <p>{result.datasetName}</p>
                </div>
                <div className={styleClasses.uploadDate}>
                    <p>Uploaded on {dateUploaded.toLocaleString()} {
                        numberOfDaysAgo > 0 ? "(" + numberOfDaysAgo + " days ago)" : ""
                    }</p>
                </div>
                <div className={styleClasses.resultsSummary}>
                    <p>{result.numberOfRows} rows with {result.numberOfRowsWithErrors} {result.numberOfRowsWithErrors == 1 ? "error" : "errors"} ({percentageErrors} %)</p>
                    <p>{result.numberOfUniqueCats} unique felines</p>
                </div>
                <button className={styleClasses.downloadButton}>Download</button>
            </div>
        </div>
    )
}

class Result extends StreamlitComponentBase {
  public render = (): React.ReactNode => {
    const result: ResultData = this.props.args["result_data"];
    return(
        <BuildResult result={result}/>
    )

    // const result: ResultData = this.props.args["result_data"];
    // const styleClasses = resultStyle;
    // console.log(result)

    // // Calculate the number of days ago that the data was uploaded
    // const numberOfDaysAgo = 0 //Math.floor(DateTime.now().diff(
    //     //result.dateUploaded, 'days').days);

    // // Calculate the percentage of rows with errors
    // const percentageErrors = roundToTwoDecimals(100 * result.numberOfRowsWithErrors / result.numberOfRows);

    // return(
    //     <div className={styleClasses.box}>
    //         <div className={styleClasses.idDiv}>
    //             {result.id}
    //         </div>
    //         <div className={styleClasses.mainBody}>
    //             <div className={styleClasses.datasetTitle}>
    //                 <p>{result.datasetName}</p>
    //             </div>
    //             <div className={styleClasses.uploadDate}>
    //                 <p>Uploaded on {result.dateUploaded.toLocaleString()} {
    //                     numberOfDaysAgo > 0 ? "(" + numberOfDaysAgo + " days ago)" : ""
    //                 }</p>
    //             </div>
    //             <div className={styleClasses.resultsSummary}>
    //                 <p>{result.numberOfRows} rows with {result.numberOfRowsWithErrors} errors ({percentageErrors} %)</p>
    //                 <p>{result.numberOfUniqueCats} unique felines</p>
    //             </div>
    //             <button className={styleClasses.downloadButton}>Download</button>
    //         </div>
    //     </div>
    // )
  }
}

export default withStreamlitConnection(Result);