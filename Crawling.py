from mimetypes import init
import re
from typing import List
from urllib import response
from bs4 import BeautifulSoup
import requests
import re



def requestCheckForSoup(url):
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        return BeautifulSoup(html, "lxml")
    else:
        print("something is wrong Code: ",(response.status_code)) 




def makeDataList(boards):
    list_of_ntt = []
    BSboards = []
    for board in boards:
        ntt_no = board.get_text()
        if ntt_no.isdigit(): 
            list_of_ntt.append(int(ntt_no))
            BSboards.append(board)
    return list_of_ntt,BSboards

def refreshChecker(list_of_ntt, BSboards, Pre_Ntt_No, urlOfBoard):
    titles = []
    auths = []
    board_urls = []
    ntts = []
    if Pre_Ntt_No < list_of_ntt[0]:
        print(f"Refreshed {list_of_ntt[0]-Pre_Ntt_No} ")
        while Pre_Ntt_No != list_of_ntt[0]:
            up_board = BSboards.pop(0)
            ntts.append(list_of_ntt.pop(0))
            titles.append(re.sub("\n|\t","",up_board.next_sibling.next_sibling.get_text()))
            auths.append(re.sub("\n|\t","",up_board.next_sibling.next_sibling.next_sibling.next_sibling.get_text()))
            board_urls.append(urlOfBoard+str(up_board.next_sibling.next_sibling).split("\"")[3])
    
            
    else: 
        print("Nothing refreshed")
        
    return titles, auths, board_urls, ntts


    
