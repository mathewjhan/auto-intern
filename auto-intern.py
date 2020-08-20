from applicant import Applicant
from lever import Auto_Lever
from greenhouse import Auto_Greenhouse
import argparse
import os
import sys

def run():
    if(len(sys.argv) != 3):
        print("Too few/not enough arguments.")
        return

    json = sys.argv[1]
    lever_list = sys.argv[2]

    applicant = Applicant()
    applicant.read_from_json(json)

    auto_lever = Auto_Lever()

    lever_urls = open(lever_list, 'r').readlines()
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
            print(url.strip(), file=lever_failed)

    lever_failed.close()

    # WIP
    # auto_greenhouse = Auto_Greenhouse()
    # auto_greenhouse.load_applicant(applicant)

    # auto_greenhouse.run()



if(__name__ == '__main__'):
    run()
