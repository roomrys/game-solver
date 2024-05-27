# game-solver

## Run the web app
This package has evolved over 1-day to include a Flask App for more detailed visual
feedback. To run the app, first get set-up with the dependencies (see below), then run

```python
python -m gsolver.app.main
```

and browse to

```
127.0.0.1:500
```

. The puzzle located at `gsolver/sudoku_puzzle.txt` will be populated on loading the
window. Hit the "Solve" button to see either the full solution or the partial solution
if "unsolveable" with the current game-solver.

Apart from the most simple puzzles, sudoku cannot be solved by just
eliminating possible cell values based on values that already exist in intersecting
rows, columns, and blocks (as the solver currently does). These "unsolvable" puzzles
yield partial solutions that are much better displayed in a GUI than on a text file. And
seeing the current state will help us understand how to implement code to fully solve
puzzles.

For example, game-solver currently outputs this partial solution:

<img width="500" alt="image" src="https://github.com/roomrys/game-solver/assets/38435167/ac9f8fde-460b-4c1a-86e3-1899cfb1d5be">

but, us human solvers can determine for example that this solution works for this cell

<img width="500" alt="image" src="https://github.com/roomrys/game-solver/assets/38435167/469b71c0-d459-43fd-a2f7-70353ad725ed">

using the reasoning that for row 4, "4" can only be in the second block. So for row 5, that
means that "4" cannot be in the second block. Since there is only one other place for "4"
in row 5 outside of the second block, "4" must be located there.

## Dependencies

To get started

1. Create a virtual environment

```bash
python3 -m venv gslvr
```

2. Activate the virtual environment

```bash
source gslvr/bin/activate
```

3. Install all the required packages in the virtual environment

```bash
pip install -r requirements.txt
```

When finished working with game-solver, you can deactivate the venv with

```bash
deactivate
```
