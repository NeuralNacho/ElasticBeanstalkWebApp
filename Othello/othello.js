const boardSize = 8;
const player1 = '⚫'; // Black
const player2 = '⚪'; // White
const emptyCell = '';

let currentPlayer = player1;
let board = createBoard();
let legalMoves = [];

function createBoard() {
  const board = new Array(boardSize * boardSize).fill(emptyCell);
  board[27] = player1;
  board[28] = player2;
  board[35] = player2;
  board[36] = player1;
  return board;
}

function renderBoard() {
  const boardContainer = document.getElementById('board');
  boardContainer.innerHTML = '';

  for (let i = 0; i < boardSize * boardSize; i++) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.innerText = board[i];

    if (board[i] === player1) {
      cell.classList.add('black');
    } else if (board[i] === player2) {
      cell.classList.add('white');
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
  currentPlayer = currentPlayer === player1 ? player2 : player1;
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