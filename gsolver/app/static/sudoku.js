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
        cellInput.classList.add("readonly");
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

    // Check if the cell is read-only
    if (cell.readOnly) {
      // Ensure that the value is correct
      if (cell.value != numbers_by_index[key]) {
        console.log("Incorrect value in cell " + key);
        // Turn cell text red
        cellInput.classList.add("conflict");
      } else {
        // Reset cell text color
        cellInput.classList.remove("conflict");
      }
      continue;
    } else {
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
