from flask import render_template, request
import json

from app import app
from solver import SolvePuzzle


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('frontend.html')
    if request.method == 'POST':
        puzzle_input = dict(request.form)
        solve_me = SolvePuzzle(puzzle_input)
        solution = solve_me.final_solved_puzzle
        solution_with_strings = {str(key): str(value) for (key, value) in solution.items()}
        return json.dumps(solution_with_strings)

