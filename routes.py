from flask import Flask, render_template, url_for, redirect, request
from app import app
from solver import solve_puzzle

empty = [[''] * 9 for i in range(9)]

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('frontend.html', matrix = empty)
    if request.method == 'POST':
        form = dict(request.form)
        results = solve_puzzle(form)
        list_copy = results.winning_list
        if not results.solved:
            for row in range(0,9):
                for column in range(0,9):
                    if list_copy[row][column] is None:
                        list_copy[row][column] = ''
        return render_template('frontend.html', solved = results.solved, matrix = list_copy)
