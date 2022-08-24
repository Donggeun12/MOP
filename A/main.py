from operator import length_hint
from Crawling import makeDataList, refreshChecker, requestCheckForSoup
from dotenv import dotenv_values
from Notion_Linking_WRequests import createPage
from time import sleep
import re
from rich.console import Console


urlOfBoard = "https://www.gist.ac.kr/kr/html/sub06/060101.html"
Pre_Ntt_No = 4600


databaseTableID = ""
config = dotenv_values(".env")
notion_token = config.get('NOTION_TOKEN')
headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}



while 1:
    soup = requestCheckForSoup(url= urlOfBoard)
    body_of_board = soup.find_all(class_ ="ntt_no" )

    list_ntt, BSboards = makeDataList(body_of_board)

    titles, auths, boards_url, ntts = refreshChecker(list_ntt, BSboards, Pre_Ntt_No, urlOfBoard)
    if len(ntts) == 0:
        print("[bold red]Nothing Changed")
    else:
        Pre_Ntt_No = ntts[0]
        boards_url = [re.sub("amp;","", x) for x in boards_url]
        print(f"\n {Pre_Ntt_No}")

        for i in range(len(ntts)):
            print("----PROGRESS ----",titles[i],ntts[i])
            createPage(databaseTableID,headers, titles[i], auths[i], str(ntts[i]), boards_url[i] )

    # sleep(300)

    console = Console()
    tasks = [f"times waiting-- {n}" for n in range(1, 11)]

    with console.status("[bold green]Waiting...") as status:
        while tasks:
            task = tasks.pop(0)
            sleep(60)
            console.log(f"{task} minutes")
