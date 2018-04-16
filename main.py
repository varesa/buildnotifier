from time import sleep
from flask import Flask, redirect, render_template, request


# Initialize app

app = Flask(__name__)

@app.route('/post', methods=['POST'])
def post():
    data = request.json
    if data['type'] == 'stage':
        print('Running stage: ' + data['stage'])

    if data['type'] == 'complete':
        print('Build complete: ' + data['url'])
    return ''

@app.route('/health')
def healthcheck():
    return 'OK'

