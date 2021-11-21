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
while check == 0:
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
video_names = []
video_deadlines = []
video_check = []
assignment_subjects = []
assignment_names = []
assignment_deadlines = []
assignment_check = []

# 과목 url
subjects = browser.find_elements_by_class_name("course-link")
for subject in subjects:
    subjects_urls.append(subject.get_attribute("href"))
for subjects_url in subjects_urls:
    browser.get(subjects_url)

    # 동영상
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 동영상 종료 일시
    deadlines = soup.find_all(class_='text-time mr-1')
    for deadline in deadlines:
        video_deadlines.append(deadline.get_text()[-19:])

        # 동영상 과목명
        video_subject = soup.find('title')
        video_subjects.append(str(video_subject)[7:-8].split('(')[0])

        # 동영상 체크, 동영상 이름
        yes = deadline.parent.parent.next_sibling.find("span", attrs={
            "class":"badge badge-completion badge-completion-auto-y"})
        no = deadline.parent.parent.next_sibling.find("span", attrs={
            "class": "badge badge-completion badge-completion-auto-n"})
        if yes:
            video_names.append(yes['title'][5:])
            video_check.append('yes')
        elif no:
            video_names.append(no['title'][9:])
            video_check.append('no')

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
    assignment_subjects.append(str(assignment_subject)[7:-8].split('&gt;')[0].split('(')[0])
    assignment_names.append(str(assignment_subject)[7:-8].split('&gt;')[1])

    # 과제 종료 일시
    deadlines = soup.find_all(class_='cell c0')
    for deadline in deadlines:
        if deadline.get_text() == '종료 일시':
            assignment_deadline = deadline.next_sibling.next_sibling
            assignment_deadlines.append(assignment_deadline.get_text())

    # 과제 체크
    yes = soup.find_all(class_='submissionstatussubmitted cell c1 lastcol')
    no = soup.find_all(class_='cell c1 lastcol')
    if yes:
        assignment_check.append('yes')
    elif no:
        assignment_check.append('no')

# 데이터 저장
results = []
for i in range(len(assignment_deadlines)):
    temp = []
    temp.append(assignment_subjects[i])
    temp.append(assignment_names[i])
    temp.append(assignment_deadlines[i])
    temp.append(assignment_check[i])
    results.append(temp)
for i in range(len(video_deadlines)):
    temp = []
    temp.append(video_subjects[i])
    temp.append(video_names[i])
    temp.append(video_deadlines[i])
    temp.append(video_check[i])
    results.append(temp)

filename = "종료일시.csv"
f = open(filename, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f)
for result in results:
    writer.writerow(result)

browser.quit()
