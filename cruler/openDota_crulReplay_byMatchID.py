import requests
import re
import sys
import os
from os import listdir
from os.path import isfile, join
import time
import datetime
import urllib.parse
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# MATCH_PATH  = '/home/dudumint/桌面/dota2/data/raw_match/'
MATCH_PATH  = '../data/raw_match/'
MATCH_FILESNAME = listdir(MATCH_PATH)

REPLAY_PATH = '/home/dudumint/桌面/dota2/data/raw_replay/'
REPLAY_FILESNAME = listdir(REPLAY_PATH)
REPLAY_BACKUP_PATH = '/media/dudumint/BackupNas/Dota2 replay/dota2_cruler/replay/5800'
REPLAY_BACKUP_FILESNAME = listdir(MATCH_PATH)

# get match page html
def getImgHtml(matchID):
    TRYNUM = 10
    openDotaUrl = "https://www.opendota.com/matches/{}".format(matchID)
    options = webdriver.ChromeOptions()
    
    browser = webdriver.Chrome()
    tryNum = 0
    getHTML= 0
    while tryNum <= TRYNUM :
        browser.implicitly_wait(20)
        browser.get(openDotaUrl)
        try:
            myDynamicElement = browser.find_element_by_class_name('image')
            getHTML= 1
            html = browser.page_source
            browser.close()
            print("No Fresh: ", tryNum)
            return html
        except Exception as e:
            browser.refresh()
            tryNum = tryNum+1
            print("Fresh: ", tryNum)
            continue
    return getHTML

def download_file(url, file_path):
    from requests import get
    reply = get(url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in reply.iter_content(chunk_size=1024): 
            if chunk:
                file.write(chunk)
                
def findMatchFileByDate(dateStr):
    for element in MATCH_FILESNAME:
        m = re.match(dateStr, element)
        if m:
            return element
    return False

def main(argv):
    if len(argv) != 2:
        print("Need One Argv")
        return
    CRUL_DAY = int(argv[1])
    for i in range(1,CRUL_DAY):
        deltaday = datetime.date.today() - datetime.timedelta(days=i)
        year = deltaday.strftime("%Y")
        month = deltaday.strftime("%m")
        day = deltaday.strftime("%d")
        
        dateStr = '^{}{}{}'.format(year, month, day)
        
        matchFileName = '{}{}'.format(MATCH_PATH, findMatchFileByDate(dateStr))
        if findMatchFileByDate(dateStr) is False:
            continue
        df = pd.read_csv(matchFileName)
        
        tmpMatchIdList = df['match_id']
        i = 1
        for tmpMatchId in tmpMatchIdList:
            # check file
            tmpBz2File = str(tmpMatchId)+".dem.bz2"
            if tmpBz2File in REPLAY_FILESNAME or tmpBz2File in REPLAY_BACKUP_FILESNAME:
                print("Found: "+tmpBz2File)
                print("{}/{}".format(i,len(tmpMatchIdList)))
                print()
                i += 1
                continue
            tmpDemFile = str(tmpMatchId)+".dem"
            if tmpDemFile in REPLAY_FILESNAME or tmpDemFile in REPLAY_BACKUP_FILESNAME:
                print("Found: "+tmpDemFile)
                print("{}/{}".format(i,len(tmpMatchIdList)))
                print()
                i += 1
                continue
            # get match html
            temp2 = getImgHtml(tmpMatchId)
            soup = BeautifulSoup(temp2, "html.parser")
            
            href_all = soup.findAll("a",attrs={'href' : re.compile("http://replay")})
            rpUrl = []
            for a in href_all:
                rpUrl = a['href']
                
            if rpUrl == []:
                continue

            fileName = rpUrl.split('/')
            fileName = fileName[len(fileName)-1].split('_')[0]
            fileName = '{}{}.dem.bz2'.format(REPLAY_PATH, fileName)
            download_file(rpUrl, fileName)
            
            print("Download: " + fileName)
            print(rpUrl)
            print("{}/{}".format(i,len(tmpMatchIdList)))
            print()
            i += 1
            time.sleep(1)
    return
 
if __name__ == "__main__":
    main(sys.argv)
