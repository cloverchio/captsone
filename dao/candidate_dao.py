import sqlite3
from sqlite3 import Error

from model.candidate import Candidate


class CandidateDAO:

    def __init__(self):
        pass

    # save candidate information to the db
    @staticmethod
    def save_candidate(candidate):
        conn = CandidateDAO.__get_connection()
        conn.cursor().execute("INSERT INTO candidates (id, first_name, last_name, role, years_experience, salary) "
                              "VALUES (?, ?, ?, ?, ?, ?)",
                              (candidate.get_candidate_id(),
                               candidate.get_first_name(),
                               candidate.get_last_name(),
                               candidate.get_role(),
                               candidate.get_years_experience(),
                               candidate.get_salary()))
        conn.commit()
        conn.close()

    # delete candidate information from the db
    @staticmethod
    def delete_candidate(candidate_id):
        conn = CandidateDAO.__get_connection()
        conn.cursor().execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
        conn.commit()
        conn.close()

    # retrieve candidate by from the db
    @staticmethod
    def get_candidate(candidate_id):
        conn = CandidateDAO.__get_connection()
        curr = conn.cursor()
        curr.execute("SELECT id, first_name, last_name, role, years_experience, salary, created_on "
                     "FROM candidates WHERE id = ?",
                     (candidate_id,))
        values = curr.fetchall()
        if values:
            value = values[0]
            return Candidate(value[0],
                             value[1],
                             value[2],
                             value[3],
                             value[4],
                             value[5],
                             value[6])
        return None

    # retrieves all candidates from the db
    @staticmethod
    def get_all_candidates():
        conn = CandidateDAO.__get_connection()
        curr = conn.cursor()
        curr.execute("SELECT id, first_name, last_name, role, years_experience, salary, created_on "
                     "FROM candidates")
        values = curr.fetchall()
        candidates = []
        if values:
            for value in values:
                candidate = Candidate(value[0],
                                      value[1],
                                      value[2],
                                      value[3],
                                      value[4],
                                      value[5],
                                      value[6])
                candidates.append(candidate)
        return candidates

    # meant to initialize db on application startup
    @staticmethod
    def init_db():
        conn = CandidateDAO.__get_connection()
        with open('dao/schema.sql') as f:
            conn.executescript(f.read())
            conn.commit()
            conn.close()
        f.close()

    # establish db connection
    @staticmethod
    def __get_connection():
        conn = None
        try:
            conn = sqlite3.connect('candidates.db')
        except Error as e:
            print(e)
        return conn
