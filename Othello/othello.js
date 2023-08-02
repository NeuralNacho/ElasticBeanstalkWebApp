const emptyCell = ''; // Empty cells are empty
const undoButton = document.getElementById('undo-button');
const resetButton = document.getElementById('reset-button');

let currentPlayer = 'black';
let board = createBoard(); // Could use class but this is simpler
let legalMoves = []; // Array of legal moves for current player
let turnsPassed = 0; // When this reaches 2 the game has ended
let gameHistory = [];
// Will be used as a stack containing arrays [board, playerTurn, turnsPassed]

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
    const boardCopy = JSON.parse(JSON.stringify(board))
    gameHistory.push([boardCopy, currentPlayer.slice(), turnsPassed])
    // slice() to create copy
    turnsPassed = 0
    board[index[0]][index[1]] = currentPlayer;
    flipTiles(index);  // Important this comes before changing player
    currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
    updateLegalMoves();
    renderBoard();
    renderScore();
    updateScoreBorders();
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
    if (legalMoves.length === 0) {
        turnsPassed += 1;
        if (turnsPassed === 2) {
            gameEnd();
        }
        else {
        currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
        updateLegalMoves();
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
                for (const tile of tilesToFlip) {
                    board[tile[0]][tile[1]] = currentPlayer;
                }
                break
            }
        }
    }
}

// Set up the undo button:
undoButton.addEventListener('click', () => {
    if (gameHistory.length != 0) {
        const gameState = gameHistory.pop()
        board = gameState[0];
        currentPlayer = gameState[1];
        turnsPassed = gameState[2];
        updateLegalMoves();
        renderBoard();
        renderScore();
        updateScoreBorders();
        const gameEndText = document.getElementById('game-end-text');
        gameEndText.textContent = ""; 
        // Clear this text so that you can undo from game end
    }
    });

// Set up the reset button:
resetButton.addEventListener('click', () => {
    gameHistory = [];
    board = createBoard();
    currentPlayer = 'black';
    turnsPassed = 0;
    updateLegalMoves();
    renderBoard();
    renderScore();
    updateScoreBorders();
    const gameEndText = document.getElementById('game-end-text');
    gameEndText.textContent = ""; 
    // Clear this text so that you can reset from game end
    });

function renderScore() {
    let noBlackTiles = 0;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'black') {
                noBlackTiles += 1;
            }
        }
    }
    const blackScoreDisc = document.getElementById('black-score-disc');
    blackScoreDisc.textContent = noBlackTiles.toString();

    let noWhiteTiles = 0;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'white') {
                noWhiteTiles += 1;
            }
        }
    }
    const whiteScoreDisc = document.getElementById('white-score-disc');
    whiteScoreDisc.textContent = noWhiteTiles.toString();
}

function updateScoreBorders() {
    // Used when player turn changes
    const blackScore = document.getElementById('black-score');
    const whiteScore = document.getElementById('white-score');
    if (currentPlayer === 'black') { // Change borders of players for player turn
        blackScore.style.borderWidth = '3px';
        whiteScore.style.borderWidth = '0px';
    }
    else {
        blackScore.style.borderWidth = '0px';
        whiteScore.style.borderWidth = '3px';
    }
}

function gameEnd() {
    // Use this when both players have no legal moves. 
    // Will display game over text and victor
    let noBlackTiles = 0;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'black') {
                noBlackTiles += 1;
            }
        }
    }
    let noWhiteTiles = 0;
    let result;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'white') {
                noWhiteTiles += 1;
            }
        }
    }
    if (noBlackTiles > noWhiteTiles) {
        result = " Black Wins ";
        score = noBlackTiles.toString() + " - " + noWhiteTiles.toString()
    }
    else if (noBlackTiles < noWhiteTiles) {
        result = " White Wins ";
        score = noWhiteTiles.toString() + " - " + noBlackTiles.toString()
    }
    else {
        result = " Draw "
        score = noBlackTiles.toString() + " - " + noWhiteTiles.toString()
    }

    const gameEndText = document.getElementById('game-end-text');
    gameEndText.textContent = "Game Over:" + result + score; 
}

function sendBoardStateToPython(boardState) {
    const url = '/get_random_move';
    const data = { board_state: boardState };
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => handleRandomMove(data.random_move))
    .catch(error => console.error('Error:', error));
}

function handleRandomMove(randomMove) {
    // Use the randomMove received from Python in your game logic
    // For example: make a move on the board using the randomMove
    console.log(randomMove);
}

sendBoardStateToPython(board);


// Initialise the game:
updateLegalMoves();
renderBoard();
renderScore();