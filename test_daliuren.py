import pytest
from daliuren4py import calculate, canonical
INPUT={'date':'2026-04-10','hour':14,'minute':30,'timezone':'Asia/Shanghai'}
def test_smoke():
    result=calculate(INPUT)
    assert len(result['gongInfos'])==12
    assert result['algorithmVersion']=='daliuren-shizhan-v1'
    assert len(canonical(INPUT)['三传'])==3
def test_late_zi(): assert calculate({'date':'2026-04-10','hour':23,'minute':30,'timezone':'Asia/Shanghai'})['dateInfo']['ganZhi']==calculate({'date':'2026-04-11','hour':0,'minute':30,'timezone':'Asia/Shanghai'})['dateInfo']['ganZhi']
def test_boundaries():
    assert calculate({'date':'2026-02-18','hour':22,'timezone':'Asia/Shanghai'})['dateInfo']['yueJiang']=='子'
    assert calculate({'date':'2026-02-18','hour':23,'minute':55,'timezone':'Asia/Shanghai'})['dateInfo']['yueJiang']=='亥'
    assert calculate({'date':'2026-09-04','hour':18,'timezone':'Asia/Shanghai'})['dateInfo']['diurnal'] is False
def test_invalid_date():
    with pytest.raises(RuntimeError,match='日期无效'): calculate({'date':'2026-02-30','hour':12})
