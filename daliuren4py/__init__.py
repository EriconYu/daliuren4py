from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from lunar_python import Solar
GAN=list('甲乙丙丁戊己庚辛壬癸'); ZHI=list('子丑寅卯辰巳午未申酉戌亥'); JIAZI=[GAN[i%10]+ZHI[i%12] for i in range(60)]
JI_GONG={'甲':'寅','乙':'辰','丙':'巳','戊':'巳','丁':'未','己':'未','庚':'申','辛':'戌','壬':'亥','癸':'丑'}
YUE_JIANG={'雨水':'亥','惊蛰':'亥','春分':'戌','清明':'戌','谷雨':'酉','立夏':'酉','小满':'申','芒种':'申','夏至':'未','小暑':'未','大暑':'午','立秋':'午','处暑':'巳','白露':'巳','秋分':'辰','寒露':'辰','霜降':'卯','立冬':'卯','小雪':'寅','大雪':'寅','冬至':'丑','小寒':'丑','大寒':'子','立春':'子'}
YUE_NAMES={'亥':'登明','戌':'河魁','酉':'从魁','申':'传送','未':'小吉','午':'胜光','巳':'太乙','辰':'天罡','卯':'太冲','寅':'功曹','丑':'大吉','子':'神后'}
JIANG=['贵人','腾蛇','朱雀','六合','勾陈','青龙','天空','白虎','太常','玄武','太阴','天后']; SHORT=dict(zip(JIANG,list('贵蛇雀合勾龙空虎常玄阴后')))
YANG_GUI={'甲':'丑','戊':'丑','庚':'丑','乙':'子','己':'子','丙':'亥','丁':'亥','壬':'巳','癸':'巳','辛':'午'}; YIN_GUI={'甲':'未','戊':'未','庚':'未','乙':'申','己':'申','丙':'酉','丁':'酉','壬':'卯','癸':'卯','辛':'寅'}
YIMA={'寅':'申','午':'申','戌':'申','申':'寅','子':'寅','辰':'寅','巳':'亥','酉':'亥','丑':'亥','亥':'巳','卯':'巳','未':'巳'}; DINGMA={'甲子':'卯','甲戌':'丑','甲申':'亥','甲午':'酉','甲辰':'未','甲寅':'巳'}; TIANMA={'未':'辰','丑':'辰','午':'寅','子':'寅','巳':'子','亥':'子','辰':'戌','戌':'戌','卯':'申','酉':'申','申':'午','寅':'午'}
WUXING={'子':'水','丑':'土','寅':'木','卯':'木','辰':'土','巳':'火','午':'火','未':'土','申':'金','酉':'金','戌':'土','亥':'水','甲':'木','乙':'木','丙':'火','丁':'火','戊':'土','己':'土','庚':'金','辛':'金','壬':'水','癸':'水'}
REL={('水','木'):'生',('水','火'):'克',('水','土'):'贼',('水','金'):'养',('水','水'):'比',('木','水'):'养',('木','火'):'生',('木','土'):'克',('木','金'):'贼',('木','木'):'比',('火','水'):'贼',('火','火'):'比',('火','土'):'生',('火','金'):'克',('火','木'):'养',('土','水'):'克',('土','火'):'养',('土','土'):'比',('土','金'):'生',('土','木'):'贼',('金','水'):'生',('金','火'):'贼',('金','土'):'养',('金','金'):'比',('金','木'):'克'}; LIUQIN={'生':'子孙','克':'妻财','贼':'官鬼','养':'父母','比':'兄弟'}
CHANG_NAMES=['长生','沐浴','冠带','临官','帝旺','衰','病','死','墓','绝','胎','养']; CHANG_START={'甲':'亥','乙':'午','丙':'寅','丁':'酉','戊':'寅','己':'酉','庚':'巳','辛':'子','壬':'申','癸':'卯'}
JIAN=['建','除','满','平','定','执','破','危','成','收','开','闭']; _TABLE=json.loads(Path(__file__).with_name('sanchuan.json').read_text())
def _validate(i):
 if not isinstance(i.get('date'),str) or len(i['date'])!=10: raise ValueError('date 必须是 YYYY-MM-DD')
 try:y,m,d=map(int,i['date'].split('-'));dt=datetime(y,m,d,int(i['hour']),int(i.get('minute',0)))
 except Exception as e: raise ValueError('日期无效，支持范围为 1900 到 2100 年') from e
 if y<1900 or y>2100 or not isinstance(i.get('hour'),int) or not 0<=i['hour']<=23 or not isinstance(i.get('minute',0),int) or not 0<=i.get('minute',0)<=59: raise ValueError('日期无效，支持范围为 1900 到 2100 年')
 return dt
