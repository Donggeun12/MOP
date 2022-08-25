from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json, requests
from time import sleep
import os

MAX_PK = 1
ESTIMATE_TIME = 1

token = 'secret_SW5UqOsIhwzwkLsrD5PcjSutEvfTf8J1r08lGmi2BP0'

class Db:
    def __init__(self):
        self.pk, self.id, self.dbid = '', '', ''
        self.headers = {
            'Authorization' : 'Bearer ' + token,
            'Notion-Version' : '2022-02-22',
            'content-Type' : 'application/json'
        }
        self.json = {}

    # null -> bool, 해당 Db class object가 Notion Db에 존재하는지 확인, 만약 존재하면 self.id 설정
    def exists(self):
        pass

    # null -> json object, Notion Db에서 response json 가져오기, 만약 exist 하지 않으면 raise
    def getJson(self):
        pass
    
    # null -> null, Notion Db에 Db member var 등록
    def create(self):
        pass

    def patch(self):
        pass

    def delete(self):
        pass

class Post(Db):
    # 생성시 DB에 있는지 확인, 없다면 신규 생성. 
    def __init__(self, title, pk, writer, dept, date, keyword, page):
        super().__init__()
        # pk|Int, title|Str, writer|Writer, dept|Dept, date|Str, keyword|[Str], page|Page
        self.pk, self.title, self.writer, self.dept, self.date, self.page = pk, title, writer, dept, date, page
        self.keyword = []
        for word in keyword:
            self.keyword.append(word)
        self.dbid = '2efb52f6c2714f25983ddc1a8d6a4069'
        if not self.exists():
            self.create()
        self.json = self.getJson()

    def exists(self):
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "pk",
                    "number": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "pk",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res['results'].__len__() > 0:
            self.id = res["results"][0]["id"]
            return True
        else:
            return False

    def getJson(self):
        if not self.exists():
            raise
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "pk",
                    "number": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "pk",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        return res

    def create(self):
        headers = {
            'Authorization' : 'Bearer ' + token,
            'Notion-Version' : '2022-02-22',
            'content-Type' : 'application/json'
        }
        reqUrl = 'https://api.notion.com/v1/pages'
        body = {
            "parent": {
                "database_id": self.dbid
                },
            "properties": {
                "dept": {
                    "id": "ETFM",
                    "type": "relation",
                    "relation": [{ "id": self.dept.getJson()["id"] }]
                },
                "date": {
                    "id": "Ff%3F%5E",
                    "type": "date",
                    "date": {
                        "start": self.date,
                        "end": None,
                        "time_zone": None
                    }
                },
                "page": {
                    "id": "%5DNRS",
                    "type": "relation",
                    "relation": [{ "id": self.page.getJson()["id"] }]
                },
                "keyword": {
                    "id": "dGL%3B",
                    "type": "multi_select",
                    "multi_select": self.keyword
                },
                "pk": {
                    "id": "iV%3Ez",
                    "type": "number",
                    "number": self.pk
                },
                "writer": {
                    "id": "nFNs",
                    "type": "relation",
                    "relation": [{ "id": self.writer.getJson()["id"] }]
                },
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                        "type": "text",
                        "text": { "content": f"{self.title}", "link": None },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": f"{self.title}",
                        "href": None
                        }
                    ]
                }
            }
        }
        try:
            res = requests.post(url=reqUrl, headers=headers, json=body)
            js = res.json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res.status_code != 200:
            print("There has something wrong")

        with open('./Post_db_create.json', 'w', encoding='utf8') as f:
            json.dump(res.json(), f, ensure_ascii=False)

        return js

