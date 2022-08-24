from curses import newpad
from pprint import pprint
from queue import Empty
from warnings import catch_warnings
from dotenv import dotenv_values
import requests
from pprint import pprint
import json

config = dotenv_values(".env")
notion_token = config.get('NOTION_TOKEN')

databaseTableID = config.get("NOTION_DATABASEID")


#post headers
headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def readWriteAsJsonDatabase(databaseID, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseID}"
    try:
        res = requests.request("GET", url= readUrl, headers= headers)
        data = res.json()
        
        print(res.status_code)
        with open("./db.json", "w", encoding= "utf8",) as f:
            json.dump(data, f, ensure_ascii=False)

    except requests.exceptions.Timeout as errd:
        print("Timeout Error : ", errd)
    
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting : ", errc)
    
    except requests.exceptions.HTTPError as errb:
        print("Http Error : ", errb)

    # Any Error except upper exception
    except requests.exceptions.RequestException as erra:
        print("AnyException : ", erra)
    
    



def createPage(databaseID, headers, title, auth, ntt, url):
    createUrl = "https://api.notion.com/v1/pages"
    try:
        newPage = {
            "parent": { "database_id": databaseID },
    
            "properties": {
                "제목": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "url": {
                    "rich_text": [
                        {
                            "text": {
                                "content": url
                            }
                        }
                    ]
                },
                "글쓴이": {
                    "rich_text": [
                        {
                            "text": {
                                "content": auth
                            }
                        }
                    ]
                },
                "NTT": {
                    "rich_text": [
                        {
                            "text": {
                                "content": ntt
                            }
                        }
                    ]
                },
                
            },
        }
        data = json.dumps(newPage)
        res = requests.request("POST", url= createUrl, headers= headers, data= data)

        print(res.status_code)
        

    except requests.exceptions.Timeout as errd:
        print("Timeout Error : ", errd)
    
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting : ", errc)
    
    except requests.exceptions.HTTPError as errb:
        print("Http Error : ", errb)

    # Any Error except upper exception
    except requests.exceptions.RequestException as erra:
        print("AnyException : ", erra)


# createPage(databaseTableID, headers, "asd", "as" ,"12", "as.com")
# readWriteAsJsonDatabase(databaseTableID, headers)
