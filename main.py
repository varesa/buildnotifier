from time import sleep
from flask import Flask, redirect, render_template, request


# Initialize app

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post():
    print(request.form)

@app.route('/health')
def healthcheck():
    return 'OK'

