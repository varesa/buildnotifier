from time import sleep
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize app

app = Flask(__name__)

@app.route('/health')
def healthcheck():
    return 'OK'