class Writer(Db):
    def __init__(self, name, dept, num, email):
        super().__init__()
        self.pk, self.dept, self.num, self.email = name, dept, num, email
        self.dbid = 'e709ad3627274a918990d28d69b62afe'

    def exists(self):
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "name",
                    "title": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "name",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res['results'].__len__() > 0:
            self.id = res["results"][0]["id"]
            return True
        else:
            return False
    
    def getJson(self):
        if not self.exists():
            raise
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "name",
                    "title": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "name",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        return res
    
    def create(self):
        headers = {
            'Authorization' : 'Bearer ' + token,
            'Notion-Version' : '2022-02-22',
            'content-Type' : 'application/json'
        }
        reqUrl = 'https://api.notion.com/v1/pages'
        body = {
            "parent": {
                "database_id": self.dbid
                },
            "properties": {
                "num": {
                    "id": "%3CZnA",
                    "type": "number",
                    "number": self.num
                },
                "email": {
                    "id": "cT%60g",
                    "type": "rich_text",
                    "rich_text": self.email
                },
                "dept": {
                    "id": "cc%3Fv",
                    "type": "relation",
                    "relation": [
                        {
                            "id": self.dept.getJson()["id"]
                        }
                    ]
                },
                "name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": self.pk,
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": self.pk,
                            "href": None
                        }
                    ]
                }
            }
        }
        try:
            res = requests.post(url=reqUrl, headers=headers, json=body)
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res.status_code != 200:
            print("There has something wrong in Writer searching")

        with open('./Post_db_create.json', 'w', encoding='utf8') as f:
            json.dump(res.json(), f, ensure_ascii=False)

        return res.json()

class Dept(Db):
    def __init__(self, name):
        super().__init__()
        self.pk = name
        self.dbid = 'c798b3628f7843afbf906884c105a9d6'

    def exists(self):
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "name",
                    "title": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "name",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res['results'].__len__() > 0:
            self.id = res["results"][0]["id"]
            return True
        else:
            return False

    def getJson(self):
        if not self.exists():
            raise
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "name",
                    "title": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "name",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        return res

    def create(self):
        headers = {
            'Authorization' : 'Bearer ' + token,
            'Notion-Version' : '2022-02-22',
            'content-Type' : 'application/json'
        }
        reqUrl = 'https://api.notion.com/v1/pages'
        body = {
            "parent": {
                "database_id": self.dbid
                },
            "properties": {
                "name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": self.pk,
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "홍보팀",
                            "href": None
                        }
                    ]
                }
            }
        }
        try:
            res = requests.post(url=reqUrl, headers=headers, json=body)
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res.status_code != 200:
            print("There has something wrong in Writer searching")

        with open('./Post_db_create.json', 'w', encoding='utf8') as f:
            json.dump(res.json(), f, ensure_ascii=False)

        return res.json()
        
class Page(Db):
    def __init__(self, name):
        super().__init__()
        self.pk = name
        self.dbid = '7e4e1dff65154ffa8a2aeff3d225b1f5'
    
    def exists(self):
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "pk",
                    "number": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "pk",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res['results'].__len__() > 0:
            self.id = res["results"][0]["id"]
            return True
        else:
            return False

    def getJson(self):
        if not self.exists():
            raise
        readUrl = f'https://api.notion.com/v1/databases/{self.dbid}/query'
        body = {
        "filter": {
            "and":[
                {
                    "property": "name",
                    "title": {
                        "equals": self.pk
                    }
                }
            ]
        },
        "sorts": [
            {
                "property": "name",
                "direction": "ascending"
            }
        ]
        }
        try:
            res = requests.post(readUrl, headers=self.headers, json=body).json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        return res

    def create(self):
        reqUrl = 'https://api.notion.com/v1/databases'
        body = {
            "parent": {
                "type": "page_id",
                "page_id": "2efb52f6-c271-4f25-983d-dc1a8d6a4069"
            },
            "icon": None,
            "cover": None,
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": "Post",
                        "link": None
                    }
                }
            ],
            "properties": {
                "name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": self.pk,
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "Portal",
                            "href": None
                        }
                    ]
                }
            }
        }
        try:
            res = requests.post(url=reqUrl, headers=self.headers, json=body)
            js = res.json()
        except requests.exceptions.HTTPError as herr:
            print("HTTP error occured : ", herr)
        
        if res.status_code != 200:
            print("There has something wrong")
        return js


