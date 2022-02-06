import json
import os
from functools import wraps

import flask
from flask import Flask, request, session, redirect, url_for

from dao.candidate_dao import CandidateDAO, CandidateDatabaseError
from service.candidate_service import CandidateService
from service.prediction_service import PredictionService

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

candidate_dao = CandidateDAO(os.environ['DATABASE_URL'])
prediction_service = PredictionService()
candidate_service = CandidateService(candidate_dao, prediction_service)

app.secret_key = os.environ['SECRET_KEY']


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        return redirect(url_for('login'))

    return wrap


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_template = "login.html"
    if request.method == 'GET':
        return flask.render_template(login_template), 200
    if request.method == 'POST':
        login_data = request.form.to_dict()
        default_username = os.environ['USER']
        default_password = os.environ['PASS']
        if login_data['username'] != default_username and login_data['password'] != default_password:
            return flask.render_template(login_template, invalid_login="Username or password was incorrect."), 400
        session['logged_in'] = True
        return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route("/dashboard")
@login_required
def dashboard():
    return flask.render_template("dashboard.html"), 200


@app.route("/candidates", methods=['GET', 'POST'])
@login_required
def candidates():
    candidates_template = "candidates.html"
    if request.method == 'GET':
        try:
            candidate_data = candidate_service.get_candidates()
            return flask.render_template(candidates_template, candidates=candidate_data), 200
        except CandidateDatabaseError:
            return flask.render_template(candidates_template), 500
    if request.method == 'POST':
        try:
            candidate_ids = json.loads(request.data)
            candidate_service.delete_candidates(candidate_ids)
            return flask.render_template(candidates_template), 204
        except CandidateDatabaseError:
            return flask.render_template(candidates_template), 500


@app.route("/candidates/new", methods=['GET', 'POST'])
@login_required
def new_candidate():
    new_candidate_template = "new_candidate.html"
    if request.method == 'GET':
        return flask.render_template(new_candidate_template), 200
    if request.method == 'POST':
        try:
            candidate_data = request.form.to_dict()
            candidate_id = candidate_service.save_candidate(candidate_data['first_name'],
                                                            candidate_data['last_name'],
                                                            candidate_data['role'],
                                                            int(candidate_data['experience']))
            return flask.render_template(new_candidate_template, candidate=candidate_id), 201
        except CandidateDatabaseError as e:
            return flask.render_template(new_candidate_template), 500


if __name__ == '__main__':
    candidate_dao.init_db()
    app.run()
