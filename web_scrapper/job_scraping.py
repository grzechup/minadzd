from selenium import webdriver


def scrape_job_listening(url: str):
    driver = webdriver.Firefox()

    driver.get(url=url)

    salary = driver.find_element_by_class_name("salary")
    print(salary.text)

    salary_amount = salary.find_element_by_tag_name('h4')
    salary_type = salary.find_element_by_class_name('type')
    print(salary_amount.text, salary_type.text)

    driver.quit()


if __name__=='__main__':
    scrape_job_listening("https://nofluffjobs.com/pl/job/magento-2-developer-solteq-poland-wroclaw-fod5wfms")