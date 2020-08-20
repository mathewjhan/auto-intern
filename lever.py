import mechanize
import difflib
import datetime
from bs4 import BeautifulSoup
import requests

class Auto_Lever:
    def __init__(self):
        self.applicant = None
        self.url = ""
        self.headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }

    def load_applicant(self, applicant):
        self.applicant = applicant

    def load_url(self, url):
        self.url = url.strip()

        # Format to apply url
        if(not url.endswith("/")):
            self.url += "/"

        if("apply" not in url[-10:]):
            self.url += "apply"

    def select_form(self, form):
        return form.attrs.get('enctype', None) == 'multipart/form-data'

    def anyInvalidStringInts(self, all_choices, num_choices):
        for choice in all_choices:
            if(not choice.isdigit() or int(choice) >= num_choices):
                return False
        return True

    def run(self):
        req = requests.get(self.url, self.headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        br = mechanize.Browser()
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        br.set_handle_equiv(False)

        br.open(self.url)
        br.select_form(predicate=self.select_form)
        br.form.set_all_readonly(False)

        print("URL: " + self.url)

        # Resume
        br.form.add_file(open(self.applicant.info["resume"], "rb"), filename="resume.pdf", name='resume')

        # Personal info
        br.form["name"] = "%s %s" %(self.applicant.info["first_name"].capitalize(), self.applicant.info["last_name"].capitalize())
        br.form["email"] = self.applicant.info["email"]
        br.form["phone"] = self.applicant.info["phone"]
        br.form["org"] = self.applicant.info["org"]

        # School, selections, and signatures
        for control in br.form.controls:
            if(control.type == "text"):
                name_lower = control.name.lower()
                # Signature
                if("signature" in name_lower):
                   control.value = "%s %s" %(self.applicant.info["first_name"].capitalize(), self.applicant.info["last_name"].capitalize())
                if("date" in name_lower):
                    control.value = datetime.datetime.now().strftime("%m/%d/%Y")

                # Websites
                if("linkedin" in name_lower):
                    control.value = self.applicant.info["linkedin"]
                if("twitter" in name_lower):
                    control.value = self.applicant.info["twitter"]
                if("github" in name_lower):
                    control.value = self.applicant.info["github"]
                if("portfolio" in name_lower):
                    control.value = self.applicant.info["website"]

                if(control.value == ""):
                    try:
                        field = soup.find('input', { 'name': control.name })
                        grandparent = field.find_parent('div').find_parent('label')
                        text = grandparent.find('div', { 'class': 'text' }).text
                        print(text)
                    except:
                        pass

                    print(control.name)
                    choice = input("Possibly required field, please type a response (or leave empty if unreadable/not required): ")
                    control.value = choice
                    print()

            if(control.type == "checkbox"):
                print("checkbox", control.name.lower())
                try:
                    field = soup.find('input', { 'name': control.name })
                    grandparent = field.find_parent('div').find_parent('label')
                    text = grandparent.find('div', { 'class': 'text' }).text
                    print(text)
                except:
                    pass

                options = [item.attrs['value'] for item in control.items]
                for option in enumerate(options):
                    print(str(option[0]) + ": " + option[1])

                choices = input("Possibly required field, please select a numbers deliminated by space (or 0 if sure not required): ")
                all_choices = choices.strip().split(" ")

                while(not self.anyInvalidStringInts(all_choices, len(options))):
                    choices = input("Please enter a valid set of numbers: ")
                    all_choices = choices.strip().split(" ")

                control.value = map(lambda c : control.items[int(c)].name, all_choices)
                print()

            if(control.type == "radio"):
                try:
                    field = soup.find('input', { 'name': control.name })
                    grandparent = field.find_parent('div').find_parent('label')
                    text = grandparent.find('div', { 'class': 'text' }).text
                    print(text)
                except:
                    pass

                print("radio", control.name)
                options = [item.attrs['value'] for item in control.items]

                for option in enumerate(options):
                    print(str(option[0]) + ": " + option[1])

                choice = input("Possibly required field, please select a number (or 0 if sure not required): ")
                while(not choice.isdigit() or int(choice) >= len(options)):
                    choice = input("Please enter a valid number: ")
                control.value = [control.items[int(choice)].name]
                print()

            if(control.type == "textarea"):
                try:
                    textarea = soup.find('textarea', { 'name': control.name })
                    grandparent = textarea.find_parent('div').find_parent('label')
                    text = grandparent.find('div', { 'class': 'text' }).text
                    print(text)
                except:
                    pass

                if(control.value == ""):
                    print(control.name)
                    choice = input("Possibly required field, please type a response (or leave empty if unreadable/not required): ")
                    control.value = choice
                print()

            if(control.type == "select"):
                name_lower = control.name.lower()

                # School
                if("field0" in name_lower):
                    options = [item.attrs['value'].lower() for item in control.items]

                    if any("harvard" in s for s in options):
                        school = self.applicant.info["university"]
                        temp = list(map(lambda a : a.name, control.items))
                        control.value = [difflib.get_close_matches(school, temp)[0]]
                        print()

                    elif any("united arab emirates" in s for s in options):
                        country = self.applicant.info["country"]
                        temp = list(map(lambda a : a.name, control.items))
                        control.value = [difflib.get_close_matches(country, temp)[0]]
                        print()


                # Below are optional fields
                if("gender" in name_lower):
                    gender = self.applicant.info["gender"].lower()
                    if(gender == "male"):
                        control.value = [control.items[1].name]
                    elif(gender == "female"):
                        control.value = [control.items[2].name]
                    else:
                        control.value = [control.items[3].name]

                if("race" in name_lower):
                    race = self.applicant.info["race"].lower()
                    if("hispanic" in race or "latino" in race):
                        control.value = [control.items[1].name]
                    elif("white" in race):
                        control.value = [control.items[2].name]
                    elif("black" in race or "african" in race):
                        control.value = [control.items[3].name]
                    elif("hawaiian" in race or "pacific" in race or "islander" in race):
                        control.value = [control.items[4].name]
                    elif("asian" in race):
                        control.value = [control.items[5].name]
                    elif("indian" in race or "alaska" in race):
                        control.value = [control.items[6].name]
                    elif("two" in race):
                        control.value = [control.items[7].name]
                    else:
                        control.value = [control.items[8].name]

                if("veteran" in name_lower):
                    veteran_status = self.applicant.info["veteran"].lower()
                    if(veteran_status == "yes"):
                        control.value = [control.items[1].name]
                    elif(veteran_status == "no"):
                        control.value = [control.items[2].name]
                    else:
                        control.value = [control.items[3].name]

                if(control.value == [control.items[0].name]):
                    try:
                        select = soup.find('select', { 'name': control.name })
                        grandparent = select.find_parent('div').find_parent('label')
                        text = grandparent.find('div', { 'class': 'text' }).text
                        print(text)
                    except:
                        pass

                    options = [item.attrs['value'] for item in control.items]
                    for option in enumerate(options):
                        print(str(option[0]) + ": " + option[1])
                    choice = input("Possibly required field, please select a number (or 0 if sure not required): ")
                    while(not choice.isdigit() or int(choice) >= len(options)):
                        choice = input("Please enter a valid number: ")
                    control.value = [control.items[int(choice)].name]
                    print()

        # Submit completed form
        try:
            response = br.submit()
        except:
            print("Unable to submit to: " + self.url)
            return self.url


        # Check for success
        response_url = response.geturl()
        if("thanks" in response_url or "received" in response_url):
            print("Submitted to: " + self.url)
            return "success"

        print("Unable to submit to: " + self.url)
        return self.url








