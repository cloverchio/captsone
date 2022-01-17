class Candidate:

    def __init__(self,
                 candidate_id=None,
                 first_name=None,
                 last_name=None,
                 role=None,
                 years_experience=None,
                 salary=None,
                 created_on=None):
        self.candidate_id = candidate_id
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.years_experience = years_experience
        self.salary = salary
        self.created_on = created_on

    def get_candidate_id(self):
        return self.candidate_id

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_role(self):
        return self.role

    def get_years_experience(self):
        return self.years_experience

    def get_salary(self):
        return self.salary

    def get_created_on(self):
        return self.created_on

    def get_salary_str(self):
        return "${:,.2f}".format(self.salary)

    def __str__(self):
        return self.first_name + ' ' + \
               self.last_name + ' ' + \
               self.role + ' ' + \
               str(self.years_experience) + ' ' + \
               str(self.salary)
