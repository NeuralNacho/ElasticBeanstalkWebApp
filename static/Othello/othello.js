const emptyCell = ''; // Empty cells are empty
const undoButton = document.getElementById('undo-button');
const resetButton = document.getElementById('reset-button');
const rulesHeader = document.getElementById('rules-header');
const rulesContent = document.getElementById('rules-content');

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
                    return move[0] == row && move[1] == col})) {
                    cell.classList.add('highlighted')
                    const highlightedCell = document.createElement('div');
                    highlightedCell.className = 'highlighted';
                    cell.appendChild(highlightedCell)
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
    flipDiscs(index);  // Important this comes before changing player
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

function flipDiscs(index) {
    // Called by handleMoves
    const directions = [[-1, -1], [-1, 0], [-1, 1],
                        [0, -1],           [0, 1],
                        [1, -1],  [1, 0],  [1, 1] ];
    for (const direction of directions) {
        const discsToFlip = [];
        let row = index[0] + direction[0];
        let col = index[1] + direction[1];
        while (row >= 0 && row < 8 && col >= 0 && col < 8) {
            if (board[row][col] == emptyCell) {
                break;
            }
            if (board[row][col] != currentPlayer) {
                discsToFlip.push([row, col]);
                row += direction[0];
                col += direction[1];
                continue;
            }
            if (board[row][col] == currentPlayer) {
                for (const disc of discsToFlip) {
                    board[disc[0]][disc[1]] = currentPlayer;
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
        gameEndText.style.display = "none";
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
    gameEndText.style.display = "none";
    // Clear this text so that you can reset from game end
    });

// Set up rules drop down button: 
rulesHeader.addEventListener('click', () => {
    rulesContent.style.display = rulesContent.style.display === 'none' || rulesContent.style.display === '' ? 'block' : 'none';
    rulesHeader.querySelector('.arrow').textContent = rulesContent.style.display === 'none' ? '\u25BC' : '\u25B2';
});


function renderScore() {
    let noBlackDiscs = 0;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'black') {
                noBlackDiscs += 1;
            }
        }
    }
    const blackScoreDisc = document.getElementById('black-score-disc');
    blackScoreDisc.textContent = noBlackDiscs.toString();

    let noWhiteDiscs = 0;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'white') {
                noWhiteDiscs += 1;
            }
        }
    }
    const whiteScoreDisc = document.getElementById('white-score-disc');
    whiteScoreDisc.textContent = noWhiteDiscs.toString();
}

function updateScoreBorders() {
    // Used when player turn changes. Used to change the shaddow
    const blackScore = document.getElementById('black-score');
    const whiteScore = document.getElementById('white-score');
    if (currentPlayer === 'black') { // Change scoreboard of players for player turn
        blackScore.style.boxShadow = '0px 2px 10px rgba(0, 0, 0, 0.2)';
        whiteScore.style.boxShadow = '';
        blackScore.style.backgroundColor = 'rgb(248, 237, 180)';
        whiteScore.style.backgroundColor = 'white';
    }
    else {
        blackScore.style.boxShadow = '';
        whiteScore.style.boxShadow = '0px 2px 10px rgba(0, 0, 0, 0.2)';
        blackScore.style.backgroundColor = 'white';
        whiteScore.style.backgroundColor = 'rgb(248, 237, 180)';
    }
}

function gameEnd() {
    // Use this when both players have no legal moves. 
    // Will display game over text and victor
    let noBlackDiscs = 0;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'black') {
                noBlackDiscs += 1;
            }
        }
    }
    let noWhiteDiscs = 0;
    let result;
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (board[row][col] === 'white') {
                noWhiteDiscs += 1;
            }
        }
    }
    if (noBlackDiscs > noWhiteDiscs) {
        result = " Black Wins ";
        score = noBlackDiscs.toString() + " - " + noWhiteDiscs.toString()
    }
    else if (noBlackDiscs < noWhiteDiscs) {
        result = " White Wins ";
        score = noWhiteDiscs.toString() + " - " + noBlackDiscs.toString()
    }
    else {
        result = " Draw "
        score = noBlackDiscs.toString() + " - " + noWhiteDiscs.toString()
    }

    const gameEndText = document.getElementById('game-end-text');
    gameEndText.style.display = 'flex';
    gameEndText.textContent = "Game Over:" + result + score; 
}

document.addEventListener('DOMContentLoaded', function() {
    // This code will run when the page is loaded
    sendRequestForRandomMove();
});

function sendRequestForRandomMove() {
    const url = '/get_random_move';
    // Important to use full address her to connect to different server
    fetch(url, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => handleRandomMove(data.random_move))
    .catch(error => console.log('Error:', error));
}

function handleRandomMove(randomMove) {
    console.log(randomMove)
    // Use the randomMove received from Python in your game logic
    // For example: make a move on the board using the randomMove
}

// Initialise the game:
updateLegalMoves();
renderBoard();
renderScore();
updateScoreBorders();