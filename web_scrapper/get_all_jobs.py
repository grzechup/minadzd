from selenium import webdriver
from selenium.webdriver import FirefoxOptions

import time


def get_all_jobs_urls():
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=opts)

    driver.get(url="https://nofluffjobs.com/pl/jobs?criteria=machine%20learning")

    urls = []

    try:
        page = 1
        while True:
            print("Current page: ", driver.current_url)
            job_list_elements = driver.find_elements_by_tag_name("nfj-postings-list")

            for job_list_element in job_list_elements:
                job_elements = job_list_element.find_elements_by_css_selector("[nfj-postings-item]")
                for job in job_elements:
                    job_url = job.get_attribute('href')
                    urls.append(job_url)
                    print(job_url)
                    time.sleep(1)

            # time.sleep(2)
            next_button = driver.find_element_by_css_selector("[aria-label=Next]")

            next_button_parent = next_button.find_element_by_xpath('..')
            if next_button_parent.get_attribute("class") == "page-item disabled":
                break

            driver.execute_script("arguments[0].click();", next_button)
            page += 1
    except Exception as e:
        print(e)
    finally:
        driver.quit()

    return urls

