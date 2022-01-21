import sqlite3
from sqlite3 import Error

from model.candidate import Candidate


class CandidateDatabaseError(Exception):
    pass


class CandidateDAO:

    def __init__(self):
        pass

    @staticmethod
    def save_candidate(candidate):
        """
        Saves a candidate object to the db.
        """
        conn = CandidateDAO.__get_connection()
        try:
            conn.cursor().execute("INSERT INTO candidates (id, first_name, last_name, role, years_experience, salary) "
                                  "VALUES (?, ?, ?, ?, ?, ?)",
                                  (candidate.get_candidate_id(),
                                   candidate.get_first_name(),
                                   candidate.get_last_name(),
                                   candidate.get_role(),
                                   candidate.get_years_experience(),
                                   candidate.get_salary()))
            conn.commit()
        except Error as e:
            raise CandidateDatabaseError(e)
        finally:
            conn.close()

    @staticmethod
    def delete_candidate(candidate_id):
        """
        Deletes a single candidate from the db by id.
        """
        conn = CandidateDAO.__get_connection()
        try:
            conn.cursor().execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
            conn.commit()
        except Error as e:
            raise CandidateDatabaseError(e)
        finally:
            conn.close()

    @staticmethod
    def get_candidate(candidate_id):
        """
        Retrieves a single candidate from the db by id.
        """
        conn = CandidateDAO.__get_connection()
        try:
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
        except Error as e:
            raise CandidateDatabaseError(e)
        finally:
            conn.close()
        return None

    @staticmethod
    def get_all_candidates():
        """
        Retrieves all candidates from the db.
        """
        conn = CandidateDAO.__get_connection()
        try:
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
        except Error as e:
            raise CandidateDatabaseError(e)
        finally:
            conn.close()

    @staticmethod
    def init_db():
        """
        Used to create the db and initialize the schema on startup.
        """
        conn = CandidateDAO.__get_connection()
        with open('dao/schema.sql') as f:
            conn.executescript(f.read())
            conn.commit()
            conn.close()
        f.close()

    @staticmethod
    def __get_connection():
        try:
            return sqlite3.connect('candidates.db')
        except Error as e:
            raise CandidateDatabaseError(e)
