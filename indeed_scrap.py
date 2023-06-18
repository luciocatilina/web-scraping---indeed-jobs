from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup as bs
import os
import re
from datetime import datetime
import pandas as pd
#
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException

#webdriver url

path = os.path.abspath('chromedriver')
#url
url = 'https://www.indeed.com/jobs?q=django&sc=0kf%3Aattr(DSQF7)%3B'

#config webdriver
options = Options()
options.add_argument('--incognito')
options.add_argument('start-maximized')
ser = Service(path)

driver = webdriver.Chrome(service=ser, options=options)
driver.get(url)
start_time = time.time()

data = []

html = driver.page_source
soup = bs(html, features='html.parser')
#list of containers

#data-testid="pagination-page-next

def extract_data():

    try:

        list_container_job = soup.find_all('div', class_= 'job_seen_beacon')
        for container_job in list_container_job:
            descriptions = []

            #job title
            post = []
            a_title_tag = container_job.find('a', class_ = "jcs-JobTitle css-jspxzf eu4oa1w0") # a_title_tag > span_title
            span_title = a_title_tag.find('span')
            title = span_title['title']
            post.append(title)
            id = span_title['id']
            post.append(id)
            #job url    !!pending
            #link = a_title_tag['href']
            #print(link)
            description_container = container_job.find('div', class_ = 'job-snippet')
            li_description = description_container.find_all('li')
            for i in li_description:
                description = i.text
                post.append(description)
            data.append(post)

    except:
        pass
extract_data()
#print(len(data))



#pagination
#i = 0
try:
    while True:#i < 2:
        #i +=1
        extract_data()
        btn_next_page = driver.find_element(By.XPATH, value='//a[@data-testid="pagination-page-next"]')
        time.sleep(3)
        btn_next_page.click()
except Exception as e:
    print(str(e))
    driver.quit()


#print(len(data)) 
#315

#data cleaning
#[0] --> title
#[1:] --> description
filtered_data = []

list_titles = []
list_ids = []
list_description = []


toExclude = ['Staff', 'Senior', 'Lead', 'Sr', 'Anti-Trafficking Software Development Volunteer', 'Middle/Senior']

for job in data:
    included_job = True
    for i in toExclude:
        if i in job[0]:
            included_job = False
            break
    if included_job:
        filtered_data.append(job)

for job in filtered_data:

    list_titles.append(job[0])
    list_ids.append(job[1])
    if len(job[1]) > 1:
        list_description.append(' '.join(list(job[2:])))
    else:
        list_description.append('Sin descripción')



dict_job = {
    'titulo': list_titles,
    'id' : list_ids,
    'descripcion': list_description
    }



df = pd.DataFrame(dict_job)
df.to_csv('ofertas.csv')

print("--- %s seconds ---" % (time.time() - start_time))


'''
try:

    while True:
        
        time.sleep(1)
        #while driver.find_element(By.)

        next_page = driver.find_element(By.CSS_SELECTOR, value='div.css-tvvxwd:nth-child(6) > a:nth-child(1)')

        title_container = driver.find_elements(By.CLASS_NAME, value='jobTitle')

        for i in title_container:
            title_tag = i.find_element(By.CLASS_NAME, value='jcs-JobTitle')
            title = title_tag.get_attribute('aria-label')
            href = title_tag.get_attribute('href')
            data.append([title, href])
            
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located)
        next_page.click()


except:
    print('except')
    pass
driver.quit()

print(len(data))
'''




'''
title_container = driver.find_elements(By.CLASS_NAME, value='jobTitle')

for i in title_container:
    title_tag = i.find_element(By.CLASS_NAME, value='jcs-JobTitle')
    title = title_tag.get_attribute('aria-label')
    href = title_tag.get_attribute('href')
    data.append([title, href])

print(len(data))
'''