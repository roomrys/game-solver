"""This module contains code to solve sudoku puzzle."""

import logging
import numpy as np
import sys
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)


class Sudoku:
    """This class represents a sudoku puzzle."""

    def __init__(self, puzzle_file: str | None = None, string_keys: bool = False):
        """Initialize the sudoku puzzle.

        Args:
            puzzle_file: The file containing the sudoku puzzle. The file should
                contain the puzzle in the following format:
                +-------+-------+-------+
                | 1 . . | . . . | . . . |
                | . 2 . | . . . | . . . |
                | . . 3 | . . . | . . . |
                +-------+-------+-------+
                | . . . | 4 . . | . . . |
                | . . . | . 5 . | . . . |
                | . . . | . . 6 | . . . |
                +-------+-------+-------+
                | . . . | . . . | 7 . . |
                | . . . | . . . | . 8 . |
                | . . . | . . . | . . 9 |
                +-------+-------+-------+
        """

        self.string_keys = string_keys
        self.puzzle_file = puzzle_file or "./sudoku_puzzle.txt"

        self.numbers_by_index, self.puzzle_size = self.read_puzzle(
            puzzle_file=self.puzzle_file
        )

        self.numbers_encoded, self.numbers_decoded = self.encode_numbers(
            puzzle_size=self.puzzle_size
        )

        self.matrix = self.numbers_by_index_to_matrix(
            numbers_by_index=self.numbers_by_index,
            puzzle_size=self.puzzle_size,
            numbers_encoded=self.numbers_encoded,
        )

        # Blocks are numbered from left to right and secondarily from top to bottom
        self.blocks = self.get_blocks(puzzle_size=self.puzzle_size, matrix=self.matrix)
        self.rows = self.get_rows(matrix=self.matrix)
        self.columns = self.get_columns(matrix=self.matrix)

        self.solution = None
        self.number_iterations = 0
        self.partial_solution = False
        self.last_solved = ("block", self.puzzle_size - 1)
        self.solution_file = Path(self.puzzle_file).parent / "sudoku_solution.txt"

    def get_blocks(self, puzzle_size: int, matrix: np.ndarray):
        """This function returns the blocks in the sudoku puzzle."""

        blocks = []
        sqrt_puzzle_size = int(np.sqrt(puzzle_size))

        for row in range(0, puzzle_size, sqrt_puzzle_size):
            for col in range(0, puzzle_size, sqrt_puzzle_size):
                block = matrix[
                    row : row + sqrt_puzzle_size, col : col + sqrt_puzzle_size
                ]
                blocks.append(block)

        return blocks

    def get_rows(self, matrix: np.ndarray):
        """This function returns the rows in the sudoku puzzle."""
        return [matrix[row, :, :] for row in range(matrix.shape[0])]

    def get_columns(self, matrix: np.ndarray):
        """This function returns the columns in the sudoku puzzle."""
        return [matrix[:, col, :] for col in range(matrix.shape[1])]

    @classmethod
    def encode_numbers(cls, puzzle_size: int):
        """This function encodes the numbers in the puzzle."""
        logger.info("Encoding numbers")

        np.eye(puzzle_size)

        numbers_encoded = {}
        numbers_decoded = {}
        for number in range(1, puzzle_size + 1):
            numbers_encoded[number] = np.eye(puzzle_size)[:, number - 1]
            numbers_decoded[tuple(numbers_encoded[number])] = number

        return numbers_encoded, numbers_decoded

    def read_puzzle(self, puzzle_file: str | None = None) -> list[list[int]]:
        """This function reads a sudoku puzzle from the user."""
        logger.info("Reading sudoku puzzle")

        if puzzle_file is None:
            logger.info("Reading local puzzle at [./sudoku_puzzle.txt]")
            puzzle_file = "./sudoku_puzzle.txt"

        puzzle_file = (
            Path(__file__).parent / puzzle_file
            if puzzle_file.startswith(".")
            else Path(puzzle_file)
        )
        if not puzzle_file.exists():
            logger.error("Puzzle file not found")
            return []

        with open(puzzle_file, "r") as file:
            puzzle_lines = file.readlines()

        numbers_by_index = {}
        numbers_by_index_string_keys = {}
        row = 0
        column = 0
        for line in puzzle_lines:
            if line.startswith("|"):
                row += 1
                column = 1
                for char in line[1:-2]:
                    if char == "." or char == "|":
                        column += 1
                        continue

                    if char.isdigit():
                        string_key = f"{row},{column}"
                        numbers_by_index_string_keys[string_key] = int(char)
                        key = (row, column)
                        numbers_by_index[key] = int(char)

        if row != column:
            logger.error("Puzzle is not a square")
            logger.error(f"row = {row}, column = {column}")
            raise ValueError("Puzzle is not a square")

        puzzle_size = row

        logger.info("Puzzle read successfully")
        logger.debug(f"numbers_by_index = {numbers_by_index}")
        logger.debug(f"puzzle_size = {puzzle_size}")

        self.numbers_by_index_str_keys = numbers_by_index_string_keys
        return numbers_by_index, puzzle_size

    def solution_to_numbers_by_index(
        self, solution: np.array, string_keys: bool = False
    ):
        """This function converts the solution to a dictionary of numbers by index.

        If there are multiple solutions for a cell, the function will return all the
        possible solutions for that cell in a list.
        """

        logger.info("Converting solution to numbers by index")

        numbers_by_index = {}
        for row in range(solution.shape[0]):
            for column in range(solution.shape[1]):
                try:
                    number = self.numbers_decoded[tuple(solution[row, column])]
                except KeyError:
                    encoded_numbers = np.where(solution[row, column] == 1)[0] + 1
                    number = encoded_numbers.tolist()

                if string_keys:
                    key = f"{row + 1},{column + 1}"
                else:
                    key = (row + 1, column + 1)

                numbers_by_index[key] = number

        logger.debug(f"numbers_by_index = {numbers_by_index}")

        return numbers_by_index

    def solution_to_board(self, solution: np.array, partial: bool = False):
        """This function converts the solution to a sudoku board txt."""

        logger.info("Converting solution to board")

        sqrt_puzzle_size = int(np.sqrt(self.puzzle_size))
        row_border = ("+" + "-" * (int(sqrt_puzzle_size) + 2)) * int(
            sqrt_puzzle_size
        ) + "+"

        with open(self.solution_file, "w") as file:
            if partial:
                file.write("Partial solution\n")

            for row in range(solution.shape[0]):

                if row % sqrt_puzzle_size == 0:
                    file.write(f"{row_border}\n")

                for column in range(solution.shape[1]):
                    col_mod = True if column % sqrt_puzzle_size == 0 else False
                    if col_mod:
                        file.write("|")

                    try:
                        number = self.numbers_decoded[tuple(solution[row, column])]
                        file.write(f"{number}")

                    except KeyError:
                        file.write(" ")

                    if not (column + 1) % sqrt_puzzle_size == 0:
                        file.write(".")

                file.write("|\n")

            file.write(f"{row_border}")

        logger.info(f"Solution saved to file [{self.solution_file}]")

    def numbers_by_index_to_matrix(
        self,
        numbers_by_index: dict[tuple[int, int], int],
        puzzle_size: int,
        numbers_encoded: dict[int, np.array],
    ) -> list[list[int]]:
        """This function converts the numbers_by_index to a matrix.

        The numbers_by_index is a dictionary with the key being a tuple of the row and
        column index and the value being the number at that index.

        The matrix is a nxnxn np array where n is the size of the sudoku puzzle. Each cell
        in the puzzle is represented by a nx1 binary vector where the index of the 1 in the
        vector represents the number at that cell. Then, there are n rows of nx1 vectors and
        also n columns of nx1 vectors.

        If the number is not yet solved for, the the vector will have 1's in more than one
        place indicating the possible solutions. On initialization, only numbers that have
        been solved for will have a single 1 in the vector. All empty cells will have 1's in
        all the places.

        Args:
            numbers_by_index: A dictionary with the key being a tuple of the row and column
                index and the value being the number at that index.
            puzzle_size: The size of the sudoku puzzle, i.e. "n".

        Returns:
            A nxnxn np array where n is the size of the sudoku puzzle.
        """

        logger.info("Converting numbers_by_index to matrix")

        # Initialize the matrix to all 1's
        matrix = np.ones((puzzle_size, puzzle_size, puzzle_size))

        # Fill in the numbers that have been solved for
        for (row, column), number in numbers_by_index.items():
            matrix[row - 1, column - 1] = numbers_encoded[number]

        logger.debug(f"matrix = {matrix}")
        logger.debug(f"matrix.shape = {matrix.shape}")

        return matrix

    def remove_impossible_solutions(self, vectors: np.array):
        """This function updates the possible solutions for a single row in the puzzle."""

        # 1. Find vector indices where sum of all vectors along third axis is 1
        solved_vector_inds = np.where(np.sum(vectors, axis=-1) == 1)
        logger.debug(f"solved_vector_inds = {solved_vector_inds}")

        # 2. Use vector indices to return solved vectors
        solved_vectors = vectors[solved_vector_inds]

        # 2a. Check if any vectors are the same
        unique_vectors, counts = np.unique(solved_vectors, axis=0, return_counts=True)
        if not np.all(counts == 1):
            duplicate_vectors = unique_vectors[np.where(counts > 1)]
            duplicate_numbers = np.where(duplicate_vectors[0] == 1)[0] + 1
            logger.error(
                f"Duplicate vectors found in solved vectors!: {duplicate_numbers.tolist()}"
            )
            return False

        # 3. Find indices where sum of all solved vectors along rows is 1
        unavailable_numbers = np.where(np.sum(solved_vectors, axis=0) == 1)

        # 4. Use vector indices from 2 to return unsolved vector indices
        unsolved_vector_inds = np.where(np.sum(vectors, axis=-1) != 1)

        # 5. Use unsolved vector indices to return unsolved vectors
        unsolved_vectors = vectors[unsolved_vector_inds]

        # 6. Use unsolved vectors and available numbers to update allowed numbers
        unsolved_vectors[:, unavailable_numbers] = 0
        vectors[unsolved_vector_inds] = unsolved_vectors

        return True

    def use_single_appearance_solution(self, vectors: np.array):
        """Find and use possible solutions that only appear once in the unsolved vectors."""

        # 1. Find all unsolved vectors
        unsolved_vector_inds = np.where(np.sum(vectors, axis=-1) != 1)
        unsolved_vectors = vectors[unsolved_vector_inds]

        # 2. Find all possible solutions that only appear once in the unsolved vectors
        global_single_appearance_solutions = np.where(np.sum(vectors, axis=0) == 1)[0]
        local_single_appearance_solutions = np.where(
            np.sum(unsolved_vectors, axis=0) == 1
        )[0]

        # Retain only single appearance solutions that are unsolved
        unsolved_single_appearance_solutions = np.intersect1d(
            global_single_appearance_solutions, local_single_appearance_solutions
        )

        if unsolved_single_appearance_solutions.shape[0] == 0:
            return

        # 3. Gather vector and solution indices
        vector_inds, solution_inds = np.where(
            unsolved_vectors[:, unsolved_single_appearance_solutions] == 1
        )
        solutions_ordered = unsolved_single_appearance_solutions[solution_inds]

        # 4. Use single appearance solutions to update unsolved vectors
        unsolved_vectors[vector_inds, :] = np.eye(self.puzzle_size)[solutions_ordered]
        vectors[unsolved_vector_inds] = unsolved_vectors

    def update_vectors(self, vectors: np.array):
        """This function updates the possible solutions for a single vector group."""

        # 1. Remove solved numbers from unsolved vectors
        okay = self.remove_impossible_solutions(vectors=vectors)
        if not okay:
            return False

        # 2. Find possible solutions that only appear once in the unsolved vectors
        self.use_single_appearance_solution(vectors=vectors)

        return True

    def solve(self, matrix: np.array, single_iteration: bool = False):
        """This function solves the sudoku puzzle."""

        self.partial_solution = False
        matrix_prev = np.copy(matrix) + 1

        num_iterations = 0
        while not np.array_equal(matrix, matrix_prev):

            num_iterations += 1
            self.number_iterations = num_iterations

            # 0. Check if puzzle is solved
            if np.sum(np.sum(matrix, axis=2) == 1) == matrix.shape[0] ** 2:
                logger.info("Puzzle solved!")
                break

            matrix_prev = np.copy(matrix)

            # 1. Solve for rows
            solve_for_row = self.last_solved == ("block", self.puzzle_size - 1) or (
                self.last_solved[0] == "row"
                and self.last_solved[1] != self.puzzle_size - 1
            )
            logger.debug(f"Solving for row: {solve_for_row}")
            if not single_iteration or solve_for_row:
                rows = (
                    self.rows
                    if not single_iteration
                    else [self.rows[(self.last_solved[1] + 1) % self.puzzle_size]]
                )
                for index, row in enumerate(rows):
                    index = (
                        (self.last_solved[1] + 1) % self.puzzle_size
                        if single_iteration
                        else index
                    )
                    logger.debug(f"Solving for row {index} = \n{row}")
                    okay = self.update_vectors(vectors=row)
                    if not okay or (single_iteration and solve_for_row):
                        self.partial_solution = True
                        break

            if single_iteration and solve_for_row:
                self.last_solved = ("row", index)
                break

            # 2. Solve for columns
            solve_for_column = self.last_solved == ("row", self.puzzle_size - 1) or (
                self.last_solved[0] == "column"
                and self.last_solved[1] != self.puzzle_size - 1
            )
            logger.debug(f"Solving for columns: {solve_for_column}")
            if not single_iteration or solve_for_column:
                columns = (
                    self.columns
                    if not single_iteration
                    else [self.columns[(self.last_solved[1] + 1) % self.puzzle_size]]
                )
                for index, column in enumerate(columns):
                    index = (
                        (self.last_solved[1] + 1) % self.puzzle_size
                        if single_iteration
                        else index
                    )
                    logger.debug(f"Solving for column {index} = \n{column}")
                    okay = self.update_vectors(vectors=column)
                    if (not okay) or (single_iteration and solve_for_column):
                        self.partial_solution = True
                        break

            if single_iteration and solve_for_column:
                self.last_solved = ("column", index)
                break

            # 3. Solve for blocks
            solve_for_block = self.last_solved == ("column", self.puzzle_size - 1) or (
                self.last_solved[0] == "block"
                and self.last_solved[1] != self.puzzle_size - 1
            )
            logger.debug(f"Solving for blocks: {solve_for_block}")
            if not single_iteration or solve_for_block:
                blocks = (
                    self.blocks
                    if not single_iteration
                    else [self.blocks[(self.last_solved[1] + 1) % self.puzzle_size]]
                )
                for index, block in enumerate(blocks):
                    index = (
                        (self.last_solved[1] + 1) % self.puzzle_size
                        if single_iteration
                        else index
                    )
                    logger.debug(f"Solving for block {index} = \n{block}")
                    okay = self.update_vectors(vectors=block)
                    if (not okay) or (single_iteration and solve_for_block):
                        self.partial_solution = True
                        self.last_solved = ("block", index)
                        break

            if single_iteration and solve_for_block:
                self.last_solved = ("block", index)
                break

            # 7. Check if unsolvable
            if np.array_equal(matrix_prev, matrix):
                logger.error(
                    f"No change in matrix solution after iteration {num_iterations}."
                    f"\nPuzzle is unsolvable."
                )
                self.partial_solution = True

            if self.partial_solution:
                logger.error(
                    f"Partial solution found after iteration {num_iterations}."
                )
                break

            # 8. Repeat from 1
            if single_iteration:
                break

        logger.info(f"num_iterations = {num_iterations}")

        self.matrix = matrix
        self.solution = matrix
        return matrix

    def update(self, key: str, value: int):
        """This function updates the puzzle with the user's input."""
        logger.info(f"Updating puzzle with user input: {key} = {value}")

        row, column = key.split(",")
        row = int(row)
        column = int(column)

        # Would be nice if user could delete a number, but doing this messes up the options
        # if value == 0:
        #     self.matrix[row - 1, column - 1] = np.ones(self.puzzle_size)

        if value > 0:
            self.matrix[row - 1, column - 1] = self.numbers_encoded[value]


if __name__ == "__main__":
    sudoku = Sudoku(puzzle_file="./sudoku_puzzle.txt")
    for _ in range(100):
        soln = sudoku.solve(matrix=sudoku.matrix, single_iteration=True)
    # sudoku.solution_to_board(solution=soln)
    sudoku.solution_to_numbers_by_index(solution=soln, string_keys=True)
