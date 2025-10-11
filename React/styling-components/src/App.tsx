import React from 'react';
import "./App.css";
import { DateTime } from 'luxon';
import { ResultData } from './model/model';
import Header from './components/header/Header';
import Information from './components/information/Information';
import Result from './components/result/Result';

function App() {
  const results: ResultData[] = [
    {
      id: 1,
      datasetName: "Cats residing in London in 2025",
      dateUploaded: DateTime.now(),
      numberOfRows: 3000,
      numberOfRowsWithErrors: 2,
      numberOfUniqueCats: 2657,
      
    },
    {
      id: 2,
      datasetName: "Ally cat arrests 2016",
      dateUploaded: DateTime.now().minus({days: 2}),
      numberOfRows: 250,
      numberOfRowsWithErrors: 10,
      numberOfUniqueCats: 134,
    },    
  ];
  console.log(results.map((r) => (r.datasetName)))

  return (
    <>
      <Header title="Cat Data Processing Engine" />
      <Information 
        title="Introduction"
        text="The Cat Data Processing Engine performs data extraction and standardisation for cat-based datasets." 
      />

      {results.map((r) => (
        <Result result={r} />
      ))}
    </>
  );
}

export default App;
