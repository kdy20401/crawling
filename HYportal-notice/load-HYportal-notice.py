from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

global i
i = 1
chromeDriverPath = 'C:/Users/SAMSUNG/Desktop/Doug/coding/python/ChromeDriver/chromedriver.exe'
loginUrl = 'https://portal.hanyang.ac.kr/sso/lgin.do'
portalBoardUrl = ('https://portal.hanyang.ac.kr/port.do'
                  '#!UDMwODIwMCRAXiRAXmNvbW0vZ2pzaCRAXk0wMDYyNjMkQF7qs7Xsp4Ds'
                  'gqztla0kQF5NMDAzNzgxJEBeMGJlMjk1OTM2MjY0MjlkZmMzZjFiNjE4MDQ'
                  '1YmM4MTcyYjg2ODMyZGYwZDMzM2JjMGY1ZGI0NzE5OWI5MDI4YQ==')
loginXpath = '//*[@id="hyinContents"]/div[1]/form/div/fieldset/p[3]/a'
l2 = '//*[@id="pagingPanel"]/span[3]/a[1]'
l3 = '//*[@id="pagingPanel"]/span[2]/a[2]'


def waitUntilLoaded(sec, elem, loc):
    try:
        WebDriverWait(driver, sec).until(
            EC.presence_of_element_located((elem, loc)))
    except TimeoutException as e:
        print(e.msg)
        driver.close()


def showNotices(date):
    global i
    html = driver.page_source
    bsObj = BeautifulSoup(html, 'html.parser')

    for noticeRow in bsObj.select('#mainGrid > tbody > tr'):
        writtenDate = noticeRow.select_one('#insertDate').get_text()
        title = noticeRow.select_one('td > #title').get_text()

        if int(writtenDate.replace('.', '')) >= date:
            print('[{}] {} {}'.format(i, writtenDate, title))
            i = i + 1


def login(driver, loginUrl):
    identifier = input("아이디: ")
    password = input('비밀번호: ')
    driver.get(loginUrl)
    driver.find_element_by_xpath(
        '/html/body/div[1]/p').click()  # COVID-19 page
    driver.find_element_by_name('userId').send_keys(identifier)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath(loginXpath).click()


def getDate():
    print("기준날짜 이후의 포털공지를 가져옵니다")
    date = int(input("날짜를 입력하세여(ex: 20.09.01): ").replace('.', '')) + 20000000
    return date


date = getDate()
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chromeDriverPath, options=options)
driver.implicitly_wait(10)
alert = Alert(driver)

# login and access to HYIN portal
login(driver, loginUrl)
alert.dismiss()  # sex-education pop-up

# access to notice page get notices of 3 pages
driver.get(portalBoardUrl)
waitUntilLoaded(10, By.CSS_SELECTOR, '#mainGrid > tbody > tr:nth-child(10)')
showNotices(date)

driver.find_element_by_xpath(l2).click()
waitUntilLoaded(10, By.CSS_SELECTOR, '#mainGrid > tbody > tr:nth-child(10)')
showNotices(date)

driver.find_element_by_xpath(l3).click()
waitUntilLoaded(10, By.CSS_SELECTOR, '#mainGrid > tbody > tr:nth-child(10)')
showNotices(date)

driver.close()

'''
# once set, implicit wait is set for the life of the webdriver object
# alert handles pop-up
# wait docs : https://selenium-python.readthedocs.io/waits.html
'''
