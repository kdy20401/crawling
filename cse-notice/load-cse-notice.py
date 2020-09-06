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
        title = row.select_one('td.left > a').get_text()
        writtenDate = row.select_one('td:nth-child(5)').get_text()
        if int(writtenDate.replace('.', '')) >= date:
            print('[{}] {} {}'.format(i, writtenDate, title))
            i = i + 1

    print('')


def loadNotices(boardUrl):
    res = requests.get(boardUrl)
    bsObj = BeautifulSoup(res.text, 'html.parser')
    res.close()
    trows = bsObj.select('#content_box > div > table > tbody > tr')
    return trows


def crawl():

    print("기준 날짜 이후의 컴소 홈페이지 공지사항들을 불러옵니다")
    date = int(input("날짜를 입력하세요(ex: 20.09.01): ").replace('.', ''))

    for name, url in boards.items():
        print(name)
        noticeRows = loadNotices(url)
        showNotices(date, noticeRows)


crawl()
