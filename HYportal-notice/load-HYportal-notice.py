from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException

global i, driver, loc
i = 1
driver = None
loc = '#pagingPanel > span.numberLink > a '
chromeDriverPath = 'C:/Users/SAMSUNG/Desktop/Doug/coding/python/ChromeDriver/chromedriver.exe'
loginUrl = 'https://portal.hanyang.ac.kr/sso/lgin.do'
portalBoardUrl = ('https://portal.hanyang.ac.kr/port.do'
                  '#!UDMwODIwMCRAXiRAXmNvbW0vZ2pzaCRAXk0wMDYyNjMkQF7qs7Xsp4Ds'
                  'gqztla0kQF5NMDAzNzgxJEBeMGJlMjk1OTM2MjY0MjlkZmMzZjFiNjE4MDQ'
                  '1YmM4MTcyYjg2ODMyZGYwZDMzM2JjMGY1ZGI0NzE5OWI5MDI4YQ==')
loginXpath = '//*[@id="hyinContents"]/div[1]/form/div/fieldset/p[3]/a'

pageLinks = ['//*[@id="pagingPanel"]/span[3]/a[1]',
             '//*[@id="pagingPanel"]/span[2]/a[2]',
             '//*[@id="pagingPanel"]/span[2]/a[3]',
             '//*[@id="pagingPanel"]/span[2]/a[4]']


def showNotices(date):
    global i
    html = driver.page_source
    bsObj = BeautifulSoup(html, 'html.parser')

    for row in bsObj.select('#mainGrid > tbody > tr'):
        writtenDate = row.select_one('#insertDate').get_text()
        title = row.select_one('td > #title').get_text()

        if int(writtenDate.replace('.', '')) >= date:
            print('[{}] {} {}'.format(i, writtenDate, title))
            i = i + 1


def waitLoading(sec, elem, loc):
    try:
        WebDriverWait(driver, sec).until(
            EC.presence_of_element_located((elem, loc)))
    except TimeoutException as e:
        print(e.msg)
        driver.close()


def waitAndShowNotices(link, date):
    global loc
    driver.find_element_by_xpath(link).click()
    waitLoading(10, By.CSS_SELECTOR, loc + '+ span')
    loc = loc + '+ a '
    showNotices(date)


def handlePopUp():
    alert = Alert(driver)
    alert.dismiss()  # sometimes NoAlertPersentException occurs


def login(loginUrl):
    driver.get(loginUrl)
    driver.find_element_by_xpath(
        '/html/body/div[1]/p').click()  # COVID-19 page

    identifier = input("Id: ")
    password = input('Password: ')
    driver.find_element_by_name('userId').send_keys(identifier)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_xpath(loginXpath).click()

    # handle COVID-19 self-check page and sex education pop-up
    popUpHandled = False
    checked = False
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainForm > div.title.mb-10 > span')))
    except TimeoutException:
        checked = True
    except UnexpectedAlertPresentException:
        checked = True
        popUpHandled = True

    if not checked:
        for num in range(37, 43):
            driver.find_element_by_xpath(
                '//*[@id="c{}_b"]'.format(num)).click()
        driver.find_element_by_xpath('//*[@id="btn_confirm"]').click()

    if not popUpHandled:  # need to be revised
        handlePopUp()


def setDriver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(chromeDriverPath, options=options)
    driver.implicitly_wait(10)
    return driver


def getDate():
    print("기준날짜 이후의 포털공지를 가져옵니다")
    date = int(input("날짜를 입력하세요(ex: 20.09.01): ").replace('.', '')) + 20000000
    return date


def crawl():
    global driver
    date = getDate()
    driver = setDriver()
    login(loginUrl)

    # first page
    driver.get(portalBoardUrl)
    waitLoading(10, By.CSS_SELECTOR,
                '#mainGrid > tbody > tr:nth-child(10)')
    showNotices(date)

    # until 3 pages
    for pageLink in pageLinks[0:2]:
        waitAndShowNotices(pageLink, date)

    driver.close()


crawl()


'''
# once set, implicit wait is set for the life of the webdriver object
# alert handles pop-up
# wait docs : https://selenium-python.readthedocs.io/waits.html
'''
