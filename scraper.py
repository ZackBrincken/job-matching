# OVERVIEW ====================================================================================================================================================================
'''
scraper.py scrapes computer science job listings in the St. Louis, MO area from indeed.com using Selenium 4.33.0, Undetected ChromeDriver 3.5.5, and Google Chrome on 
a Windows machine.

Disclaimer:
This scraper may not be used for any purposes other than the one described in this overview and no user-favoring modifications shall be made to the delays in place.
Since Indeed's terms of service (TOS) explicitly prohibits the unauthorized scraping of data for commercial use, it is fair to assume scraping is generally not appreciated. 
Whether this is to keep their services exclusive or simply to reduce server lag, it is important to take their TOS into account. So, since the project requirements call for data 
from a high-profile job listings website (all of which prohibit scraping), there are slowdown functions (sleep, small_sleep, and tiny_sleep) implemented in various locations to 
reduce the load on the server. Additionally, this data will be used strictly for the academic purpose of designing this project, so no commercial gain will EVER be involved.
'''
# =============================================================================================================================================================================





# IMPORTS ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

from selenium.webdriver.common.by import By                     # for finding elements by an html attribute
from selenium.webdriver.support import expected_conditions      # for waiting on html elements to load before acting
from selenium.webdriver.support.ui import WebDriverWait         # for enforces the wait time before giving up
import undetected_chromedriver                                  # for easy scraping without being blacklisted
import time, random                                             # for sleep functions

import json                                                     # for writing scraped data to a jsonl file (one object per job)

from job.job_module import Job                                  # for storing job data as Job objects and easy printing (for testing)

#  --------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# CONSTANT DEFINTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------

MAX_PAGES = 50  # the maximum number of pages which can be loaded before exiting the program (in case of some error that causes indefinite/unexpected runtime)

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------





# SLEEP FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------------------------------

# a moderate sleep time for giving servers a break or waiting for pages to load
def sleep() -> None:
    time.sleep(random.uniform(8, 12))

# a small sleep time for waiting on job elements to load after clicking on a job card
def small_sleep() -> None:
    time.sleep(random.uniform(2, 4))

# a very small sleep used for spin-waiting while the user is interacting with the site (logging in, navigating, etc. manually)
def tiny_sleep() -> None:
    time.sleep(0.2)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------






# OTHER FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------

# retrieves the text contained within an element by xpath -- times out after 3 seconds (element likely not loading properly)
def retrieve_element_text(driver, xpath: str, timeout: int = 3, default: str = "Not Listed"):
    try:
        return WebDriverWait(driver, timeout).until(expected_conditions.presence_of_element_located((By.XPATH, xpath))).text
    except:
        return default
    
# retrieves the title, company, location, and full description for a job card and returns this information as a job object
def retrieve_job(driver) -> Job:
        title = retrieve_element_text(driver, "//*[@data-testid='jobsearch-JobInfoHeader-title']/span[1]")
        title = title.removesuffix("\n- job post")

        company = retrieve_element_text(driver, "//*[@data-testid='inlineHeader-companyName']")

        location = retrieve_element_text(driver, "//*[@data-testid='inlineHeader-companyLocation']")

        full_description = retrieve_element_text(driver, "//*[@id='jobDescriptionText']")

        return Job(title, company, location, full_description)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------





# MAIN ===================================================================================================================================================================

if __name__ == "__main__":

# INITIALIZE DRIVER ------------------------------------------------------------------------------------------------------------------------------------------------------

    options = undetected_chromedriver.ChromeOptions()               # sets the options undetected-chromedriver will start with

    options.add_argument("--window-size=1960,1080")                 # makes automation harder to detect (apparently)

    driver = undetected_chromedriver.Chrome(options=options)        # creates the driver which will be used to browse the web

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------





# ALLOW USER TO LOG IN (REQUIRED) ---------------------------------------------------------------------------------------------------------------------------------------

    driver.get("https://www.indeed.com")        # bring the user to indeed (the site to be scraped)

    sleep()     # initial sleep while logging in

    while (driver.current_url != "https://onboarding.indeed.com/onboarding/location"):      # wait for the user to finish logging in manually if needed
        tiny_sleep()

    driver.get("https://www.indeed.com/jobs?q=computer+science&l=St.+Louis%2C+MO")          # once the user is logged in, redirect to computer science jobs in St. Louis, MO

    sleep()     # initial sleep while site is loading and user is completing human verification

    while ("https://www.indeed.com/jobs?q=computer+science&l=St.+Louis%2C+MO" not in driver.current_url):   # additional sleep if needed
        tiny_sleep()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------





# SCRAPE EACH JOB (BY CARD) ---------------------------------------------------------------------------------------------------------------------------------------------

    job_count = 0       # counts number of jobs scraped for debugging purposes
    seen = set()        # maintains a set of all jobs that have been seen in case duplicates are loaded

    with open("jobs.jsonl", "w", encoding="UTF-8") as fout:     # opens the jsonl that each job will be written to

        # go through a maximum of MAX_PAGES to ensure non-infinite scraping and that the program will eventually stop if there is a bug
        for page in range(MAX_PAGES):

            try:
                # wait for all cards on the screen to load (max 10 seconds), then store them all in cards
                cards = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, "resultContent")))

                for card in cards:

                    # ensure card has not already been seen -- if it has, continue, if not, add it to seen
                    card_text = card.text
                    if card_text in seen:
                        continue
                    seen.add(card_text)

                    try:
                        # load the job data by clicking the card and sleep to allow the content to load
                        card.click()
                        small_sleep()
                        
                        # retrieve the job from the card and dump the attributes of the Job object as a single json object in the jsonl file
                        json.dump(retrieve_job(driver).__dict__, fout)
                        fout.write("\n")

                        job_count += 1      # track number of jobs for debugging

                    except Exception as e:
                        print(f"Failed on page {page}, job {job_count}. Skipped job.")
                        print(f"Error: {e}")

                # if the next_page element exists and is enabled, go to the next page, else there are no more pages -> break out of loop
                next_page = driver.find_element(By.XPATH, "//*[contains(@data-testid, 'pagination-page-next')]")
                if next_page and next_page.is_enabled():
                    next_page.click()
                    sleep()     # moderate sleep to allow site to load and lessen site traffic
                else:
                    break

            except Exception as e:

                print(f"Failed on page {page}.")
                print(f"Error: {e}")

    driver.quit()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# END MAIN ============================================================================================================================================================