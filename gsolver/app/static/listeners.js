document.getElementById("button-solve").addEventListener("click", function () {
  fetch("/solve")
    .then((response) => response.json())
    .then((data) => updateSudokuBoard((numbers_by_index = data)));
});

window.addEventListener("load", function () {
  fetch("/get-board")
    .then((response) => response.json())
    .then((data) => createSudokuBoard((numbers_by_index = data)));
});
