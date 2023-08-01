const emptyCell = ''; // Empty cells are empty

let currentPlayer = 'black';
let board = createBoard(); // Could use class but this is simpler
let legalMoves = []; // Array of legal moves for current player

function createBoard() {
    // 8x8 array with starting position
    const board = [];
    for (let i = 0; i < 8; i++) {
        board[i] = new Array(8).fill(emptyCell);
    }
    board[3][3] = 'white';
    board[3][4] = 'black';
    board[4][3] = 'black';
    board[4][4] = 'white';
    return board;
}

function renderBoard() {
    // For every square on the board display appropriate cell
    const boardContainer = document.getElementById('board');
    boardContainer.innerHTML = '';
    // Above line clears the board each time renderBoard is called

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            if (board[row][col] == 'black') {
                const blackDisc = document.createElement('div');
                blackDisc.className = 'black-disc';
                cell.appendChild(blackDisc);
            }
            else if (board[row][col] == 'white') {
                const whiteDisc = document.createElement('div');
                whiteDisc.className = 'white-disc';
                cell.appendChild(whiteDisc);
            }
            else {
                cell.addEventListener('click', () => handleMove([row, col]))
                // Need arrow function for a closure
                if (legalMoves.some(move => {
                    return move[0] == row && move[1] == col})) {  // some() method
                    cell.classList.add('highlighted');
                }
            }

            boardContainer.appendChild(cell);
            // Cells added to .board grid row by row
        }
    }
}

function handleMove(index) {
    // Called in arrow function on empty cell event listener
    // If legal move update everything
    if (!legalMoves.some(move => {
        return move[0] == index[0] && move[1] == index[1]})) {
        return;
    }
    board[index[0]][index[1]] = currentPlayer;
    flipTiles(index);  // Important this comes before changing player
    currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
    updateLegalMoves();
    renderBoard();
}

function isValidMove(index) {
    if (board[index[0]][index[1]] != emptyCell) {
        return false;
    }
    const directions = [[-1, -1], [-1, 0], [-1, 1],
                        [0, -1],           [0, 1],
                        [1, -1],  [1, 0],  [1, 1] ];
    for (const direction of directions) {
        let row = index[0] + direction[0];
        let col = index[1] + direction[1];
        let foundOpponentPiece = false;
        while (row >= 0 && row < 8 && col >= 0 && col < 8) {
            if (board[row][col] == emptyCell) {
                break;
            }
            if (board[row][col] != currentPlayer) {
                foundOpponentPiece = true;
                row += direction[0];
                col += direction[1];
                continue;
            }
            if (foundOpponentPiece) { // Have  met a disc of currentPlayer
                return true;
            }
            else {
                break; // If we've not found an oppenent piece
                // we should still keep checking other directions
            }
        }
    }
    return false; // If none of the directions work then get false
}

function updateLegalMoves() {
    // Called by handleMoves
    legalMoves = [];
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] == emptyCell && isValidMove([row, col])) {
                legalMoves.push([row, col]);
            }
        }
    }
}

function flipTiles(index) {
    // Called by handleMoves
    const directions = [[-1, -1], [-1, 0], [-1, 1],
                        [0, -1],           [0, 1],
                        [1, -1],  [1, 0],  [1, 1] ];
    for (const direction of directions) {
        const tilesToFlip = [];
        let row = index[0] + direction[0];
        let col = index[1] + direction[1];
        while (row >= 0 && row < 8 && col >= 0 && col < 8) {
            if (board[row][col] == emptyCell) {
                break;
            }
            if (board[row][col] != currentPlayer) {
                tilesToFlip.push([row, col]);
                row += direction[0];
                col += direction[1];
                continue;
            }
            if (board[row][col] == currentPlayer) {
                console.log(tilesToFlip)
                for (index of tilesToFlip) {
                    console.log(index)
                    board[index[0]][index[1]] = currentPlayer;
                }
                break
            }
        }
    }
}

// Initialise the game:
updateLegalMoves();
renderBoard();