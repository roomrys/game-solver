from logging import getLogger

from flask import Flask, jsonify, render_template, request, session

from ..sudoku import Sudoku

logger = getLogger(__name__)

app = Flask(__name__)
app.secret_key = "gsolver"

sudoku = Sudoku(string_keys=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get-board")
def get_board():
    numbers_by_index_str_keys = sudoku.numbers_by_index_str_keys
    return jsonify(numbers_by_index_str_keys)


@app.route("/update", methods=["POST"])
def update_board():
    body = request.get_json()
    logger.debug(f"Update board request: {body}")

    user_values = body.get("userValues", {})
    for key, value in user_values.items():
        sudoku.update(key, value)

    return jsonify({"status": "success"}), 200


@app.route("/solve")
def solve():
    matrix = sudoku.solve(matrix=sudoku.matrix)
    logger.info(f"Solved matrix: {matrix}/nPatial solution: {sudoku.partial_solution}")
    numbers_by_index = sudoku.solution_to_numbers_by_index(
        solution=sudoku.solution, string_keys=True
    )
    return jsonify(numbers_by_index)


if __name__ == "__main__":
    app.run(debug=True)
