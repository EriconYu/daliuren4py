from daliuren4py import calculate
INPUT={'date':'2026-04-10','hour':14,'minute':30,'timezone':'Asia/Shanghai'}
def test_smoke(): assert len(calculate(INPUT)['gongInfos'])==12
def test_late_zi(): assert calculate({'date':'2026-04-10','hour':23,'minute':30,'timezone':'Asia/Shanghai'})['dateInfo']['ganZhi']==calculate({'date':'2026-04-11','hour':0,'minute':30,'timezone':'Asia/Shanghai'})['dateInfo']['ganZhi']
