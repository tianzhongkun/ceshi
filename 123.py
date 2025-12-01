self.doc_early = strategy['detail']['early_info'].replace("&#10;", "") + "。" + strategy['detail'][
    'equipment_info'].replace('&amp;nbsp;', '').replace("&#10;", "")
self.doc_d_time = strategy['detail']['d_time'].replace("&#10;", "")
self.doc_enemy = strategy['detail']['enemy_info'].replace("&#10;", "")
self.doc_location = strategy['detail']['location_info'].replace("&#10;", "")
self.switch_doc(self._typer)

avg_rank = item["info"]["list"][0]["avg_rank"]
# avg_rank_diff=item["info"]["list"][0]["avg_rank_diff"]
core_chess = item["info"]["list"][0]["core_chess"]
free_chess = item["info"]["list"][0]["free_chess"]
assist_chess = item["info"]["list"][0]["assist_chess"]
assist_chess_equip = item["info"]["list"][0]["assist_chess_equip"]
main_c_chess_equip = item["info"]["list"][0]["main_c_chess_equip"]

if mode == 1:

    main_c_chess_name = str(self.chess_id_to_name(core_chess[0], mode))


else:
    main_c_chess_name = str(self.chess_id_to_name2(core_chess[0], mode))

d = {}
d["quality"] = avg_rank
d["detail"] = {}
d['detail']['equipment_info'] = ""
d['detail']['early_info'] = ""
d['detail']['d_time'] = ""
d['detail']['enemy_info'] = ""
d['detail']['location_info'] = ""
d['detail']['y21_early_heros'] = ""
d['detail']['y21_metaphase_heros'] = ""
d['detail']['hero_replace'] = ""

d["detail"]["hero_location"] = []

chess_list = core_chess + free_chess
if mode == 1:
    chess_list = [it for it in chess_list if self.chess_id_to_name(it, mode) is not None]
else:
    # 转换一下id
    chess_list = [it for it in chess_list if self.chess_id_to_name2(it, mode) is not None]
    chess_list = [self.chess_TFTID_to_chessId(it, mode) for it in chess_list]

    assist_chess = [self.chess_TFTID_to_chessId(it, mode) for it in assist_chess]

chess_list = chess_list[:10]  # 最多10个
if len(chess_list) == 0:
    return []
d["detail"]["level_3_heros"] = ",".join([chess_list[0]] + assist_chess)
for i_chess, item_chess in enumerate(chess_list):
    _d_hero = {}
    _d_hero["chess_type"] = "hero"
    _d_hero["location"] = ""
    _d_hero["hero_id"] = item_chess

    if i_chess == 0:
        _d_hero["equipment_id"] = ",".join([str(self.equip_en_name_to_id(equip, mode)) for equip in main_c_chess_equip])
    elif item_chess in assist_chess:
        _d_hero["equipment_id"] = ",".join([str(self.equip_en_name_to_id(equip, mode)) for equip in assist_chess_equip])
    else:
        _d_hero["equipment_id"] = ""

    d["detail"]["hero_location"].append(_d_hero)

d["detail"]["line_name"] = f"【{main_c_chess_name}】{self.get_job_and_race_name(d, mode)} "
# print(d)
__data_list.append(d)