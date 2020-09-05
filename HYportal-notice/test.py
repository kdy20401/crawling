import requests
from bs4 import BeautifulSoup

domain = 'http://cs.hanyang.ac.kr'
boards = {'학사일반 게시판': domain + '/board/info_board.php',
          '취업정보 게시판': domain + '/board/job_board.php',
          '졸업작품 게시판': domain + '/board/gradu_board.php',
          '삼성트랙': domain + '/board/trk_board.php',
          '학생게시판': domain + '/board/stu_board.php'}


def showNotices(date, rows):
    i = 1
    for row in rows:
        titleTag = row.find('td', {'class': 'left'})
        writtenDateTag = titleTag.next_sibling.next_sibling.next_sibling.next_sibling
        title = titleTag.get_text().replace('\n', '')
        writtenDate = writtenDateTag.get_text()

        if int(writtenDate.replace('.', '')) >= date:
            print('[{}] {} {}'.format(i, writtenDate, title))
            i = i + 1

    print('')


def loadNotices(boardUrl):
    html = requests.get(boardUrl)
    bsObj = BeautifulSoup(html.text, 'html.parser')
    html.close()
    tbody = bsObj.find('table', {'class': 'bbs_con'}).find('tbody')
    trows = tbody.findAll('tr')

    return trows


def init():

    print("기준날짜 이후의 컴공게시판 공지를 가져옵니다")
    date = int(input("날짜를 입력하세요(ex: 20.09.01): ").replace('.', ''))

    for name, url in boards.items():
        print(name)
        noticeRows = loadNotices(url)
        showNotices(date, noticeRows)


init()
