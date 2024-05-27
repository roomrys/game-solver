// Create a Sudoku board
function createSudokuBoard(numbers_by_index) {
  // Get the board container
  var boardContainer = document.getElementById("sudoku-board");

  // Create a 9x9 grid
  for (var i = 0; i < 9; i++) {
    var row = document.createElement("div");
    row.className = "row";
    for (var j = 0; j < 9; j++) {
      var cell = document.createElement("div");
      cell.className = "cell";
      cell.index = i + 1 + "," + (j + 1);

      var cellInput = document.createElement("input");
      cell.maxLength = "1";
      cellInput.className = "cell-input";
      cellInput.type = "text";
      cell.appendChild(cellInput);
      cell.cellInput = cellInput;

      var options = document.createElement("div");
      options.className = "options";
      options.type = "text";
      cell.appendChild(options);
      cell.options = options;

      // Check if there's a value for this cell in numbers_by_index
      var key = i + 1 + "," + (j + 1); // +1 because Sudoku grid indices start from 1, not 0
      if (numbers_by_index.hasOwnProperty(key)) {
        cellInput.value = numbers_by_index[key];
        cellInput.readOnly = true;
      }

      row.appendChild(cell);
    }
    boardContainer.appendChild(row);
  }
}

function updateSudokuBoard(numbers_by_index) {
  // Get all the cells
  var cells = document.getElementsByClassName("cell");

  // Update the value of each cell
  for (var i = 0; i < cells.length; i++) {
    var cell = cells[i];
    var key = cell.index;
    var options = cell.options;
    var cellInput = cell.cellInput;

    console.log(numbers_by_index);
    console.log(`key = ${key}`);
    console.log(options);
    // Check if the cell is read-only
    if (cell.readOnly) {
      // Ensure that the value is correct
      if (cell.value != numbers_by_index[key]) {
        console.log("Incorrect value in cell " + key);
        // Turn cell text red
        cellInput.style.color = "red";
      }
      continue;
    } else {
      // Reset cell text color
      cellInput.style.color = "black";

      // Check if the value is a list
      if (Array.isArray(numbers_by_index[key])) {
        // Display the list as a comma-separated string
        options.textContent = numbers_by_index[key].join(",");
      } else {
        cellInput.value = numbers_by_index[key];
      }
    }
  }
}

// // TODO(LM): Remove hard-coded numbers_by_index and instead add two buttons:
// // - "Set Puzzle" for users to manually enter then set the starting positions
// // - "Generate Puzzle" to randomly generate a puzzle
// // Call the function to create the board
// var numbers_by_index = {
//   "1,2": 6,
//   "1,5": 9,
//   "1,7": 3,
//   "2,3": 5,
//   "2,6": 8,
//   "2,9": 4,
//   "3,1": 7,
//   "3,4": 6,
//   "3,8": 5,
//   "4,2": 2,
//   "4,4": 8,
//   "4,8": 6,
//   "5,3": 6,
//   "5,5": 7,
//   "5,7": 5,
//   "6,1": 4,
//   "6,6": 1,
//   "6,9": 8,
//   "7,2": 4,
//   "7,4": 3,
//   "7,7": 1,
//   "7,8": 9,
//   "8,3": 7,
//   "8,5": 5,
//   "8,9": 3,
//   "9,1": 3,
//   "9,6": 2,
//   "9,7": 4,
// };
// createSudokuBoard((numbers_by_index = numbers_by_index));
