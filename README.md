# game-solver

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

# TODO paste screenshot

but, us human solvers can determine for example that this solution works for this cell

# TODO past screenshot

using the reasoning that well "4" can only be in these places and if "4" can only be
here for this row, then that means "4" cannot be in the same block for these other rows,
and "4" only has one other option for this other row outside of the "taken" block, so
"4" must be in the other block.

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
