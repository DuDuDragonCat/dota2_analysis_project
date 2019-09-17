CRUL_PATH="/home/dudumint/桌面/dota2/cruler"
CRUL_DAY=10
echo $CRUL_PATH/openDota_crulMatch_bySQL.py
python $CRUL_PATH/openDota_crulMatch_bySQL.py $CRUL_DAY
python $CRUL_PATH/openDota_crulReplay_byMatchID.py $CRUL_DAY
exit 0
