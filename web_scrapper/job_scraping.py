from selenium import webdriver
import json
from datetime import datetime
from get_all_jobs import get_all_jobs_urls
from selenium.webdriver import FirefoxOptions

opts = FirefoxOptions()
opts.add_argument("--headless")
driver = webdriver.Firefox(options=opts)


def find_element_by_xpath(xpath):
    result = ''
    try:
        result = driver.find_element_by_xpath(xpath).text
    except:
        print('Cannot find for xpath: ', xpath)
    return result


def find_element_by_classname(classname):
    result = ''
    try:
        result = driver.find_element_by_class_name(classname).text
    except:
        print('Cannot find for classname: ', classname)
    return result


def scrape_job_listening(url: str):
    print('current url: ', url)
    driver.get(url=url)
    now = datetime.now()
    job_json = {}
    job_json['id'] = url.split('/')[-1]

    salary = driver.find_element_by_class_name("salary")
    if (salary.text.find('B2B') == -1):
        job_json['salary_B2B'] = ''
        job_json['salary_employment_contract'] = salary.text
    else:
        job_json['salary_B2B'] = salary.text
        job_json['salary_employment_contract'] = ''

    job_json['company'] = {
        'name': find_element_by_xpath(
            '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/nfj-posting-header/div/div[2]/a[1]/dl/dd'),
        'link': driver.find_element_by_xpath('//*[@id="postingCompanyUrl"]').get_attribute('href'),
        'size': find_element_by_xpath(
            '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/nfj-posting-header/div/div[2]/a[2]/dl/dd')
    }

    job_json['link'] = url
    job_json['experience_level'] = driver.find_element_by_class_name('seniority-section').find_element_by_class_name('active').text
    job_json['city'] = find_element_by_classname('text-break')
    job_json['position'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/nfj-posting-header/div/div[2]/h1')
    job_json['download_date'] = now.strftime("%d/%m/%Y %H:%M:%S")

    recruitment_language = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/nfj-posting-header/div/div[2]/a[3]/dl/dd')
    job_json['recruitment_language'] = recruitment_language.split(', ')

    job_json['job_profile'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[1]/div[2]')
    job_json['start'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[2]/div[2]')
    job_json['contract_duration'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[3]/div[2]/span')
    job_json['paid_holiday'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[4]/div[2]')
    job_json['part_time_work'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[5]/div[2]')
    job_json['remote_possible'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[6]/div[2]/span')
    job_json['flexible_hours'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[7]/div[2]')
    job_json['travel_involved'] = find_element_by_xpath(
        '/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-posting-details/common-main-loader/section/div[2]/div[1]/nfj-posting-content-wrapper/div[2]/nfj-posting-specs/div[8]/div[2]/span')

    requirements = []
    for x in driver.find_elements_by_id('posting-requirements'):
        for y in x.find_elements_by_tag_name('common-posting-item-tag'):
            requirements.append(y.text)
    job_json['must_have'] = requirements

    nice_to_have = []
    for x in driver.find_elements_by_id('posting-nice-to-have'):
        for y in x.find_elements_by_tag_name('common-posting-item-tag'):
            nice_to_have.append(y.text)
    job_json['nice_to_have'] = nice_to_have

    return job_json

if __name__ == '__main__':
    job_jsons = []
    urls = get_all_jobs_urls()
    print(urls)

    for url in urls:
        job_jsons.append(scrape_job_listening(url))

    now = datetime.now()
    f = open("./jsons/" + now.strftime("%m-%d-%Y_%H-%M-%S") + ".txt", "w+")
    f.write(json.dumps(job_jsons))
    f.close()

    print(job_jsons)
    driver.quit()