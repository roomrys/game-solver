// Try to solve the board when the button is clicked
document.getElementById("button-solve").addEventListener("click", function () {
  solveBoard();
});

// Try to solve the board when the Enter key is pressed
document.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    solveBoard();
  } else if (event.key === "ArrowRight") {
    solveBoard(true);
  }
});

// Load the board when the page is loaded
window.addEventListener("load", function () {
  fetch("/get-board")
    .then((response) => response.json())
    .then((data) => createSudokuBoard((numbers_by_index = data)))
    .then(() => {
      // Limit the input to single numbers only
      var inputs = document.querySelectorAll(".cell-input");
      inputs.forEach(function (input) {
        input.setAttribute("maxLength", "1");
        input.addEventListener("keydown", function (event) {
          if (event.key === "Enter") {
            solveBoard();
          } else {
            this.value = "";
          }
        });
        input.addEventListener("keypress", function (event) {
          var allowedCharacters = "123456789";
          if (
            allowedCharacters.indexOf(String.fromCharCode(event.charCode)) < 0
          ) {
            event.preventDefault();
          }
        });
      });
    });
});
