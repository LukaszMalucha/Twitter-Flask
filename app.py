##### App Utilities


import os

from flask_bootstrap import Bootstrap

from flask import Flask, render_template, current_app, request, redirect, url_for, flash






##### App Settings



app = Flask(__name__)

app.config['SECRET_KEY'] = 'BiggestSecret'

Bootstrap(app)