def _xun(p):
 idx=JIAZI.index(p); start=idx//10*10; used={JIAZI[x][1] for x in range(start,start+10)};return JIAZI[start],[b for b in ZHI if b not in used]
def _shang(tian,z): return tian[ZHI.index(z)]
def _jiang_for(tian,jiang,z): return jiang[tian.index(z)]
def _chang(g,z):
 start=ZHI.index(CHANG_START[g]);pos=ZHI.index(z);off=(pos-start)%12 if GAN.index(g)%2==0 else (start-pos)%12;return CHANG_NAMES[off]
def _wang(month_zhi,wx):
 wang={'寅':'木','卯':'木','巳':'火','午':'火','申':'金','酉':'金','亥':'水','子':'水','辰':'土','未':'土','戌':'土','丑':'土'}[month_zhi]; cycle=['木','火','土','金','水'];i=cycle.index(wang);return '旺' if wx==wang else '相' if wx==cycle[(i+1)%5] else '休' if wx==cycle[(i+4)%5] else '囚' if wx==cycle[(i+3)%5] else '死'
def _liuqin(g,z): return LIUQIN[REL[(WUXING[g],WUXING[z])]]
def calculate(i:dict[str,Any])->dict[str,Any]:
 dt=_validate(i);y,m,d,h,minute=dt.year,dt.month,dt.day,dt.hour,dt.minute;l=Solar.fromYmdHms(y,m,d,h,minute,0).getLunar();pillars=[l.getYearInGanZhiExact(),l.getMonthInGanZhiExact(),l.getDayInGanZhiExact(),l.getTimeInGanZhi()];term=l.getPrevJieQi(False).getName();yj=YUE_JIANG[term];xun,kong=_xun(pillars[2]);day_gan,day_zhi=pillars[2];hour_zhi=pillars[3][1];diurnal=hour_zhi in '卯辰巳午未申'
 tian=['']*12;hi=ZHI.index(hour_zhi);yi=ZHI.index(yj)
 for n in range(12):tian[(hi+n)%12]=ZHI[(yi+n)%12]
 gui=(YANG_GUI if diurnal else YIN_GUI)[day_gan];gp=tian.index(gui);forward=ZHI[gp] in '亥子丑寅卯辰';jiang=['']*12
 for n,name in enumerate(JIANG):jiang[(gp+n*(1 if forward else -1))%12]=name
 def lesson(lower):
  upper=_shang(tian,lower);return [upper+lower,_jiang_for(tian,jiang,upper)]
 yi_ke=lesson(JI_GONG[day_gan]);er_ke=lesson(yi_ke[0][0]);san_ke=lesson(day_zhi);si_ke=lesson(san_ke[0][0])
 dun={b:'' for b in ZHI};start=ZHI.index(xun[1]);
 for n in range(10):dun[ZHI[(start+n)%12]]=GAN[n]
 month_zhi=pillars[1][1];jc={b:'' for b in ZHI};jstart=tian.index(month_zhi)
 for n,name in enumerate(JIAN):jc[ZHI[(jstart+n)%12]]=name
 entry=_TABLE[pillars[2]][ZHI.index(yi_ke[0][0])];combo=entry['干支组合'];method=entry['格局']
 def transmission(z):return [z,_jiang_for(tian,jiang,z),_liuqin(day_gan,z),dun[z]]
 chu,zhong,mo=map(transmission,combo)
 tdp={'diPan':{str(n):ZHI[n] for n in range(12)},'tianPan':{str(n):tian[n] for n in range(12)},'tianJiang':{str(n):jiang[n] for n in range(12)}}
 gong=[]
 for n,b in enumerate(ZHI):tz=tian[n];gong.append({'diZhi':b,'tianZhi':tz,'tianJiang':jiang[n],'tianJiangShort':SHORT[jiang[n]],'dunGan':dun[b],'changSheng':_chang(day_gan,tz),'wuXing':WUXING[tz],'wangShuai':_wang(month_zhi,WUXING[tz]),'jianChu':jc[b]})
 sub=[method];extra=[]
 if day_zhi in '子卯午酉' and san_ke[0][0] in '子卯午酉' and combo[0] in '子卯午酉':extra.append('三交')
 wi=[WUXING[z] for z in combo];sheng={'木':'火','火':'土','土':'金','金':'水','水':'木'}
 if sheng[wi[0]]==wi[1] and sheng[wi[1]]==wi[2]:extra.append('铸印')
 if (ZHI.index(combo[1])-ZHI.index(combo[0]))%12==(ZHI.index(combo[2])-ZHI.index(combo[1]))%12==1 or (ZHI.index(combo[0])-ZHI.index(combo[1]))%12==(ZHI.index(combo[1])-ZHI.index(combo[2]))%12==1:extra.append('连珠')
 tao='卯' if day_zhi in '寅午戌' else '酉' if day_zhi in '申子辰' else '午' if day_zhi in '巳酉丑' else '子';date_info={'solarDate':f'{y}年{m}月{d}日 {h}时{minute}分','bazi':' '.join(pillars),'ganZhi':dict(zip(('year','month','day','hour'),pillars)),'yueJiang':yj,'yueJiangName':YUE_NAMES[yj],'xun':xun,'kongWang':kong,'yiMa':YIMA[day_zhi],'dingMa':DINGMA[xun],'tianMa':TIANMA[month_zhi],'diurnal':diurnal}
 result={'algorithmVersion':'daliuren-shizhan-v1','dateInfo':date_info,'tianDiPan':tdp,'siKe':{'yiKe':yi_ke,'erKe':er_ke,'sanKe':san_ke,'siKe':si_ke},'sanChuan':{'chu':chu,'zhong':zhong,'mo':mo,'method':method},'keTi':{'method':method,'subTypes':sub,'extraTypes':extra},'keName':f'{pillars[2]}日 干上{yi_ke[0][0]}','shenSha':[{'name':'桃花','value':tao,'description':'主桃花、感情、人缘。'}],'gongInfos':gong,'dunGan':dun,'jianChu':jc}
 if 'question'in i:result['question']=i['question']
 if i.get('birthYear') and i.get('gender'):
  age=y-i['birthYear'];result['benMing']=GAN[(i['birthYear']-4)%10]+ZHI[(i['birthYear']-4)%12];result['xingNian']=(GAN[(2+age)%10]+ZHI[(2+age)%12]) if i['gender']=='male' else (GAN[(8-age)%10]+ZHI[(8-age)%12])
 return result
