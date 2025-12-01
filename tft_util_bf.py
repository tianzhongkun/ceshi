import re
from tft_decrypt_data import DataDecryptor
import requests
import urllib.parse
import json
# ========================================
# 全局映射表
# ========================================
g = {}
d = {}
# ========================================
# 获取数据
# ========================================
decryptor = DataDecryptor()
result = decryptor.decrypt_data(decryptor.get_encrypted_str())

def A():
    return result.get('heros15', [])

def O():
    return result.get('equips15', [])

def H():
    return result.get('hexs15', [])

def j():
    return result.get('anomalies15', [])

def D(code):
    for row in H():
        for item in row:
            if item['code'] == code:
                return item
    return None

def S(code):
    for item in A():
        if item['code'] == code:
            return item
    return None

def F(code):
    for item in O():
        if item['code'] == code:
            return item
    return None

def J(code):
    for item in j():
        if item['code'] == code:
            return item
    return None

def P(e):
    return e.isdigit()

def v():
    """
    初始化全局映射表 g 和 d
    """
    global g, d
    g = {}
    d = {}

    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    map_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!<>."

    # map0 ~ map55
    for r in range(56):
        g_key = f"map{r}"
        d_key = f"map{map_chars[r]}"
        g[g_key] = map_chars[r]
        d[d_key] = r

    # 英雄映射
    heroes = A()
    for idx, hero in enumerate(heroes):
        o = idx // len(chars)
        f = (str(o) if o > 0 else "") + chars[idx - o * len(chars)]
        if 'code' in hero:
            f = hero['code']
        g[f"hero{hero['chessId']}"] = f
        d[f"hero{f}"] = hero['chessId']

    # 装备映射（过滤并调整顺序）
    equips = O()
    filtered = [e for e in equips if e['equipId'] not in [612, 545, 573, 31004, 31005, 31006, 31007, 2252]]
    special = [e for e in equips if e['equipId'] in [31004, 31005, 31006, 31007]]
    equip_list = filtered + special

    for idx, equip in enumerate(equip_list):
        o = idx // len(chars)
        f = chars[o] + chars[idx - o * len(chars)]
        if 'code' in equip:
            f = equip['code']
        g[f"equip{equip['equipId']}"] = f
        d[f"equip{f}"] = equip['equipId']

    # 海克斯映射
    hexes = [item for row in H() for item in row]
    for hex_item in hexes:
        g[f"hex{hex_item['hexId']}"] = hex_item['code']
        d[f"hex{hex_item['code']}"] = hex_item['hexId']

    # 强化符文（anomalies）
    anomalies = j()
    for item in anomalies:
        g[f"powerup{item['key']}"] = item['code']
        d[f"powerup{item['code']}"] = item['key']
# ========================================
# URL 解码
# ========================================
def decode_uri_component(encoded):
    try:
        return urllib.parse.unquote(encoded)
    except Exception:
        return encoded
