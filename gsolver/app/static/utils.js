function solveBoard(singleIteration = false) {
  // Try to solve the board when the Enter key is pressed
  fetch("/update", {
    method: "POST",
    body: JSON.stringify({ userValues: getUserUpdatedSudokuBoardValues() }),
    headers: {
      "Content-Type": "application/json",
    },
  }).then(() => {
    fetch("/solve", {
      method: "POST",
      body: JSON.stringify({ singleIteration: singleIteration }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => updateSudokuBoard((numbers_by_index = data)));
  });
}
