import json

class Applicant:
    def __init__(self):
        self.info = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone": "",
            "org": "",
            "resume": "",
            "resume_textfile": "",
            "linkedin": "",
            "website": "",
            "github": "",
            "twitter": "",
            "location": "",
            "grad_month": "",
            "grad_year": "",
            "school": "",
            "city": "",
            "state": ""
        }

    def read_from_json(self, filename):
        with open(filename) as json_file:
            self.info = json.load(json_file)

