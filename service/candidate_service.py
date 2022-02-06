import uuid

from model.candidate import Candidate


class CandidateService:

    def __init__(self,
                 candidate_dao=None,
                 prediction_service=None):
        self.candidate_dao = candidate_dao
        self.prediction_service = prediction_service

    def get_candidates(self):
        """
        Retrieves all candidates.
        """
        return self.candidate_dao.get_all_candidates()

    def get_candidate(self, candidate_id):
        """
        Retrieves a single candidate by id.
        """
        return self.candidate_dao.get_candidate(candidate_id)

    def save_candidate(self, first_name, last_name, role, years_experience):
        """
        Saves the candidate and their corresponding salary estimation to the database.
        """
        candidate_id = str(uuid.uuid4())
        salary_prediction = self.prediction_service.get_salary_prediction([years_experience])
        if salary_prediction:
            candidate = Candidate(candidate_id,
                                  first_name,
                                  last_name,
                                  role,
                                  years_experience,
                                  int(salary_prediction[0]),
                                  None)
            self.candidate_dao.save_candidate(candidate)
            return candidate_id

    def delete_candidates(self, candidate_ids):
        """
        Deletes multiple candidates by their corresponding ids.
        """
        for candidate_id in candidate_ids:
            self.delete_candidate(candidate_id)

    def delete_candidate(self, candidate_id):
        """
        Deletes a single candidate by id.
        """
        self.candidate_dao.delete_candidate(candidate_id)
