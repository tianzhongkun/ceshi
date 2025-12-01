import json
import time
import random
import requests
import warnings
import urllib3
from tft_decrypt_data import DataDecryptor
import tft_util
from tools.check_update import CheckUpdate
from tools.utils import chessId_get_data, equipId_get_data, job_get_background_sf, race_get_background_sf

# 忽略 InsecureRequestWarning
warnings.filterwarnings('ignore', category=urllib3.exceptions.InsecureRequestWarning)
#因为没啥规律 只能手动建表了
mode2_d = {
    "1ed": 712,
    "203": 719,
    "21b": 722,
    "22b": 767,
    "241": 768,
    "1e5": 727,
    "1ec": 734,
    "1e6": 735,
    "1e7": 736,
    "1ef": 740,
    "22a": 778,
    "1e4": 753,
    "240": 780,
    "22d": 761,
    "218": 707,
    "1e8":713 ,
    "242": 763,
    "230": 765,
    "1f5": 723,
    "243": 766,
    "216": 732,
    "22e": 773,
    "21c": 751,
    "1f4": 757,
    "22c": 781,
    "22f":784 ,
    "1eb":710 ,
    "244": 783,
    "1f7":721 ,
    "24c": 770,#770 785 786 都是
    "20e": 728,
    "1fc": 729,
    "234": 772,
    "232": 774,
    "231": 775,
    "219": 745,
    "1f6": 752,
    "233": 782,
    "23c": 754,
    "229": 776,
    "221": 709,
    "220": 716,
    "21f": 738,
    "21e": 744,
    "23a": 777,
    "235": 762,
    "201": 714,
    "236": 764,
    "239": 769,
    "237": 771,
    "215": 755,
    "21d": 703,
    "227":705 ,
    "20f":706 ,
    "238": 779,
    "200": 739,
    "202": 742,
    "20c":756 ,
    "20b":758
}
mode1_d = {
    "15a": 10357,
    "168": 10368,
    "16a": 10371,
    "018": 10372,
"173":10380 ,
"175": 10383,
"176":10384 ,
"017": 10391,
"17d": 10394,
"180": 10396,
"185": 10402,
"01b": 10409,
"18d": 10419,
"197": 10434,
"014": 10366,
"016":10370,
"16c": 10374,
"16f": 10377,
"172": 10379,
"174": 10382,
"177": 10385,
"17b": 10393,
"184": 10399,
"00d": 10408,
"01a": 10425,
"192": 10429,
"193": 10430,
"15b": 10358,
"164": 10362,
"166": 10365,
"16e": 10376,
"19a": 10386,
"17e": 10395,
"01d": 10397,
"1c1": 10400,
"013":10405 ,
"00f": 10410,
"18c": 10413,
"18e":10423 ,
"191": 10426,
"194": 10431,
"198": 10435,
"15c": 10359,
"15e": 10360,
"16d": 10375,
"170": 10378,
"019": 10381,
"171": 10387,
"179": 10390,
"182": 10398,
"187": 10403,
"188": 10404,
"18a":10407 ,
"199": 10427,
"196": 10433,
"163": 10361,
"16b": 10373,
"178": 10388,
"189": 10406,
"01c":10422 ,
"190": 10424,
"195": 10432,
"01e": 10436,

}
def generate_did():
    random_part = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    timestamp = int(time.time() * 1000)
    return f"did_{random_part}_{timestamp}"
def hex_decrypt(hex_str:str,mode=1):
    """解密函数"""
    #没啥规律 所以直接写死
    if mode==1:
        return mode1_d[hex_str]
    else:
        return mode2_d[hex_str]
def hex_encrypt(dec_num:int,mode=1):
    """加密函数"""
    if mode == 1:
        #李青 多形态
        if dec_num==10439 or dec_num==10440 or dec_num==10441:
            dec_num=10388
        key = next(k for k, v in mode1_d.items() if v == dec_num)
    else:
        #"24c": 770 785 786 都是
        if dec_num==785 or dec_num==786  :
            dec_num = 770
        key = next(k for k, v in mode2_d.items() if v == dec_num)
    return key  # 转为三位小写，补前导零
