import uuid

from dao.candidate_dao import CandidateDAO
from model.candidate import Candidate
from service.prediction_service import PredictionService


class CandidateService:

    def __init__(self):
        self.prediction_service = PredictionService()

    @staticmethod
    def get_candidates():
        """
        Retrieves all candidates.
        """
        return CandidateDAO.get_all_candidates()

    @staticmethod
    def get_candidate(candidate_id):
        """
        Retrieves a single candidate by id.
        """
        return CandidateDAO.get_candidate(candidate_id)

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
            CandidateDAO.save_candidate(candidate)
            return candidate_id

    @staticmethod
    def delete_candidates(candidate_ids):
        """
        Deletes multiple candidates by their corresponding ids.
        """
        for candidate_id in candidate_ids:
            CandidateService.delete_candidate(candidate_id)

    @staticmethod
    def delete_candidate(candidate_id):
        """
        Deletes a single candidate by id.
        """
        CandidateDAO.delete_candidate(candidate_id)
