import flask
import json
from flask import Flask, request

from dao.candidate_dao import CandidateDAO, CandidateDatabaseError
from service.candidate_service import CandidateService

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

candidateService = CandidateService()


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return flask.render_template("dashboard.html")


@app.route("/candidates", methods=['GET', 'POST'])
def candidates():
    candidates_template = "candidates.html"
    if request.method == 'GET':
        try:
            candidate_data = candidateService.get_candidates()
            return flask.render_template(candidates_template, candidates=candidate_data), 200
        except CandidateDatabaseError:
            return flask.render_template(candidates_template), 500
    if request.method == 'POST':
        try:
            candidate_ids = json.loads(request.data)
            candidateService.delete_candidates(candidate_ids)
            return flask.render_template(candidates_template), 204
        except CandidateDatabaseError:
            return flask.render_template(candidates_template), 500


@app.route("/candidates/new", methods=['GET', 'POST'])
def new_candidate():
    new_candidate_template = "new_candidate.html"
    if request.method == 'GET':
        return flask.render_template(new_candidate_template), 200
    if request.method == 'POST':
        try:
            candidate_data = request.form.to_dict()
            candidate_id = candidateService.save_candidate(candidate_data['first_name'],
                                                           candidate_data['last_name'],
                                                           candidate_data['role'],
                                                           int(candidate_data['experience']))
            return flask.render_template(new_candidate_template, candidate=candidate_id), 201
        except CandidateDatabaseError:
            return flask.render_template(new_candidate_template), 500


if __name__ == '__main__':
    CandidateDAO.init_db()
    app.run()