def canonical(i:dict[str,Any])->dict[str,Any]:
 r=calculate(i);di=r['dateInfo'];basic={'占测时间':di['solarDate'],'昼夜':'昼占' if di['diurnal'] else '夜占','四柱':di['bazi'],'课式':f"{r['keName']} / {r['keTi']['method']}课",'月将':di['yueJiang'],'关键状态':{'空亡':di['kongWang'],'驿马':di['yiMa'],'丁马':di['dingMa'],'天马':di['tianMa']}}
 if 'question'in r:basic['占事']=r['question']
 lessons=[]
 for label,key in zip(['一课 (干上)','二课 (干阴)','三课 (支上)','四课 (支阴)'],['yiKe','erKe','sanKe','siKe']):
  x=r['siKe'][key];lessons.append({'课别':label,'乘将':x[1] or '-','上神':x[0][0] if x else '-','下神':x[0][1] if x else '-'})
 trans=[]
 for label,key in zip(['初传 (发端)','中传 (移易)','末传 (归计)'],['chu','zhong','mo']):
  x=r['sanChuan'][key];trans.append({'传序':label,'地支':x[0] or '-','天将':x[1] or '-','六亲':x[2] or '-','遁干':x[3] or '-'})
 board=[{'地盘':x['diZhi'],'五行':x['wuXing'],'旺衰':x['wangShuai'],'天盘':x['tianZhi'],'天将':x['tianJiang'],'遁干':x['dunGan'] or '-','长生十二神':x['changSheng'] or '-'} for x in r['gongInfos']]
 return {'基本信息':basic,'四课':lessons,'三传':trans,'天地盘':board}
__all__=['calculate','canonical']