def tft_decrypt_to_list(tft_hexstr='0224f000000000000000000000000000TFTSet10',mode=1):
    '''
    解密tft小队字符串 返回英雄id列表
    :return: int
    '''
    hexstr = tft_hexstr[2:-8].strip()
    #将hexstr 3个为一个词 分割
    id_list = [hexstr[i:i+3] for i in range(0, len(hexstr), 3) if hexstr[i:i+3]!="000"]
    id_list = [hex_decrypt(item,mode) for item in id_list]

    return id_list
def tft_encrypt_to_str(id_list=list,mode=1):
    '''
    解密tft小队字符串 返回英雄id列表
    :return: int
    '''
    hexstr_start="02"
    if mode==1:
        hexstr_end = "TFTSet15"
    else:
        hexstr_end = "TFTSet7_Stage2_Revival"
    # id_list 补足10个成员 补足的都用000填充后面的成员
    hex_list=[ ]
    for item in id_list:
        hex_list.append(hex_encrypt(item,mode=mode))
    #补足10个成员
    target_length = 10
    fill_value = "000"
    missing_elements = target_length - len(hex_list)
    # 使用 extend() 方法补充
    hex_list.extend([fill_value] * missing_elements)
    hexstr=hexstr_start+"".join(hex_list)+hexstr_end
    return hexstr
