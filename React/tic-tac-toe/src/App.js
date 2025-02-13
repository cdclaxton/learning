import { useState } from 'react';

// Square on the board.
// value -- index of the square.
// onSquareClick -- callback if the square is clicked.
// isHighlighted -- boolean to determine if the square should be highlighted.
function Square({value, onSquareClick, isHighlighted}) {
  const squareClass = isHighlighted ? "square square-highlighted" : "square";

  return (
    <button className={squareClass} onClick={onSquareClick}>
      {value}
    </button>
  );
}

// Board on which to play.
// xIsNext -- player X is next.
// squares -- array of 9 elements with values representing the current state.
// onPlay -- callback for returning the modified squares.
function Board({xIsNext, squares, onPlay}) {

  function handleClick(i) {
    // Check the square hasn't already been populated or that there isn't
    // a winner
    if (calculateWinner(squares).isWinner || squares[i]) {
      return;
    }

    const nextSquares = squares.slice();
    if (xIsNext) {
      nextSquares[i] = "X";
    } else {
      nextSquares[i] = "O";
    }

    onPlay(nextSquares);
  }
  
  const winner = calculateWinner(squares);
  let status;
  if (winner.isWinner) {
    status = "Winner: " + winner.winner;
  } else {
    status = "Next player: " + (xIsNext ? "X" : "O");
  }

  // Make the board
  let board = [];
  for (let row=0; row<3; row++) {
    
    let rowOfElements = [];
    for (let column=0; column<3; column++) {
      const j = (row * 3) + column;
      const square = <Square value={squares[j]} onSquareClick={() => handleClick(j)} isHighlighted={winner.isWinner && winner.squares.has(j)}/>
      rowOfElements.push(square);
    }

    board.push(<div className="board-row">{rowOfElements}</div>)
  }
  
  return (
    <>
    <div className="status">{status}</div>
    {board}
    </>
  )
}

// export -- makes it accessible outisde of the file
// default -- main function in the file
export default function Game() {
  
  const [history, setHistory] = useState([Array(9).fill(null)]);
  const [currentMove, setCurrentMove] = useState(0);

  const xIsNext = currentMove % 2 === 0;
  const currentSquares = history[currentMove];

  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);
  }

  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }

  const moves = history.map((squares, move) => {
    let description;
    if (move > 0) {
      description = "Go to move #" + move;
    } else {
      description = "Go to game start";
    }

    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    )
  })

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info">
        <ol>{moves}</ol>
      </div>
    </div>
  )
}

function calculateWinner(squares) {
  const lines = [
    // Horizontal
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    // Vertical
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],
    // Diagonal
    [0, 4, 8],
    [2, 4, 6],
  ]

  for (let i=0; i<lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[b] === squares[c]) {
      return {
        isWinner: true,
        winner: squares[a],
        squares: new Set(lines[i]),
      }
    }
  }

  return {
    isWinner: false,
  };
}