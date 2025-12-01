from PyQt5 import QtCore
from PyQt5.Qt import *

import setting
from ui.form_strategy_list import Ui_FormStrategyList
from page.page_item_strategy import ItemStrategy
from tft import tft as tft_instance  # 导入tft实例
from tools.utils import chessId_get_data  # 导入工具函数
class FormStrategyList(QWidget, Ui_FormStrategyList):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.set_ui()
        self.setupUi(self)
        self.resize(744, 95)  # 大小
        self.move(0, 0)  # 位置
        self.frame.setObjectName("frame_box")
        self.is_lock=False
        # 禁止编辑
        self.tw_strategy_list.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 水平表格头显示和隐藏
        self.tw_strategy_list.horizontalHeader().setVisible(False)
        # 垂直表格头显示和隐藏
        self.tw_strategy_list.verticalHeader().setVisible(False)
        # 隐藏分割线
        self.tw_strategy_list.setShowGrid(False)
        # 隐藏滚动条
        self.tw_strategy_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.tw_strategy_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tw_strategy_list.setColumnCount(1)
        self.tw_strategy_list.setSelectionMode(QAbstractItemView.SingleSelection)

        # 搜索功能初始化
        self.search_history = []
        self.search_keyword = ""
        self.match_indices = []
        self.last_search_pos = -1  # 跟踪最后搜索的位置

        # 绑定搜索按钮事件
        self.search_button.clicked.connect(self.search_next)
        # 绑定输入框回车事件
        self.search_input.returnPressed.connect(self.search_next)

        # 为输入框添加历史记录功能
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.search_input.setCompleter(QCompleter(self.search_history))
        self.search_input.completer().setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    def on_tw_strategy_list_itemSelectionChanged(self):
        if not self.is_lock:
            # 获取选中的项
            self.parent().window_equip.setVisible(True)
            # self.parent().window_location.setVisible(True)
            # self.parent().window_early.setVisible(False)
            self.parent().window_set.cb_equip.setChecked(True)
            # self.parent().window_set.cb_location.setChecked(True)

            self.tw_strategy_list.cellWidget(self.tw_strategy_list.currentIndex().row(),0).update_item(setting.mode)


    def set_ui(self):
        pass
    def add_team(self,strategy=None):
        #增加一行
        new_row_index = self.tw_strategy_list.rowCount()
        self.tw_strategy_list.insertRow(new_row_index)
        item_strategy = ItemStrategy(self)
        item_strategy.set_strategy(strategy)
        self.tw_strategy_list.setCellWidget(new_row_index,0 , item_strategy)
    def set_teams(self,strategy_list:list):
        '''
        设置队伍
        :param chess_datas:
        :return:
        '''

        if len(strategy_list)==0:
            return
        # 清空列表
        self.is_lock=True
        self.tw_strategy_list.setRowCount(0)
        self.tw_strategy_list.clear()
        for item in strategy_list:
            self.add_team(item)
        self.is_lock = False
        # 重置搜索状态
        self.reset_search_state()
    def test(self):
        '''
        测试展示
        :return:
        '''
        for i in range(10):
            self.add_team(None)

    def on_search_text_changed(self, text):
        '''
        搜索文本变化时的处理
        :param text:
        :return:
        '''
        # 当文本变化时，只更新自动完成，不立即重置搜索状态
        # 搜索状态会在点击搜索按钮或按回车时重置
        completer = self.search_input.completer()
        if completer:
            model = completer.model()
            model.setStringList(self.search_history)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

    def reset_search_state(self):
        '''
        重置搜索状态
        :return:
        '''
        self.match_indices = []
        self.search_keyword = ""

    def search_next(self):
        '''
        查找下一个匹配项
        :return:
        '''
        keyword = self.search_input.text().strip()
        if not keyword:
            return

        # 如果关键词变化，重置搜索状态并重新搜索
        if keyword != self.search_keyword:
            self.search_keyword = keyword
            self.last_search_pos = -1  # 重置搜索位置
            # 添加到搜索历史
            if keyword not in self.search_history:
                self.search_history.append(keyword)
                # 更新自动完成
                self.search_input.setCompleter(QCompleter(self.search_history))
                self.search_input.completer().setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # 获取当前选中的行索引作为起始点
        current_row = self.tw_strategy_list.currentRow()
        
        # 如果是第一次搜索或者当前行不是有效行，从0开始搜索
        start_row = 0
        if current_row >= 0 and self.search_keyword != "":
            # 从当前选中行的下一行开始搜索
            start_row = current_row + 1

        # 查找第一个匹配项
        row_index = self.find_first_match(keyword, start_row)
        
        # 如果从start_row开始没找到，再从0开始查找（循环查找）
        if row_index is None and start_row > 0:
            row_index = self.find_first_match(keyword, 0)
            if row_index is not None:
                # 显示提示信息，表明已经循环到开始
                #QMessageBox.information(self, "提示", "已经找到最后一个匹配项，现在从开始处继续查找。")
                pass
        
        if row_index is None:
            #QMessageBox.information(self, "提示", f"没有找到包含'{keyword}'的项。")
            return
        
        # 更新最后搜索位置
        self.last_search_pos = row_index
        # 确保行可见
        item = self.tw_strategy_list.item(row_index, 0)
        if item:
            self.tw_strategy_list.scrollToItem(item)
        # 选中行
        self.tw_strategy_list.selectRow(row_index)
        # 确保单元格有焦点
        self.tw_strategy_list.setCurrentCell(row_index, 0)
        # 触发项目选择更改事件
        self.on_tw_strategy_list_itemSelectionChanged()

    def find_first_match(self, keyword, start_row=0):
        '''
        查找第一个匹配的项
        :param keyword: 搜索关键词，可以包含空格分隔的多个条件
        :param start_row: 起始行索引
        :return: 匹配的行索引，如果没有匹配项则返回None
        '''
        # 解析关键词为条件列表
        conditions = keyword.lower().split()
        if not conditions:
            return None
    
        # 先从start_row开始查找
        for row in range(start_row, self.tw_strategy_list.rowCount()):
            item_widget = self.tw_strategy_list.cellWidget(row, 0)
            if hasattr(item_widget, 'strategy') and item_widget.strategy:
                strategy = item_widget.strategy
                all_conditions_met = True

                # 对每个条件进行检查
                for cond in conditions:
                    condition_met = False
                    name_part = cond
                    # 处理普通条件
                    # 检查阵容名
                    if 'detail' in strategy and 'line_name' in strategy['detail']:
                        if name_part in strategy['detail']['line_name'].lower():
                            condition_met = True
                    
                    # 检查英雄名
                    if not condition_met and 'detail' in strategy and 'hero_location' in strategy['detail']:
                        for hero_item in strategy['detail']['hero_location']:
                            if hero_item['chess_type'] == 'hero':
                                hero_id = hero_item['hero_id']
                                # 尝试获取英雄名称（支持模式1和模式2）
                                hero_name = tft_instance.chess_id_to_name(hero_id, mode=1)
                                
                                if not hero_name:
                                    hero_name = tft_instance.chess_id_to_name2(hero_id, mode=1)
                                if hero_name and name_part in hero_name.lower():
                                    condition_met = True
                                    break

                    # 检查职业和羁绊名称
                    if not condition_met and 'detail' in strategy and 'hero_location' in strategy['detail']:
                        # 获取所有英雄的职业和羁绊
                        job_ids = set()
                        race_ids = set()
                        for hero_item in strategy['detail']['hero_location']:
                            if hero_item['chess_type'] == 'hero':
                                hero_id = hero_item['hero_id']
                                # 获取英雄数据
                                chess_data = chessId_get_data(tft_instance.chess_list, hero_id)
                                if chess_data:
                                    # 添加职业
                                    if 'jobIds' in chess_data and chess_data['jobIds']:
                                        job_ids.update(chess_data['jobIds'].split(','))
                                    # 添加羁绊
                                    if 'raceIds' in chess_data and chess_data['raceIds']:
                                        race_ids.update(chess_data['raceIds'].split(','))

                        # 检查职业名称
                        for job_id in job_ids:
                            if job_id:
                                job_data = tft_instance.get_job_or_race_data(job_id, 1, 'job', mode=1)
                                if job_data and len(job_data) >= 3 and 'name' in job_data[2] and name_part in job_data[2]['name'].lower():
                                    condition_met = True
                                    break

                        # 检查羁绊名称
                        if not condition_met:
                            for race_id in race_ids:
                                if race_id:
                                    race_data = tft_instance.get_job_or_race_data(race_id, 1, 'race', mode=1)
                                    if race_data and len(race_data) >= 3 and 'name' in race_data[2] and name_part in race_data[2]['name'].lower():
                                        condition_met = True
                                        break

                    # 如果任何一个条件不满足，则整行不匹配
                    if not condition_met:
                        all_conditions_met = False
                        break

                # 如果所有条件都满足，则返回当前行
                if all_conditions_met:
                    return row

        # 如果从start_row开始没找到，再从0开始查找（循环查找）
        if start_row > 0:
            for row in range(0, start_row):
                item_widget = self.tw_strategy_list.cellWidget(row, 0)
                if hasattr(item_widget, 'strategy') and item_widget.strategy:
                    strategy = item_widget.strategy
                    all_conditions_met = True

                    # 对每个条件进行检查
                    for cond in conditions:
                        condition_met = False
                        # 处理普通条件
                        name_part = cond
                        # 检查阵容名
                        if 'detail' in strategy and 'line_name' in strategy['detail']:
                            if name_part in strategy['detail']['line_name'].lower():
                                condition_met = True

                        # 检查英雄名
                        if not condition_met and 'detail' in strategy and 'hero_location' in strategy['detail']:
                            for hero_item in strategy['detail']['hero_location']:
                                if hero_item['chess_type'] == 'hero':
                                    hero_id = hero_item['hero_id']
                                    # 尝试获取英雄名称（支持模式1和模式2）
                                    hero_name = tft_instance.chess_id_to_name(hero_id, mode=1)

                                    if not hero_name:
                                        hero_name = tft_instance.chess_id_to_name2(hero_id, mode=1)
                                    if hero_name and name_part in hero_name.lower():
                                        condition_met = True
                                        break

                        # 检查职业和羁绊名称
                        if not condition_met and 'detail' in strategy and 'hero_location' in strategy['detail']:
                            # 获取所有英雄的职业和羁绊
                            job_ids = set()
                            race_ids = set()
                            for hero_item in strategy['detail']['hero_location']:
                                if hero_item['chess_type'] == 'hero':
                                    hero_id = hero_item['hero_id']
                                    # 获取英雄数据
                                    chess_data = chessId_get_data(tft_instance.chess_list, hero_id)
                                    if chess_data:
                                        # 添加职业
                                        if 'jobIds' in chess_data and chess_data['jobIds']:
                                            job_ids.update(chess_data['jobIds'].split(','))
                                        # 添加羁绊
                                        if 'raceIds' in chess_data and chess_data['raceIds']:
                                            race_ids.update(chess_data['raceIds'].split(','))

                            # 检查职业名称
                            for job_id in job_ids:
                                if job_id:
                                    job_data = tft_instance.get_job_or_race_data(job_id, 1, 'job', mode=1)
                                    if job_data and len(job_data) >= 3 and 'name' in job_data[2] and name_part in job_data[2]['name'].lower():
                                        condition_met = True
                                        break

                            # 检查羁绊名称
                            if not condition_met:
                                for race_id in race_ids:
                                    if race_id:
                                        race_data = tft_instance.get_job_or_race_data(race_id, 1, 'race', mode=1)
                                        if race_data and len(race_data) >= 3 and 'name' in race_data[2] and name_part in race_data[2]['name'].lower():
                                            condition_met = True
                                            break

                        # 如果任何一个条件不满足，则整行不匹配
                        if not condition_met:
                            all_conditions_met = False
                            break

                    # 如果所有条件都满足，则返回当前行
                    if all_conditions_met:
                        return row
                             
                    # 检查英雄名
                    if 'detail' in strategy and 'hero_location' in strategy['detail']:
                        for hero_item in strategy['detail']['hero_location']:
                            if hero_item['chess_type'] == 'hero':
                                hero_id = hero_item['hero_id']
                                # 尝试获取英雄名称（支持模式1和模式2）
                                hero_name = tft_instance.chess_id_to_name(hero_id, mode=1)
                                
                                if not hero_name:
                                    hero_name = tft_instance.chess_id_to_name2(hero_id, mode=1)
                                if hero_name and keyword in hero_name.lower():
                                    return row

                    # 直接检查职业和羁绊（不依赖get_job_and_race_name）
                    if 'detail' in strategy and 'hero_location' in strategy['detail']:
                        # 获取所有英雄的职业和羁绊
                        job_ids = set()
                        race_ids = set()
                        for hero_item in strategy['detail']['hero_location']:
                            if hero_item['chess_type'] == 'hero':
                                hero_id = hero_item['hero_id']
                                # 获取英雄数据
                                chess_data = chessId_get_data(tft_instance.chess_list, hero_id)
                                if chess_data:
                                    # 添加职业
                                    if 'jobIds' in chess_data and chess_data['jobIds']:
                                        job_ids.update(chess_data['jobIds'].split(','))
                                    # 添加羁绊
                                    if 'raceIds' in chess_data and chess_data['raceIds']:
                                        race_ids.update(chess_data['raceIds'].split(','))

                        # 检查职业名称
                        for job_id in job_ids:
                            if job_id:
                                job_data = tft_instance.get_job_or_race_data(job_id, 1, 'job', mode=1)
                                if job_data and len(job_data) >= 3 and 'name' in job_data[2] and keyword in job_data[2]['name'].lower():
                                    return row

                        # 检查羁绊名称
                        for race_id in race_ids:
                            if race_id:
                                race_data = tft_instance.get_job_or_race_data(race_id, 1, 'race', mode=1)
                                if race_data and len(race_data) >= 3 and 'name' in race_data[2] and keyword in race_data[2]['name'].lower():
                                    return row

        return None