def format_location(i):
    """
    将线性索引转换为行列坐标
    参数:
        i: 线性索引(0-27)
    返回:
        字符串格式的行列坐标 "行,列"
    """
    if not 0 <= i <= 27:
        raise ValueError("索引必须在0-27范围内")

    row = (i // 7)  # 计算行号(3到0)
    col = i % 7  # 计算列号(0到6)
    return f"{row+1},{col+1}"
class TFT():#云顶攻略类 单列模式
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'}
        self.saiji = "s15"  # 赛季

        self.chess_list = self.get_chess()# 棋子资料
        self.equip_list = self.get_equip()# 装备资料
        self.race_list = self.get_race()# 羁绊资料
        self.job_list = self.get_job()  # 职业资料

        self.chess_list2 =self.get_chess(2)  # 棋子资料
        self.equip_list2 =self.get_equip(2)  # 装备资料

        self.race_list2 = self.get_race(2)  # 羁绊资料
        self.job_list2 = self.get_job(2)  # 职业资料
        try:

            with open('datas/my_teams.json', 'r', encoding='utf-8') as f:
                my_teams = json.load(f)
        except:
            print("发现用户没有自定义阵容,新建一个案列")
            my_teams = [
                {"title": "自定义卡组教学案列1 天才 猫咪",
                 "quality": "OP",
                 "teamUrl": "https://www.datatft.com/team-builder/BACCAWDAx3BxBuCDEAv3BxBzCDVBD3BmBYBq-1XAf3BtBpBgYBHZAMbAB%7CJxJOJwFRFQHBs15",
                 "early_info": "早期过渡细节说明",
                 "equipment_info": "装备细节说明",
                 "d_time": "D牌时机和锁血细节",
                 "enemy_info": "对局克制和海克斯推荐等额外说明",
                 "location_info": "站位和对位细节说明"
                 },
                {"title": "自定义卡组教学案列2 天才 猫咪",
                 "quality": "OP",
                 "teamUrl": "https://www.datatft.com/team-builder/BACCAWDAx3BxBuCDEAv3BxBzCDVBD3BmBYBq-1XAf3BtBpBgYBHZAMbAB%7CJxJOJwFRFQHBs15",
                 "early_info": "早期过渡细节说明",
                 "equipment_info": "装备细节说明",
                 "d_time": "D牌时机和锁血细节",
                 "enemy_info": "对局克制和海克斯推荐等额外说明",
                 "location_info": "站位和对位细节说明"
                 }
            ]
            #新建一个my_teams.json
            with open('datas/my_teams.json', 'w', encoding='utf-8') as f:
                json.dump(my_teams, f, ensure_ascii=False, indent=4)


            # 用法例子
        jcu = CheckUpdate("",
                          "",
                          "https://share.note.youdao.com/ynoteshare/index.html?id=2cb8bfc79fdfb0e5e949281fb102f235"
                          )


        self.strategy_list = (self.get_data_diy_list(my_teams,1,lable_="我的阵容")+
                              self.get_data_diy_list(jcu.get_netizen_teams(),1,lable_="懒人严选")+
                              self.get_datatft_list(1)+
                              self.get_strategy_list(1)) # 攻略列表 包含 所有的攻略成员


        self.strategy_list+=self.get_winning_list(1)  # 攻略列表 包含 所有的攻略成员
        self.strategy_list2 = self.get_strategy_list(2)
        self.strategy_list2+=self.get_winning_list(2)  # 攻略列表 包含 所有的攻略成员

    def maopao(self,list):  # 冒泡排序
        length = len(list)
        for i in range(length - 1):
            for j in range(length - i - 1):
                if int(list[j]['sortID']) > int(list[j + 1]['sortID']):
                    list[j], list[j + 1] = list[j + 1], list[j]
                    #print(list[j]['detail'])
        return list[::-1]#列表倒置
    def maopao2(self,list):  # 冒泡排序
        length = len(list)
        for i in range(length - 1):
            for j in range(length - i - 1):

                if int(list[j]['price']) > int(list[j + 1]['price']):
                    list[j], list[j + 1] = list[j + 1], list[j]

                    #print(list[j]['detail'])


        return list#列表倒置
    def guolv(self,l):
        list2=[]
        for item in l:
            if item["price"] == '0' or item["price"] == None or item["price"] == "":
                continue
            else:
                list2.append(item)
        return list2  # 列表倒置
    def get_winning_list(self,mode=1):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42',

        }
        if mode==1:

            datas = {"req_group":[{"req_alias":"tft_lineup_group_list","is_return_source":0,"req_params":{"queue_id":"1100","tier_part":"2","time_type":"d_grouping","version_id":"v3"}}]}

        else:
            return []

        res = requests.post(
            f"https://mlol.qt.qq.com/go/exploit/common_proxy_v2",
            headers=headers, verify=False,data=json.dumps(datas))
        try:
            data_json=  res.json()
        except:
            return []
        __data_list=[]


        data_json=data_json["data"][0]["data"]["main_traits_data"]
        #排序
        data_json.sort(key=lambda x: x["info"]["list"][0]["avg_rank"], reverse=False)
        for i,item in enumerate(data_json):

            avg_rank=item["info"]["list"][0]["avg_rank"]
            #avg_rank_diff=item["info"]["list"][0]["avg_rank_diff"]
            core_chess=item["info"]["list"][0]["core_chess"]
            free_chess=item["info"]["list"][0]["free_chess"]
            assist_chess=item["info"]["list"][0]["assist_chess"]
            assist_chess_equip=item["info"]["list"][0]["assist_chess_equip"]
            main_c_chess_equip=item["info"]["list"][0]["main_c_chess_equip"]

            if mode==1:

                main_c_chess_name=str(self.chess_id_to_name(core_chess[0],mode))


            else:
                main_c_chess_name = str(self.chess_id_to_name2(core_chess[0], mode))




            d={}
            d["quality"]=avg_rank
            d["detail"]={}
            d['detail']['equipment_info']=""
            d['detail']['early_info'] = ""
            d['detail']['d_time'] = ""
            d['detail']['enemy_info'] = ""
            d['detail']['location_info'] = ""
            d['detail']['y21_early_heros'] = ""
            d['detail']['y21_metaphase_heros'] = ""
            d['detail']['hero_replace'] = ""

            d["detail"]["hero_location"]=[]

            chess_list = core_chess + free_chess
            if mode == 1:
                chess_list=[it for it in chess_list if self.chess_id_to_name(it,mode) is not None]
            else:
                #转换一下id
                chess_list=[it for it in chess_list if self.chess_id_to_name2(it, mode) is not None]
                chess_list = [self.chess_TFTID_to_chessId(it,mode) for it in chess_list ]

                assist_chess = [self.chess_TFTID_to_chessId(it,mode) for it in assist_chess ]

            chess_list=chess_list[:10] #最多10个
            if len(chess_list)==0:
                return []
            d["detail"]["level_3_heros"] = ",".join([chess_list[0]] + assist_chess)
            for i_chess,item_chess in  enumerate(chess_list):
                _d_hero={}
                _d_hero["chess_type"]="hero"
                _d_hero["location"] = ""
                _d_hero["hero_id"]=item_chess


                if i_chess==0 :
                    _d_hero["equipment_id"]=",".join([str(self.equip_en_name_to_id(equip,mode)) for equip in main_c_chess_equip])
                elif item_chess in assist_chess:
                    _d_hero["equipment_id"] = ",".join([str(self.equip_en_name_to_id(equip, mode)) for equip in assist_chess_equip])
                else:
                    _d_hero["equipment_id"] = ""




                d["detail"]["hero_location"].append(_d_hero)

            d["detail"]["line_name"] = f"★№官方★【{main_c_chess_name}】{self.get_job_and_race_name(d,mode)} "
            #print(d)
            __data_list.append(d)
        return __data_list
    def get_datatft_list(self,mode=1):
        '''
        一图流 https://www.datatft.com/comps/tier
        '''
        try:
            decryptor = DataDecryptor()
            de_result = decryptor.decrypt_data(decryptor.get_encrypted_str())
            tft_util.result = de_result
            equips15=de_result["equips15"]
            # 获取13位时间截 和特点的did密文
            t = int(time.time() * 1000)
            did=generate_did()
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'CN',
                'Browser-Language': 'ZH-CN',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Length': '2',
                'Content-Type': 'application/json',
                'Host': 'api.datatft.com',
                'Origin': 'https://www.datatft.com',
                'Pragma': 'no-cache',
                'Referer': 'https://www.datatft.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
                'did': did,
                't': str(t),
            }
            #获取攻略id的列表
            res = requests.post(
                f"https://api.datatft.com/team/comps",
                headers=headers, verify=False,data=json.dumps(""))
            try:
                data_json=  res.json()["data"]['list']
                if len(data_json) == 0:
                    return []
            except Exception as err:
                print(err,res.json())
                return []
            __data_list = []
            for i,item in enumerate(data_json):
                d = {}
                #更新协议头
                t = int(time.time() * 1000)
                headers['t']=str(t)
                res = requests.post(
                    "https://api.datatft.com/team/strategy",
                    headers=headers, verify=False, data=json.dumps({"id":item["id"]}))
                dd_json=  res.json()["data"]
                d["quality"] =item["tier"]

                d["detail"] = {}
                d["detail"]["line_name"] = "【云顶大数据】"+item["title"]

                if dd_json.get('tags') is None:
                    d['detail']['equipment_info'] = ""
                else:
                    d['detail']['equipment_info'] = dd_json.get('earlyDesc')

                if dd_json.get('earlyDesc') is None:
                    d['detail']['early_info'] = ""
                else:
                    d['detail']['early_info'] = str(dd_json.get('tags'))

                if dd_json.get('midDesc') is None:
                    d['detail']['d_time'] = ""
                else:
                    d['detail']['d_time'] = dd_json.get('midDesc')

                if dd_json.get('open') is None:
                    d['detail']['enemy_info'] = ""
                else:
                    d['detail']['enemy_info'] = dd_json.get('open')

                teamdata=tft_util.De(dd_json.get("teamUrl"))
                d['detail']['enemy_info']+="\n海克斯:"+str([h['name'] for h in teamdata["mapHexs"]])


                if dd_json.get('finalDesc') is None:
                    d['detail']['location_info'] = ""
                else:
                    d['detail']['location_info'] = dd_json.get('finalDesc')
                d['detail']['y21_early_heros'] = self.format_early_heros(tft_util.De(dd_json.get("earlyTeamUrl"))["mapHeroItems"],mode)
                d['detail']['y21_metaphase_heros'] = ""
                d['detail']['hero_replace'] = ""

                d["detail"]["hero_location"],d["detail"]["level_3_heros"]  = self.format_hero_location(teamdata["mapHeroItems"],equips15,mode)

                __data_list.append(d)
                time.sleep(0.05)
        except Exception as err:
            print("get_datatft_list",err)
            __data_list=[]
        return __data_list
    def get_data_diy_list(self, data_json=[],mode=1,lable_="懒人严选"):
        '''
        自定义阵容展示
        '''
        try:
            decryptor = DataDecryptor()
            de_result = decryptor.decrypt_data(decryptor.get_encrypted_str())
            tft_util.result = de_result
            equips15 = de_result["equips15"]

            __data_list = []
            for i, item in enumerate(data_json):
                d = {}
                d["quality"] = item["quality"]
                d["detail"] = {}
                d["detail"]["line_name"] = "【"+lable_+"】" + item["title"]
                if item.get('equipment_info') is None:
                    d['detail']['equipment_info'] = ""
                else:
                    d['detail']['equipment_info'] = item.get('equipment_info')

                if item.get('early_info') is None:
                    d['detail']['early_info'] = ""
                else:
                    d['detail']['early_info'] = item.get('early_info')

                if item.get('d_time') is None:
                    d['detail']['d_time'] = ""
                else:
                    d['detail']['d_time'] = item.get('d_time')

                if item.get('enemy_info') is None:
                    d['detail']['enemy_info'] = ""
                else:
                    d['detail']['enemy_info'] = item.get('enemy_info')

                teamdata = tft_util.De(item.get("teamUrl"))
                d['detail']['enemy_info'] += "\n海克斯:" + str([h['name'] for h in teamdata["mapHexs"]])

                if item.get('location_info') is None:
                    d['detail']['location_info'] = ""
                else:
                    d['detail']['location_info'] = item.get('location_info')

                d['detail']['y21_early_heros'] = ""
                d['detail']['y21_metaphase_heros'] = ""
                d['detail']['hero_replace'] = ""

                d["detail"]["hero_location"], d["detail"]["level_3_heros"] = self.format_hero_location(
                    teamdata["mapHeroItems"], equips15, mode)

                __data_list.append(d)
                time.sleep(0.05)
        except Exception as err:
            print("get_data_diy_list", err)
            __data_list = []
        return __data_list
    def get_strategy_list(self,mode=1):#返回最新卡组列表包括攻略详情
        '''
        返回所有最新卡组的数据列表
        :return:
        '''
        if mode==1:
            res =requests.get(f"http://game.gtimg.cn/images/lol/act/tftzlkauto/json/lineupJson/{self.saiji}/6/lineup_detail_total.json",
                              headers=self.headers,verify=False)
        else:
            res = requests.get(
                f"http://game.gtimg.cn/images/lol/act/tftzlkauto/json/lineupJson/{self.saiji}/6/6100/lineup_detail_total.json",
                headers=self.headers, verify=False)
        try:
            __data_list=self.maopao(json.loads(res.text)['lineup_list'])

            for i,item in enumerate(__data_list):
                __data_list[i]["detail"]=json.loads(item["detail"].replace("\n", "").replace("\r\n", ""), strict=False)

            return __data_list
        except:
            return []
    def get_chess(self,mode=1):#f获取所以棋子的资料，返回一个列表

        if mode == 1:

            res=requests.get(f"http://game.gtimg.cn/images/lol/act/img/tft/js/chess.js",headers=self.headers, verify=False)
        else:
            res = requests.get(f"http://game.gtimg.cn/images/lol/act/img/tft/js/15.21-2025.S15-6100/chess-6100.js", headers=self.headers,
                               verify=False)
        j=json.loads(res.text)
        j=j['data']
        j = self.maopao2(j)
        j = self.guolv(j)
        return j
    def get_equip(self,mode=1):#获取装资料返回一个列表

        if mode == 1:
            res=requests.get(f"http://game.gtimg.cn/images/lol/act/img/tft/js/equip.js",headers=self.headers, verify=False)
        else:
            res = requests.get(f"http://game.gtimg.cn/images/lol/act/img/tft/js/15.21-2025.S15-6100/equip-6100.js", headers=self.headers,
                               verify=False)
        j=json.loads(res.text)
        j=j['data']
        equip=[]


        # 排除项
        for XH,i in enumerate(j):

            #排除之前版本删除的装备
            #小件装备为89-97
            # if XH<78 :
            #     continue
            # 排除之前版本删除的装备  Form_zb.py  在这里改
            if i['isShow']=="0":
                continue
            equip.append(i)
        return equip
    def get_job(self,mode=1):#获取所有的职业 返回一个列表
        if mode == 1:
            res=requests.get(f'http://game.gtimg.cn/images/lol/act/img/tft/js/job.js',headers=self.headers, verify=False)
        else:
            res = requests.get(f'http://game.gtimg.cn/images/lol/act/img/tft/js/15.21-2025.S15-6100/job-6100.js', headers=self.headers,
                               verify=False)
        j=json.loads(res.text)#兼容模式
        j=j['data']
        return j
    def get_race(self,mode=1):#获取所有的羁绊种族 返回一个列表
        if mode == 1:
            res=requests.get(f'http://game.gtimg.cn/images/lol/act/img/tft/js/race.js',headers=self.headers, verify=False)
        else:
            res = requests.get(f'http://game.gtimg.cn/images/lol/act/img/tft/js/15.21-2025.S15-6100/race-6100.js', headers=self.headers,
                               verify=False)
        j=json.loads(res.text)
        j=j['data']
        return j
    def chess_id_to_name(self,id=0,mode=1):
        '''
        棋子id转名字
        :return:
        '''
        id=str(id)
        if mode==1:
            chess_list=self.chess_list
        else:
            chess_list = self.chess_list2
        for item in chess_list:
            if item["chessId"]==id:
                return item["displayName"]
        return None
    def chess_name_to_id(self,name=0,mode=1):
        '''
        名字转id
        :return:
        '''
        name=str(name)
        if mode==1:
            chess_list=self.chess_list
        else:
            chess_list = self.chess_list2
        for item in chess_list:
            if item["displayName"]==name:
                return item["chessId"]
        return None
    def chess_TFTID_to_chessId(self,id="",mode=1):
        '''
        棋子图片id转棋子id
        :return:
        '''

        if mode==1:
            chess_list=self.chess_list
        else:
            chess_list = self.chess_list2
        for item in chess_list:
            if item["TFTID"]==id:
                return item["chessId"]
        return None
    def chess_id_to_name2(self,id=0,mode=1):
        '''
        棋子id转名字
        :return:
        '''
        id=str(id)
        if mode==1:
            chess_list=self.chess_list
        else:
            chess_list = self.chess_list2
        for item in chess_list:
             if item["TFTID"] == id:
                return item["displayName"]
        return None
    def equip_en_name_to_id(self, en_name="", mode=1):
        '''
        装备英文名转id
        :return:
        '''
        if mode == 1:
            equip_list = self.equip_list
        else:
            equip_list = self.equip_list2
        for item in equip_list:

            if item["englishName"] == en_name:
                return item["equipId"]
        return 0
    def datatft_equip_id_to_name(self, id,equip_list):
        '''
        datatft 装备id转装备名
        :return:
        '''
        id=int(id)
        for item in equip_list:

            if item["equipId"] == id:
                return item["name"]
        return ""
    def datatft_name_to_lol_id(self, equip_name,mode=1):
        '''
        datatft 装备id转装备名
        :return:
        '''

        if mode == 1:
            equip_list = self.equip_list
        else:
            equip_list = self.equip_list2
        for item in equip_list:

            if item["name"] == equip_name:
                return item["equipId"]
        return 0
    def get_job_and_race_name(self,strategy=None,mode=1):
        '''
        根据羁绊和职业 生成一个命名
        :param strategy:
        :return:
        '''

        if strategy is None:
            return ""

        if mode == 1:
            chess_list = self.chess_list
            equip_list=self.equip_list

        else:
            chess_list = self.chess_list2
            equip_list = self.equip_list2

        hero_location=strategy['detail']['hero_location']

        job_list = []
        race_list = []
        for item in hero_location:
            #统计阵容里面的棋字 job和race的数量
            try:
                chess_data = chessId_get_data(chess_list, item['hero_id'])
                if chess_data is None:
                    continue
            except:
                continue
            try:
                job_list+=chess_data['jobIds'].split(',')
            except:
                pass
            try:
                race_list+=chess_data['raceIds'].split(',')
            except:
                pass
            # 看看装备里是否有转职和羁绊
            if item['equipment_id'] != '':
                for equi in item['equipment_id'].split(','):

                    # 将羁绊和职业数据存进容器
                    try:
                        equi_data = equipId_get_data(equip_list, equi)
                        if equi_data is None:  # 排除错误
                            continue
                        if equi_data['jobId'] != '0' and equi_data['jobId'] is not None:
                            job_list.append(equi_data['jobId'])
                    except:
                        pass
                    try:
                        if equi_data['raceId'] != '0' and equi_data['raceId'] is not None:
                            race_list.append(equi_data['raceId'])
                    except:
                        pass

        # 统计职业并按数量降序排序
        job_ss = sorted({}.fromkeys(job_list).keys(),
                        key=lambda x: job_list.count(x),
                        reverse=True)
        #去除空
        job_ss = [it for it in job_ss if it!=""]

        job_id = job_ss[0]
        job_num=job_list.count(job_id)
        try:
            job_txt=f"{job_num}{self.get_job_or_race_data(job_id,job_num,'job',mode)[2]['name']} "
        except:
            job_txt = ""

        # 统计种族并按数量降序排序
        race_ss = sorted({}.fromkeys(race_list).keys(),
                         key=lambda x: race_list.count(x),
                         reverse=True)
        # 去除空
        race_ss = [it for it in race_ss if it != ""]
        race_id = race_ss[0]
        race_num = race_list.count(race_id)

        try:
            race_txt = f"{race_num}{self.get_job_or_race_data(race_id, race_num, 'race', mode)[2]['name']} "
        except:
            race_txt=""

        if race_num>job_num:
            txt=f"{race_txt}{job_txt}"
        else:
            txt=f"{job_txt}{race_txt}"

        return txt
    def get_job_or_race_data(self,id=0,num=0,_type="job",mode=1):
        if mode == 1:

            race_list=self.race_list
            job_list=self.job_list
        else:

            race_list = self.race_list2
            job_list = self.job_list2

        if _type=="job":
            _data=job_get_background_sf(job_list, id,num)
        else:

            _data = race_get_background_sf(race_list, id,num)
        return _data
    def format_early_heros(self,teams=[],mode=1):
        early_heros=[]
        for team in teams:
            if team is None:
                continue
            name=team['hero']['displayName']
            #根据棋子名找到id
            hero_id=self.chess_name_to_id(name,mode)
            early_heros.append({"hero_id":str(hero_id)})
        return early_heros
    def format_hero_location(self,teams=[],equips15=[],mode=1):

        hero_location=[]
        level_3_heros=[]
        for i,team in enumerate(teams):
            if team is None:
                continue
            if team['hero'].get("raceIds") is None:
                chess_type="else"
            else:
                chess_type="hero"

            name=team['hero']['displayName']
            #根据棋子名找到id
            hero_id=self.chess_name_to_id(name,mode)
            if hero_id is  None:

                continue
            if team.get('stars') is None:
                numStar=1
            else:
                numStar=team['stars']
            if numStar==3:
                level_3_heros.append(str(hero_id))
            if team.get('isMain') is None:
                is_carry_hero = False
            else:
                is_carry_hero = team['isMain']
            if team.get('equips') is None:
                equipment_id = ""
            else:
                #将装备id转换成官网的格式
                equips=[]
                for item in team['equips']:
                    datatft_name=self.datatft_equip_id_to_name(item['equipId'],equips15)
                    equip_id = self.datatft_name_to_lol_id(datatft_name)
                    equips.append(equip_id)
                equipment_id = ','.join(str(item) for item in equips)
            d={'chess_type': chess_type, 'hero_id': str(hero_id),
               'equipment_id':  equipment_id,
               'location': format_location(i), 'numStar': numStar, 'is_carry_hero': is_carry_hero,
               'isChosenHero': False, 'is_goop': False, 'is_powerup': is_carry_hero, 'isNew': False}
            hero_location.append(d)

        return hero_location,",".join(level_3_heros)






tft = TFT()
if __name__=="__main__":
    mode=1

    #
    # tft_hexstr = '0216316b17818901c19019501e000000TFTSet15'
    # id_list = tft_decrypt_to_list(tft_hexstr,mode=1)
    # tft_str = tft_encrypt_to_str(id_list,mode=1)
    # name_list = [tft.chess_id_to_name(item,mode=1) for item in id_list]
    # print("解密:", id_list, "=", name_list, "\n加密:", tft_str, "\n测试结果:", tft_str == tft_hexstr)
    #
    # [print(tft.strategy_list2[x]['detail']["line_name"]) for x in range(len(tft.strategy_list2))]

    #tft.get_datatft_list(1)






