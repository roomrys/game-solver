# game-solver

## Run the web app

This package has evolved over 1-day to include a Flask App for more detailed visual
feedback. To run the app, first get set-up with the dependencies (see below), then run

```python
python -m gsolver.app.main
```

and browse to

```
127.0.0.1:5000
```

. The puzzle located at `gsolver/sudoku_puzzle.txt` will be populated on loading the
window. Hit the "Solve" button to see either the full solution or the partial solution
if "unsolveable" with the current game-solver.

## Current solver state: COMPLETE

Apart from the most simple puzzles, sudoku cannot be solved by just
eliminating possible cell values based on values that already exist in intersecting
rows, columns, and blocks.

For example, consider this partial solution, paying particular attention to row 5 (1-indexed):

<img width="500" alt="image" src="https://github.com/roomrys/game-solver/assets/38435167/65486b59-75df-45a9-ae58-ba192744e8bb">

. We see that there are multiple cells where the number "4" might be placed in row 5, but if we instead consider which rows, columns, or blocks require a "4", then we see that the right most center block only has one option where a "4" can be placed, leading us to this solution:

<img width="500" alt="image" src="https://github.com/roomrys/game-solver/assets/38435167/025c780e-fc0b-4570-bff0-33cc83fe1daf">

.

So far, after a weekend of testing (and one particularly difficult newspaper soduko puzzle), the puzzle has been solved using this alternating strategy:
1. Remove intersecting values from the solution space
2. Accept solutions that only appear once in the solution space for a row, column, or block

Originally the problem was formulated in such a way that we might get to do some linear algebra, but no real luck there. There is always the hope for a vectorization refactor.

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
