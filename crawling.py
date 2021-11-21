from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import csv

options = webdriver.ChromeOptions()
options.headless = True

browser = webdriver.Chrome(options=options)
browser.get("https://ecampus.kookmin.ac.kr/login/index.php")

# 로그인
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

subjects_urls = []
assignment_urls = []
video_subjects = []
video_deadlines = []
assignment_subjects = []
assignment_deadlines = []

# 과목 url
subjects = browser.find_elements_by_class_name("course-link")
for subject in subjects:
    subjects_urls.append(subject.get_attribute("href"))
for subjects_url in subjects_urls:
    browser.get(subjects_url)

    # 동영상 종료 일시
    span = browser.find_elements_by_tag_name("span")
    for video_deadline in span:
        if video_deadline.get_attribute("class") == "text-time mr-1":
            video_deadlines.append(video_deadline.text)
            
            # 동영상 과목명
            metas = browser.find_elements_by_tag_name("meta")
            for meta in metas:
                if meta.get_attribute("property") == "og:title":
                    video_subjects.append(meta.get_attribute("content"))

    # 과제 url
    imgs = browser.find_elements_by_tag_name("img")
    for img in imgs:
        if img.get_attribute('alt') == '과제':
            assignment_urls.append(img.find_element_by_xpath('..').get_attribute('href'))

for assignment_url in assignment_urls:
    browser.get(assignment_url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 과제 과목명
    assignment_subject = soup.find('title')
    assignment_subjects.append(str(assignment_subject)[7:-8].replace('&gt;', '-'))
    
    # 과제 종료 일시
    deadlines = soup.find_all(class_='cell c0')
    for deadline in deadlines:
        if deadline.get_text() == '종료 일시':
            assignment_deadline = deadline.next_sibling.next_sibling
            assignment_deadlines.append(assignment_deadline.get_text())

# 데이터 저장
results = []
for i in range(len(assignment_deadlines)):
    temp = []
    temp.append(assignment_subjects[i])
    temp.append(assignment_deadlines[i])
    results.append(temp)
for i in range(len(video_deadlines)):
    temp = []
    temp.append(video_subjects[i])
    temp.append(video_deadlines[i])
    results.append(temp)

filename = "종료일시.csv"
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
for result in results:
    writer.writerow(result)

browser.quit()
