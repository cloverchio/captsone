import flask
from flask import Flask, request

from dao.candidate_dao import CandidateDAO
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


@app.route("/candidates")
def candidates():
    candidate_data = candidateService.get_candidates()
    return flask.render_template("candidates.html", candidates=candidate_data)


@app.route("/candidates/new", methods=['GET', 'POST'])
def new_candidate():
    if request.method == "GET":
        return flask.render_template("new_candidate.html")
    if request.method == "POST":
        candidate_data = request.form.to_dict()
        candidate_id = candidateService.save_candidate(candidate_data['first_name'],
                                                       candidate_data['last_name'],
                                                       candidate_data['role'],
                                                       int(candidate_data['experience']))
        return flask.render_template("new_candidate.html", candidate=candidate_id)


if __name__ == '__main__':
    CandidateDAO.init_db()
    app.run()