def PortalCrowling():
    driver = webdriver.Chrome('/Users/yoon.jh/Desktop/MOP_project/chromedriver')

    driver.implicitly_wait(3)
    driver.get('https://portal.gist.ac.kr/login.jsp')

    while driver.current_url == 'https://portal.gist.ac.kr/login.jsp':
        try:
            alert = driver.switch_to.alert
            alert.accept()
        except:
            pass
        idBox, pwBox = driver.find_element_by_name('user_id'), driver.find_element_by_name('user_password')
        idBox.clear()
        pwBox.clear()
        idBox.send_keys('ysa5347')
        pwBox.send_keys('jinhyun@@99')
        sleep(1)
        driver.find_element_by_class_name('btn_login').click()
        
    
    title, dept, writer, date, pk, keywords = [], [], [], [], [], []
    driver.execute_script('window.open("https://portal.gist.ac.kr/p/EXT_LNK_BRD/?boardId=1");')

    page = 1
    # 1 ~ 10 페이지 탐색
    while(page):
        print(f'_____________for {page} in 10_______________')
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.frame("body_frame")
        sleep(1)
        
        # 각 항목 parsing 및 Data화
        html = driver.page_source
        soup = bs(html, 'html.parser') # BeautifulSoup parsing
        
        # 한 페이지 속 20개의 게시글 탐색
        for column in range(20):
            _title = soup.select('tbody > tr > td.bc-s-txtval > div > span')[column].text
            _dept = soup.select('tbody > tr > td.bc-s-cre_user_dept_name')[column].text
            _writer = soup.select('tbody > tr > td.bc-s-cre_user_name')[column].text
            _date = soup.select('tbody > tr > td.bc-s-cre_dt')[column].text
            _pk = int(soup.select('tbody > tr')[column].attrs['data-url'].split('=')[-1])

            print(f'-------for {column + 1} in 20 --------')
            
            # 게시글이 존재하지 않는다면( _pk not in postCollection.CollectionQuery. )
            if not searchPost(_title):
                print("---------------Post is not in DB------------------")
                title.append(_title)
                dept.append(_dept)
                writer.append(_writer)
                date.append(_date)
                pk.append(_pk)

                # dept 존재 유무 판별
                if not "_dept not in deptCollection":
                    print('_______dept is not in deptCollection______')
                    
                    
                # writer 존재 유무 판별
                if not "_writer not in writerCollection":
                    # _writer 검색
                    driver.switch_to.window(driver.window_handles[-2])
                    driver.switch_to.frame('portletIframe')
                    search_box = driver.find_element_by_css_selector('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.eXPortal_PtlPe041Portlet__9rt5ab_3_InputArea > ul > li:nth-child(1) > input')
                    search_box.clear()
                    search_box.send_keys(_writer)
                    sleep(0.5)
                    search_box.send_keys(Keys.ENTER)

                    # tempStaffInfo list 접근 다시 보기
                    htmlWriter = driver.page_source
                    soupWriter = bs(htmlWriter, 'html.parser')
                    tempStaffInfo = soupWriter.select('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.board_area3 > table > tbody > tr > td')
                    
                    # 검색되지 않을 때 -> 퇴사
                    if len(tempStaffInfo) == 0:         
                        newStaff = page.children[]
                        newStaff.save()
                    # 검색 결과가 list로 반환
                    else:                               
                        # case report: 작성자 소속과, 게시글 소속이 다른 경우가 있음.(_dept는 게시글 소속, tempStaffInfo[0]은 작성자 소속.) 
                        # 그러나 동명이인이 존재할 수 있고, 이 경우 동명이인 중 게시글 소속과 동일한 소속을 우선하고, 동명이인이 있더라도 게시글과 동일한 소속이 없다면, 사실관계 확인 후 수동 부여를 위해 None로 설정한다.
                        for k in range(len(tempStaffInfo) // 5):
                            _exNum = tempStaffInfo[5*k+2]
                            _email = tempStaffInfo[5*k+3]
                            if tempStaffInfo[5*k] == _dept:
                                newStaff = Staff(name=_writer, dept=Dept.objects.get(name=_dept), exNum=_exNum, email=_email)
                                newStaff.save()
                                break
                                # 게시글과 동일한 소속인 사람이 없다. -> 사람은 공란으로 둔다.

                _dept = Dept.objects.get(name=_dept)
                try:
                    _writer = Staff.objects.get(name=_writer)
                except:
                    _writer = None

                portalPost = Portal(title=_title, dept=_dept, writer=_writer, date=_date, pk=_pk)
                portalPost.save()

            driver.switch_to.window(driver.window_handles[-1])
            driver.switch_to.frame("body_frame")

        
        
        # 다음 페이지 탐색
        driver.switch_to.window(driver.window_handles[-1])
        driver.switch_to.frame("body_frame")
        sleep(1)
        next = driver.find_elements_by_css_selector(f'#bi_cont_middle > div:nth-child(6) > div > div > div > a:nth-child({i+3})')
        
        next[0].click()

        # driver.switch_to.window(driver.window_handles[-1])
        # driver.switch_to.frame("body_frame")
        i += 1
        
        if i == 10:
            break
    
    
    if len(pk) != 0:
        msg = f'{datetime.now().strftime("%Y/%m/%d - %H/%M/%S")} 기준, 새로운 게시글은 아래와 같습니다.\n---------------------------------------------\n'
        for l in range(len(pk)):
            msg += f'{title[l]} | {dept[l]} | {writer[l]} [{pk[l]}]\n'
        msg += '---------------------------------------------'
    else:
        msg = 'No update!'

    print(msg)
    file = open(f'/Users/yoon.jh/Desktop/MOP_project/project/crowling/example/{datetime.now().strftime("%Y%m%d")}output_textfile.txt','w')
    file.write(msg)
    file.close

    return msg
    # 키워드 구현 필요
    # 유효성 검사 필요


# 교직원 db 갱신
def checkStaff():
    driver = webdriver.Chrome('/Users/yoon.jh/Desktop/MOP_project/chromedriver')
    driver.implicitly_wait(3)
    curr_url = ''
    driver.get('https://portal.gist.ac.kr/login.jsp')

    while(1):
        if(driver.current_url != 'https://portal.gist.ac.kr/login.jsp'):
            break
        driver.find_element_by_name('user_id').send_keys('ysa5347')
        driver.find_element_by_name('user_password').send_keys('jinhyun@@99')
        sleep(1)
        driver.find_element_by_class_name('btn_login').click()
        sleep(3)
        print(driver.current_url)


    driver.switch_to.frame('portletIframe')
    sleep(1)
    print(driver.current_url)

    staffObjects = Staff.objects.all()
    n = len(staffObjects)
    for obj in staffObjects:
        search_box = driver.find_element_by_css_selector('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.eXPortal_PtlPe041Portlet__9rt5ab_3_InputArea > ul > li:nth-child(1) > input')

        search_box.clear()
        search_box.send_keys(obj.name)
        sleep(0.5)
        search_box.send_keys(Keys.ENTER)

        # tempStaffInfo list 접근 다시 보기
        html = driver.page_source
        soup = bs(html, 'html.parser')
        tempStaffInfo = soup.select('#AjaxPtlBodyeXPortal_PtlPe041Portlet__9rt5ab_3_ > div > div > div.board_area3 > table > tbody > tr > td')

        if len(tempStaffInfo) == 0:         # 만약 검색되지 않는다면 -> 퇴사
            obj.stat, obj.email, obj.exNum = '퇴사', None, None
            
        else:
            obj.stat = '재직'

        obj.save()

while 1:
    if "시간이 30분 지났을 때":
        PortalCrowling()
        
