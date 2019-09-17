import requests
import sys
import re
import os
import time
import datetime
import urllib.parse
import json
import csv
from bs4 import BeautifulSoup
from selenium import webdriver

MATCH_PATH = '/home/dudumint/桌面/dota2/data/raw_match/'
# get sql page html
def getSqlHtml(mmr, startYear, startMonth, startDay, endYear, endMonth, endDay, limit):
    startTime = "{}-{}-{}".format(startYear, startMonth, startDay)
    endTime = "{}-{}-{}".format(endYear, endMonth, endDay)

    sqlQuery =  '''
                SELECT *
                FROM public_matches
                WHERE TRUE
                AND public_matches.avg_mmr >= {}
                AND public_matches.start_time >= extract(epoch from timestamp '{}T00:00:00+00:00')
                AND public_matches.start_time <  extract(epoch from timestamp '{}T23:59:59+00:00')
                AND public_matches.lobby_type = 7
                LIMIT {}
                '''.format(mmr,startTime,endTime,limit)

    openDotaUrl = "https://api.opendota.com/api/explorer?sql="
    sqlUrl = openDotaUrl+urllib.parse.quote_plus(sqlQuery)

    options = webdriver.ChromeOptions()
    
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    browser.get(sqlUrl)
    myDynamicElement = browser.find_element_by_tag_name('pre')
    html = browser.page_source
    browser.close()
    return html
def jsonToCsv(json, mmr, startYear, startMonth, startDay):
    json_data = json['rows']
    fileName = "{}{}{}_{}".format(startYear,startMonth,startDay,len(json_data))
    # open a file for writing
    dayMatchId_data = open('{}{}.csv'.format(MATCH_PATH,fileName), 'w')

    # create the csv writer object
    csvwriter = csv.writer(dayMatchId_data)
    count = 0
    for jsKey in json_data:
          if count == 0:
                 header = jsKey.keys()
                 csvwriter.writerow(header)
                 count += 1
          csvwriter.writerow(jsKey.values())
    dayMatchId_data.close()


def main(argv):
    if len(argv) != 2:
        print("Need One Argv")
        return
    CRUL_DAY = int(argv[1])
    today = datetime.date.today()
    MMR = "5800"
    for i in range(1,CRUL_DAY):
        deltaday = datetime.timedelta(days=i)
        deltaday = today - deltaday
        
        
        startYear = deltaday.strftime("%Y")
        startMonth = deltaday.strftime("%m")
        startDay = deltaday.strftime("%d")
        endYear = deltaday.strftime("%Y")
        endMonth = deltaday.strftime("%m")
        endDay = deltaday.strftime("%d")
        limit = "10000"
        
        temp = getSqlHtml(MMR, startYear, startMonth, startDay, endYear, endMonth, endDay, limit)
        temp = BeautifulSoup(temp, "html.parser")
        href_all = temp.find("pre")
        jsonText = json.loads(href_all.text)
        jsonToCsv(jsonText, MMR, startYear, startMonth, startDay)
        
        print("{} Done: {}{}".format(i,startMonth,startDay))
        time.sleep(1)
    return
 
if __name__ == "__main__":
    main(sys.argv)
