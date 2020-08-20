from applicant import Applicant
from lever import Auto_Lever
from greenhouse import Auto_Greenhouse
import os

def run():
    applicant = Applicant()
    applicant.read_from_json('jsons' + os.sep + 'person.json')

    auto_lever = Auto_Lever()

    lever_urls = open('lists' + os.sep + 'lever.txt', 'r').readlines()
    lever_failed = open('failed' + os.sep + 'lever_failed.txt', 'w')

    for url in lever_urls:
        auto_lever.load_url(url)
        auto_lever.load_applicant(applicant)

        try:
            response = auto_lever.run()

            if(response != 'success'):
                print(response, file=lever_failed)
            print()
        except:
            print("Oops! Something went wrong. Skipping URL...")
            print(url, file=lever_failed)

    lever_failed.close()

    # WIP
    # auto_greenhouse = Auto_Greenhouse()
    # auto_greenhouse.load_applicant(applicant)

    # auto_greenhouse.run()



if(__name__ == '__main__'):
    run()
