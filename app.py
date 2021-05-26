import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, world!"