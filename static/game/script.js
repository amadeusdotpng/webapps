/* i'm going to use global variables I DON'T CARE*/
/* [x] implement pathfinding algo
 * [x]  choose one random outer cell i.e. (-1, -1).
 * [x]  focus on that path for the rest of the game.
 * [x]  update path if droppedCells && path.
 * [x] update board
 * [x] detect win
 * [ ] detect loss
 * [ ] win/loss screen
 * [ ] reset board
 */
const boardWidth = 21;
const boardHeight = 21;
let angelCoord;
let angelFocus;
let angelPath;
let droppedCells = new Set()
let gameWon = false;
let gameLost = false;

window.onload = function loadGame() {
	loadBoard(boardWidth, boardHeight);
	setAngel([Math.floor(boardWidth/2), Math.floor(boardHeight/2)]);
	preDropCells(0.15);
	angelFocus = setAngelFocus();
	angelPath = getAngelPath(angelFocus);
	console.log(angelFocus)
	console.log(angelPath)
	document.getElementById("win").setAttribute("style", "display:none");
	document.getElementById("lose").setAttribute("style", "display:none");
}

function loadBoard() {
	let board = document.getElementById("board");
	for(let i = 0; i < boardWidth; i++) {
		for(let j = 0; j < boardHeight; j++) {
			const cell = document.createElement("div");
			cell.classList.add("cell");
			cell.id=`cell_${i}_${j}`
			cell.coord = [i,j]
			cell.addEventListener('click', ()=> {updateBoard(cell)});

			const margin = 0.5;
			const wid = Math.round((board.offsetWidth / boardWidth - 2*margin)*100) / 100;
			const len = Math.round((board.offsetHeight / boardHeight - 2*margin)*100) / 100;
			cell.setAttribute("style", `width:${wid}px;height:${len}px;margin:${margin}px`);
			board.appendChild(cell);
		}
	}
}

function updateBoard(cell) {
	if(gameWon || gameLost) return;
	const coord = cell.coord;
	if(!dropCell(cell)) return;
	for(let c of angelPath) {
		if(equalCoord(coord, c)) {
			angelPath = getAngelPath(angelFocus);
		}
	}
	win()
	updateAngel(angelPath.shift());
}

function resetBoard() {
	droppedCells = new Set();
	for(let i = 0; i < boardWidth; i++) {
		for(let j = 0; j < boardHeight; j++) {
			const cell = getCellByCoord([i,j])
			cell.classList.remove("dropped")
		}
	}
	const angelCell = getCellByCoord(angelCoord);
	if(!(angelCell === null)) {
		angelCell.classList.remove("angel");
	}
	setAngel([Math.floor(boardWidth/2), Math.floor(boardHeight/2)]);
	preDropCells(0.12);
	angelFocus = setAngelFocus();
	angelPath = getAngelPath(angelFocus);
	gameWon = false;
	gameLost = false;
	document.getElementById("win").setAttribute("style", "display:none");
	document.getElementById("lose").setAttribute("style", "display:none");
}

function win() {
	if(angelPath === null) {
		gameWon = true;
		document.getElementById("win").setAttribute("style", "display:static");
		return true;
	}
	return false;
}

function lose() {
	if(angelCoord[0] < 0 ||
	   angelCoord[0] >= boardWidth ||
	   angelCoord[1] < 0 ||
	   angelCoord[1] >= boardHeight) {
		
		document.getElementById("lose").setAttribute("style", "display:static");
		gameLost = true;
		return true;
	}
	return false;
}

function dropCell(targetCell) {
	if(droppedCells.has(targetCell.coord.toString())) return false;
	if(equalCoord(targetCell.coord, angelCoord)) return false;

	targetCell.classList.add("dropped")
	droppedCells.add(targetCell.coord.toString())

	return true;
}

function preDropCells(density) {
	for(i = 0; i < boardWidth; i++) {
		for(j = 0; j < boardHeight; j++) {
			const cell = getCellByCoord([i,j]);
			if(Math.random() < density) dropCell(cell);
		}
	}
}

function setAngel(coord) {
	angelCoord = coord;
	if(lose()) return;
	const angel = getCellByCoord(coord)
	angel.classList.toggle("angel")
}

function updateAngel(coord) {
	const angelCell = getCellByCoord(angelCoord)
	angelCell.classList.toggle("angel")
	setAngel(coord);
}

function setAngelFocus() {
	let side = Math.floor(Math.random()*4)
	if(side == 0) {
		return [-1,Math.floor(Math.random()*(boardHeight+2)-1)]
	} else if(side == 1) {
		return [boardWidth,Math.floor(Math.random()*(boardHeight+2)-1)]
	} else if(side == 2) {
		return [Math.floor(Math.random()*(boardWidth+2)-1), boardHeight]
	} else if(side == 3) {
		return [Math.floor(Math.random()*(boardWidth+2)-1), -1]
	}
}

/* BFS */
function getAngelPath(focus) {
	let queue = [];
	let explored = new Set();
	let parents = {};
	queue.push(angelCoord);
	explored.add(angelCoord.toString());

	while(queue.length != 0) {
		let cell = queue.shift();
		if(equalCoord(cell, focus)) {
			let path = []
			while(cell in parents) {
				path.unshift(cell);
				cell = parents[cell];
			}
			return path;
		}
		for(let edge of getCellNeighbours(cell)) {
			if(!droppedCells.has(edge.toString()) &&
			   !explored.has(edge.toString())) {
				explored.add(edge.toString());
				parents[edge] = cell;
				queue.push(edge);
			}
		}
	}
	return null;
}

function getCellNeighbours(coord) {
	const [x, y] = coord;
	return [[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y],[x+1,y-1],[x,y-1],[x-1,y-1]]
//	return [[x-1,y],[x,y+1],[x+1,y],[x,y-1]];
}

function equalCoord(c0, c1) {
	return c0[0] == c1[0] && c0[1] == c1[1];
}

function getCellByCoord(coord) {
	return document.getElementById(`cell_${coord[0]}_${coord[1]}`);
}
