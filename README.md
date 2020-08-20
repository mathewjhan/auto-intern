# Auto Intern

Automating the internship process

## Features

- Scraping a URL and generating a list of all jobs.lever.co links 
- Automate applying for jobs on Lever
- Ask user for fields that aren't in the json

## Requirements

Python packages can be installed via `pip install -r requirements.txt`. Recommended to use a virtual environment.

## How to use

1. Copy over jsons/template.json and fill out with your information
2. Add your resume to the root directory of the project and name it `resume.pdf`
3. Optionally run `python scrapers/lever_scraper.py` on a website with internship URLs (recommended [this](https://raw.githubusercontent.com/Pitt-CSC/Summer2021-Internships/master/README.md))
4. Run `python auto-intern.py YOUR_JSON.json URL_LIST.txt`

## Platform support

As of now, only Lever works l u l
