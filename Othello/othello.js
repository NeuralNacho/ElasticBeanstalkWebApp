const boardSize = 8;
const emptyCell = '';

let currentPlayer = 'black';
let board = createBoard();
let legalMoves = [];

function createBoard() {
  const board = new Array(boardSize * boardSize).fill(emptyCell);
  board[27] = 'black';
  board[28] = 'white';
  board[35] = 'white';
  board[36] = 'black';
  return board;
}

function renderBoard() {
  const boardContainer = document.getElementById('board');
  boardContainer.innerHTML = '';

  for (let i = 0; i < boardSize * boardSize; i++) {
    const cell = document.createElement('div');
    cell.className = 'cell';

    if (board[i] === 'black') {
      const blackDisc = document.createElement('div');
      blackDisc.className = 'black-disc';
      cell.appendChild(blackDisc);

    } else if (board[i] === 'white') {
      const whiteDisc = document.createElement('div');
      whiteDisc.className = 'white-disc';
      cell.appendChild(whiteDisc);

    } else {
      cell.classList.add('empty');
      cell.addEventListener('click', () => handleMove(i));
    }

    // Highlight legal moves
    if (legalMoves.includes(i)) {
      cell.classList.add('legal-move');
    }

    boardContainer.appendChild(cell);
  }
}

function handleMove(index) {
  if (!legalMoves.includes(index)) {
    return; // Cell is not a legal move
  }

  board[index] = currentPlayer;
  flipTiles(index);
  currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
  updateLegalMoves();
  renderBoard();
}

function updateLegalMoves() {
  legalMoves = [];
  for (let i = 0; i < boardSize * boardSize; i++) {
    if (board[i] === emptyCell && isValidMove(i)) {
      legalMoves.push(i);
    }
  }
}

// Function to check if a move is valid
function isValidMove(index) {
    if (board[index] !== emptyCell) {
      return false; // Cell is not empty, so it's an invalid move
    }
  
    const directions = [
      [-1, -1], [-1, 0], [-1, 1],
      [0, -1],           [0, 1],
      [1, -1],  [1, 0],  [1, 1]
    ];
  
    let isValid = false;
  
    for (const [dx, dy] of directions) {
      let x = index % boardSize;
      let y = Math.floor(index / boardSize);
      let foundOpponentPiece = false;
  
      // Move in the direction and check if there is an opponent's piece
      x += dx;
      y += dy;
  
      while (x >= 0 && x < boardSize && y >= 0 && y < boardSize) {
        const currentIndex = y * boardSize + x;
  
        if (board[currentIndex] === emptyCell) {
          break; // Reached an empty cell, so it's not a valid move in this direction
        } else if (board[currentIndex] === currentPlayer) {
          if (foundOpponentPiece) {
            isValid = true; // Valid move if there's a player's piece after finding an opponent's piece
            break;
          } else {
            break; // No opponent's piece in this direction
          }
        } else {
          foundOpponentPiece = true; // Found an opponent's piece
        }
  
        x += dx;
        y += dy;
      }
    }
  
    return isValid;
  }

// Function to flip tiles based on the current move
function flipTiles(index) {
    const directions = [
      [-1, -1], [-1, 0], [-1, 1],
      [0, -1],           [0, 1],
      [1, -1],  [1, 0],  [1, 1]
    ];
  
    for (const [dx, dy] of directions) {
      let x = index % boardSize;
      let y = Math.floor(index / boardSize);
      let foundOpponentPiece = false;
      const tilesToFlip = [];
  
      // Move in the direction and collect opponent's pieces to flip
      x += dx;
      y += dy;
  
      while (x >= 0 && x < boardSize && y >= 0 && y < boardSize) {
        const currentIndex = y * boardSize + x;
  
        if (board[currentIndex] === emptyCell) {
          break; // Reached an empty cell, so no opponent's pieces to flip in this direction
        } else if (board[currentIndex] === currentPlayer) {
          if (foundOpponentPiece) {
            // Flip opponent's pieces between the current cell and the original move
            for (const tileIndex of tilesToFlip) {
              board[tileIndex] = currentPlayer;
            }
          }
          break;
        } else {
          foundOpponentPiece = true; // Found an opponent's piece
          tilesToFlip.push(currentIndex);
        }
  
        x += dx;
        y += dy;
      }
    }
  }
  

updateLegalMoves();
renderBoard();