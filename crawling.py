from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import csv

options = webdriver.ChromeOptions()
options.headless = True

browser = webdriver.Chrome(options=options)
browser.get("https://ecampus.kookmin.ac.kr/login/index.php")

check = 0
while(check == 0):
    ID = input("아이디를 입력하세요 : ")
    PW = input("비밀번호를 입력하세요 : ")
    browser.find_element_by_id("input-username").send_keys(ID)
    browser.find_element_by_id("input-password").send_keys(PW, Keys.ENTER)

    try:
        alert = browser.switch_to.alert
        print(alert.text)
        alert.accept()
        # alert.dismiss()
    except:
        check = 1

subjects = browser.find_elements_by_class_name("course-link")
subjects_urls = []
assignment_urls = []

for subject in subjects:
    subjects_urls.append(subject.get_attribute("href"))
for subjects_url in subjects_urls:
    browser.get(subjects_url)
    imgs = browser.find_elements_by_tag_name("img")
    for img in imgs:
        if img.get_attribute('alt') == '과제':
            assignment_urls.append(img.find_element_by_xpath('..').get_attribute('href'))

subject_names = []
dates = []
for assignment_url in assignment_urls:
    browser.get(assignment_url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    subject_name = soup.find('title')
    # print(subject_name.get_text())
    subject_names.append(str(subject_name)[7:-8].replace('&gt;', '-'))
    deadlines = soup.find_all(class_='cell c0')

    for deadline in deadlines:
        if deadline.get_text() == '종료 일시':
            date = deadline.next_sibling.next_sibling
            # print(date.get_text())
            dates.append(date.get_text())

results = []
for i in range(len(dates)):
    temp = []
    temp.append(subject_names[i])
    temp.append(dates[i])
    results.append(temp)

filename = "과제종료일시.csv"
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
for result in results:
    writer.writerow(result)

browser.quit()
