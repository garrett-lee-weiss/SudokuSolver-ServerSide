from flask import render_template, request
from app import app
from solver import SolvePuzzle

empty = [[''] * 9 for i in range(9)]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('frontend.html', matrix = empty)
    if request.method == 'POST':
        puzzle_input = dict(request.form)
        solve_me = SolvePuzzle(puzzle_input)
        solution = solve_me.final_solved_puzzle
        return render_template('frontend.html', solved = solve_me.is_puzzle_solved, matrix = solution)