# ========================================
# 核心解密函数 L(e, l)
# ========================================
def L(e, l=None):
    if l is None:
        l = {}

    print("decrypt", e)

    # 清理输入
    e = (e
         .replace("https://www.datatft.com/team-builder/", "")
         .replace("https://www.datatft.com/simulator/", "")
         .replace("%7C", "|"))

    if e.endswith("."):
        e = e[:-1]

    if e.endswith("s") and len(e) >= 3 and e[-3] == 's' and e[-2:].isdigit():
        e = e[:-3]

    if not e:
        return {
            "mapHeroItems": [None] * 56,
            "mapHexs": [],
            "isError": False
        }

    try:
        e = decode_uri_component(e)
    except:
        pass

    s = 0
    map_hero_items = [None] * 56
    map_hexs = []
    is_error = False

    while s < len(e):
        if e[s] == '|':
            s += 1
            while s < len(e):
                if s + 2 > len(e):
                    break
                code = e[s:s+2]
                hex_id = d.get(f"hex{code}")
                if hex_id is None:
                    is_error = True
                    msg = f"强化符文解析失败: {code}"
                    print(msg)
                    if 'onError' in l:
                        l['onError'](msg)
                    break
                hex_obj = D(code)
                #print("hexInDB", hex_obj)
                if hex_obj:
                    map_hexs.append(hex_obj)
                s += 2
            break

        # 解析地图位置
        pos_char = e[s]
        s += 1
        pos_idx = d.get(f"map{pos_char}")
        if pos_idx is None:
            is_error = True
            msg = f"map位置解析失败: {pos_char}, idx: {s}, length: {len(e)}"
            print(msg)
            if 'onError' in l:
                l['onError'](msg)
            break

        if pos_idx > 27 and 'onMapIndexChange' in l:
            l['onMapIndexChange'](pos_idx)

        # 解析英雄
        if s + 2 > len(e):
            is_error = True
            break
        hero_code = e[s:s+2]
        s += 2
        hero_id = d.get(f"hero{hero_code}")
        print(hero_code)
        if hero_id is None:
            is_error = True
            msg = f"弈子解析失败: {hero_code}"
            print(msg)
            if 'onError' in l:
                l['onError'](msg)
            continue

        item = {"id": hero_id, "index": pos_idx}
        hero_obj = S(hero_code)
        item["hero"] = hero_obj

        # 装备
        if s < len(e) and (P(e[s]) or e[s] in '123456789'):
            equips = []
            # 处理数量或绑定前缀
            if P(e[s]):
                count = int(e[s])
                s += 1
            else:
                count = 1  # 默认1件

            for _ in range(count):
                if s + 2 > len(e):
                    is_error = True
                    break

                code = e[s:s + 2]
                s += 2

                # 判断是否是绑定码：1P, 2Z, 1A 等
                if code[0] in '123456789' and code[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    # 是绑定码，如 1P, 2Z
                    target_hero_index = int(code[0]) - 1  # 第1个英雄 → index 0
                    equip_char = code[1]

                    # 特殊处理：P 和 Z 是特殊装备
                    special_map = {
                        'P': 'ZA',  # Thief's Gloves
                        'Z': 'ZB',  # Shimmerscale
                        # 可扩展
                    }
                    equip_code = special_map.get(equip_char, f"{equip_char}{equip_char}")

                    equip_id = d.get(f"equip{equip_code}")
                    if equip_id is None:
                        is_error = True
                        print(f"特殊装备解析失败: {code} → {equip_code}")
                        if 'onError' in l:
                            l['onError'](f"特殊装备解析失败: {code}")
                        continue

                    equip_obj = F(equip_code)
                    if equip_obj:
                        equips.append(equip_obj)
                else:
                    # 普通装备 AA, AB, AC...
                    equip_id = d.get(f"equip{code}")
                    if equip_id is None:
                        is_error = True
                        msg = f"装备解析失败: {code}"
                        print(msg)
                        if 'onError' in l:
                            l['onError'](msg)
                    else:
                        equip_obj = F(code)
                        if equip_obj:
                            equips.append(equip_obj)

            item["equips"] = equips

        # 强化果实 (powerups)
        if s < len(e) and e[s] == '~':
            s += 1
            if s >= len(e):
                is_error = True
                break
            pu_count = int(e[s])
            s += 1
            powerups = {"left": [], "right": [], "top": [], "bottom": []}
            for _ in range(pu_count):
                if s >= len(e):
                    is_error = True
                    break
                side = e[s]
                s += 1
                pos = ""
                if side == 'L': pos = "left"
                elif side == 'R': pos = "right"
                elif side == 'T': pos = "top"
                elif side == 'B': pos = "bottom"
                else:
                    is_error = True
                    print("强化果实位置解析失败", side)
                    continue

                if s + 2 > len(e):
                    is_error = True
                    break
                code = e[s:s+2]
                s += 2
                key = d.get(f"powerup{code}")
                if key is None:
                    is_error = True
                    print("强化果实解析失败", code)
                    continue
                pu_obj = J(code)
                if pu_obj:
                    cloned = pu_obj.copy()
                    cloned["position"] = pos
                    powerups[pos].append(cloned)
            if not is_error:
                item["powerups"] = powerups

        # 星级
        if s < len(e) and e[s] == '*':
            s += 1
            if s >= len(e):
                is_error = True
                break
            stars = int(e[s])
            s += 1
            item["stars"] = stars

        # 主C
        if s < len(e) and e[s] == '-':
            s += 2  # skip "-1"
            item["isMain"] = True

        # 替换英雄
        if s < len(e) and e[s] == '_':
            s += 1
            if s + 2 > len(e):
                is_error = True
                break
            replace_code = e[s:s+2]
            s += 2
            replace_id = d.get(f"hero{replace_code}")
            replace_hero = S(replace_code)
            item["replaceId"] = replace_id
            item["replaceIdPrice"] = replace_hero.get("price") if replace_hero else None

        map_hero_items[pos_idx] = item

    return {
        "mapHeroItems": map_hero_items,
        "mapHexs": map_hexs,
        "isError": is_error
    }
# ========================================
# 对外接口：De(url, options)
# ========================================

def De(url, options=None):
    """
    解密 datatft 分享链接
    :param url: 完整 URL 或分享码
    :param options: { onError, onMapIndexChange }
    :return: 解析结果
    """
    if not d:  # 如果未初始化
        v()
    return L(url, options)

def We(endpoint, params):
    """模拟 HTTP 请求（替换为真实 API）"""
    base = "https://www.datatft.com/api"
    try:
        resp = requests.get(base + endpoint, params=params)
        return resp.json()
    except Exception as e:
        print("请求失败:", e)
        return None
# 模拟响应式变量
class Ref:
    def __init__(self, value=None):
        self.value = value

# 全局状态
WW = {}  # 示例阵容 ID
UU = Ref(False)
dd = Ref({})
LL = Ref([])  # 主阵容
BB = Ref([])  # 海克斯
bb = Ref([])  # 早期阵容

def ce(strategy_id=None):
    """
    获取并解析阵容策略
    """
    try:
        UU.value = True
        sid = strategy_id or WW.get("id")
        if not sid:
            return

        resp = We("/team/strategy", {"id": sid})
        if resp:
            d.value = resp
            team_url = resp.get("teamUrl", "")
            early_url = resp.get("earlyTeamUrl", "")

            # 解密主阵容
            k = De(team_url, {
                "onError": lambda x: print("解密错误:", x)
            })
            if not k["isError"]:
                LL.value = k["mapHeroItems"][:28]
                BB.value = k["mapHexs"]

            # 解密早期阵容
            N = De(early_url, {})
            if not N["isError"]:
                bb.value = N["mapHeroItems"][:28]

        UU.value = False
    except Exception as e:
        print("获取阵容数据失败:", e)

# ========================================
# 使用示例
# ========================================

if __name__ == "__main__":
    # 初始化映射
    v()

    # 示例分享码（需替换为真实有效码）
    test_url = "https://www.datatft.com/team-builder/CAC3BxBuBz*3DAx2ByCDEBE1CFFAKVAM3CbBZBY*3-1WBD2BgBe-1YAfaABbBH%7CEgFZElFvHBHSHyKNKWs15"

    result_parsed = De(test_url)
    print(result_parsed)

    print("\n=== 解析结果 ===")
    print("是否出错:", result_parsed["isError"])
    print("海克斯:", [h['name'] for h in result_parsed["mapHexs"]])

    print("\n棋子布局:")
    for i, item in enumerate(result_parsed["mapHeroItems"]):
        if item:

            hero_name = item["hero"]["displayName"] if item["hero"] else "Unknown"
            stars = item.get("stars", 1)
            equips = [e["name"] for e in item.get("equips", [])]
            print(f"格{i}: {hero_name}*{stars} 装备:{equips}")