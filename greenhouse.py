from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import os
import time
import random

class Auto_Greenhouse:
    def __init__(self):
        self.applicant = None
        self.url = "https://boards.greenhouse.io/lightstep/jobs/873368#app"

    def load_applicant(self, applicant):
        self.applicant = applicant

    def load_url(self, url):
        self.url = url

        # Format to apply url
        if(url.endswith("/")):
            self.url = self.url[:-1]

        if("apply" not in url[-10:]):
            self.url += "#app"

    def select_form_main(self, form):
        return form.attrs.get('enctype', None) == 'multipart/form-data'

    def select_form_aws(self, form):
        return form.attrs.get('id', None) == 's3_upload_for_resume'

    def smooth_scroll(self, driver, length):
        for i in range(length):
            driver.execute_script("window.scrollBy(0,1)", "")

    def run(self):
        options = Options()
        #ua = UserAgent()
        #user_agent = ua.random
        #options.add_argument(f'user-agent={user_agent}')


        driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
        #driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
        actions = ActionChains(driver)
        info = self.applicant.info

        time.sleep(random.uniform(3, 7))
        driver.get(self.url)

        first_name = driver.find_element_by_id('first_name')
        first_name.send_keys(info['first_name'])

        last_name = driver.find_element_by_id('last_name')
        last_name.send_keys(info['last_name'])

        email = driver.find_element_by_id('email')
        email.send_keys(info['email'])

        phone = driver.find_element_by_id('phone')
        phone.send_keys(info['phone'])

        # Location
        # The location menu requires you to actually click the dropdown, so we
        # have to work around that by finding the dropdown elements.
        # We wait until the dropdown appears and then click the div.
        try:
            location = driver.find_element_by_id('job_application_location')
            location.send_keys(info['city'].capitalize() + ", " + info["state"].capitalize())
            autocomplete = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, 'ui-id-1')))
            autocomplete_li = autocomplete.find_element_by_tag_name('li')
            autocomplete_div = autocomplete_li.find_element_by_tag_name('div')
            autocomplete_div.click()
        except NoSuchElementException:
            pass

        # Upload resume
        # Greenhouse.io uses another form to upload the resume, making it hard to submit a single form.
        # Instead, we use webdriver to input the resume so we can submit the form
        try:
            resume_div = driver.find_element_by_id('s3_upload_for_resume')
            resume_input = resume_div.find_element_by_xpath("//form[@id='s3_upload_for_resume']//input[@name='file']")
            resume_input.send_keys(os.getcwd()+"/resume.pdf")
            resume_input.click()
        except StaleElementReferenceException:
            pass

        # Websites/Linkedin
        try:
            linkedin = driver.find_element_by_xpath("//label[contains(.,'LinkedIn')]")
            linkedin.send_keys(info['linkedin'])
        except NoSuchElementException:
            pass
        try:
            driver.find_element_by_xpath("//label[contains(.,'Website')]").send_keys(info['website'])
        except NoSuchElementException:
            pass

        # Occasionally this field is required ("How did you hear about this job?")
        try:
            driver.find_element_by_xpath("//label[contains(.,'hear about')]").send_keys("Job board")
        except NoSuchElementException:
            pass

        time.sleep(random.uniform(3, 5))
        submit = driver.find_element_by_id("submit_app")
        submit.click()
        time.sleep(20)
        #print(response_url)
        #if("thanks" in response_url):
        #    print("success")








