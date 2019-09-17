import os
import pandas as pd
from elasticsearch import Elasticsearch

ELASTIC_INDEX = 'dota2_overview'
es = Elasticsearch('localhost:9200')
result = es.indices.create(index=ELASTIC_INDEX, ignore=400)

MATCH_PATH  = '/home/dudumint/桌面/dota2/data/raw_match/'
MATCH_FILESNAME = os.listdir(MATCH_PATH)
REPLAY_PATH = '/home/dudumint/桌面/dota2/data/raw_replay/'
REPLAY_FILESNAME = os.listdir(REPLAY_PATH)

for tmpFilesNames in MATCH_FILESNAME:
    tmpPath = MATCH_PATH + tmpFilesNames
    df = pd.read_csv(tmpPath)
    for index, row in df.iterrows():
        queryData={"query": {"match": {"_id": str(row['match_id'])}}}
        tmp = es.search(index=ELASTIC_INDEX, body=queryData)
        if tmp['hits']['total']['value'] is 1:
            print("Match Exist: ", str(row['match_id']))
            continue
        tmpData = {
            'match_id': str(row['match_id']),
            'radiant_win': row['radiant_win'],
            'start_time': str(row['start_time']),
            'duration':str(row['duration']),
            'avg_mmr': str(row['avg_mmr']),
            'num_mmr': str(row['num_mmr']),
            'avg_rank_tier': str(row['avg_rank_tier']),
            'num_rank_tier': str(row['num_rank_tier']),
            'lobby_type': str(row['lobby_type']),
            'game_mode': str(row['game_mode'])
           }
        result = es.create(index=ELASTIC_INDEX, id=str(row['match_id']), body=tmpData, ignore=[400, 404, 409])
        print(result)