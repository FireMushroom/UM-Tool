import sys
from UMHelper2 import Ui_MainWindow
import os.path
from functools import partial
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QMenu, QAction
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QBitmap
import math
from PyQt5.QtCore import QSize, Qt
import re
import pandas as pd
from MyCustomWidget import OneButtonOneLabel

class MainWindow(QMainWindow):
    def __init__(self, parent=None):    
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.m_flag = False
        self.setup_excel_data()
        self.btn_ind = [-2 for i in range(self.page_info_num)] #当前按钮编号
        self.f_relic_no = -1 #合成圣物1
        self.l_relic_no = -1 #合成圣物2
        
        #绑定左侧按钮的槽函数
        for i in range(self.page_info_num + 1):
            #使用partial函数给槽赋固定变量的值
            self.ui.menu_btn_list[i].clicked.connect(partial(self.ui.stackedWidget.setCurrentIndex, i))
        #左右按钮的槽函数连接，需要更新修改
        self.ui.page_info_li[0].btn_left.clicked.connect(lambda:self.show_table_info(ind = 0, btn_ind = self.btn_ind[0] - 1))
        self.ui.page_info_li[0].btn_right.clicked.connect(lambda:self.show_table_info(ind = 0, btn_ind = self.btn_ind[0] + 1))
        self.ui.page_info_li[1].btn_left.clicked.connect(lambda:self.show_table_info(ind = 1, btn_ind = self.btn_ind[1] - 1))
        self.ui.page_info_li[1].btn_right.clicked.connect(lambda:self.show_table_info(ind = 1, btn_ind = self.btn_ind[1] + 1))
        self.ui.page_info_li[2].btn_left.clicked.connect(lambda:self.show_table_info(ind = 2, btn_ind = self.btn_ind[2] - 1))
        self.ui.page_info_li[2].btn_right.clicked.connect(lambda:self.show_table_info(ind = 2, btn_ind = self.btn_ind[2] + 1))        
        self.ui.page_info_li[3].btn_left.clicked.connect(lambda:self.show_table_info(ind = 3, btn_ind = self.btn_ind[3] - 1))
        self.ui.page_info_li[3].btn_right.clicked.connect(lambda:self.show_table_info(ind = 3, btn_ind = self.btn_ind[3] + 1))       
        self.ui.page_info_li[4].btn_left.clicked.connect(lambda:self.show_table_info(ind = 4, btn_ind = self.btn_ind[4] - 1))
        self.ui.page_info_li[4].btn_right.clicked.connect(lambda:self.show_table_info(ind = 4, btn_ind = self.btn_ind[4] + 1))  
        self.btn_list = [[] for i in range(self.page_info_num)]
        self.pixmap = QPixmap("./images/UI_BookProps1.png")
        self.bix = QBitmap(QPixmap("./images/UI_BookProps_mask.png").scaled(self.size()))
        self.setMask(self.bix)
        
    def setup_excel_data(self):
        self.pages_name = ["Relics", "Potions", "Blessings", "Curses", "Familiars"]
        #新表格登记处,需要更新修改
        self.page_info_num = len(self.pages_name)
        self.info_table_list = [] #记录表格信息
        for excel in self.pages_name:
            self.info_table_list.append(pd.read_excel("./resources/" + excel + ".xlsx", keep_default_na=False, engine='openpyxl'))
        self.table_num = [] #记录各表格项目数
        for i in range(len(self.info_table_list)):
            self.table_num.append(self.info_table_list[i].shape[0])   
        

    #-------------------事件重写--------------------
    #绘制背景图片    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setOpacity(0.8)
        painter.drawPixmap(self.rect(), self.pixmap)
        
    #支持拖拽    
    def mousePressEvent(self, evt):    
        #判定标记、左键
        if evt.button() == Qt.LeftButton:
            self.m_flag = True 
        #获取两个点
            self.mouse_x = evt.globalX()
            self.mouse_y= evt.globalY()
            self.origin_x = self.x()
            self.origin_y= self.y()
        
    def mouseMoveEvent(self, evt):
        #判断标记
        if self.m_flag:
        #计算移动向量
            move_x = evt.globalX() - self.mouse_x
            move_y = evt.globalY() - self.mouse_y
            dest_x = self.origin_x + move_x
            dest_y = self.origin_y + move_y
        #移动窗口
            self.move(dest_x, dest_y)
            
    def mouseReleaseEvent(self, evt):
        #重置标记
        self.m_flag = False
        
    #-------------------事件重写完毕--------------------
    
    #设置排序按钮菜单    
    def set_menu(self, ind):
        menu = QMenu(self.ui.page_li[ind])
        action_list = []
        action_list.append(QAction(QIcon("./images/UI_Mushroom.png"), "按编号排序(默认)", menu))
        action_list[0].triggered.connect(partial(self.sort_table, ind, sort_by=""))
        selections = {"rarity":["稀有度","btn_2.png"],"is_unique":["独特圣物","ExclamationYellow.png"],\
                      "shop_cost":["商店价值","GoldIcon.png"],"unlock_cost":["解锁价格","Thorium.png"]}
        title_list = list(self.info_table_list[ind].columns)
        i = 1
        for selection in selections.keys():
            if selection in title_list:
                action_list.append(QAction(QIcon(f"./images/{selections[selection][1]}"), f"按{selections[selection][0]}排序", menu))
                action_list[i].triggered.connect(partial(self.sort_table, ind, sort_by=selection))
                i += 1
        for action in action_list:
            menu.addAction(action)
        self.ui.page_li[ind].sort_btn.setMenu(menu)
        
    #设置表格按商店金额排序    
    def sort_table(self, ind, sort_by=""):
        id_list = ["relic", "potion", "blessing", "curse", "familiar"]
        if sort_by == "":
            self.info_table_list[ind].sort_index(inplace=True)
        elif sort_by == "rarity":
            if ind == 0:
                self.info_table_list[ind].sort_values(by=["major_curse_cost", "minor_curse_cost", "synthetic_cost", "rarity", f"{id_list[ind]}_id"], ascending=[False, False, False, False, True], inplace=True)
            elif ind == 1:
                self.info_table_list[ind].sort_values(by=["major_curse_cost", "minor_curse_cost", "rarity", f"{id_list[ind]}_id"], ascending=[False, False, False, True], inplace=True)
            else:
                self.info_table_list[ind].sort_values(by=["rarity", f"{id_list[ind]}_id"], ascending=[False, True], inplace=True)
        else:
            self.info_table_list[ind].sort_values(by=[sort_by, f"{id_list[ind]}_id"], ascending=[False, True], inplace=True)
        selections = {"shop_cost":1,"unlock_cost":2,"rarity":3}
        if sort_by in selections.keys():
            self.update_pages(ind, selections[sort_by])
        else:
            self.update_pages(ind)

    #根据中文名称查询圣物编号或圣物英文名
    def get_table_info(self, ind, chi_name, need_eng=False):    
        chi_name_list = list(self.info_table_list[ind]["chinese_name"])
        relic_no = chi_name_list.index(chi_name) 
        if not need_eng:
            return relic_no
        else:
            eng_name_list = self.info_table_list[ind]["english_name"].values
            return eng_name_list[relic_no]
    
    #加载圣物查询界面的图像(可以在名字下方附加几个信息按钮)
    def update_pages(self, ind, flag=0):
        self.ui.page_li[ind].tableWidget.clear() #清空表格
        self.btn_list[ind] = [] #清空按钮列表
        row_n = math.ceil(self.table_num[ind] / 5)#圣物呈现行数，每行5个,有一行是表头
        self.ui.page_li[ind].tableWidget.setRowCount(row_n)
        self.ui.page_li[ind].tableWidget.setColumnCount(5)
        w = self.ui.page_li[ind].tableWidget.width() / 5 - 5 #留给滚动条余地
        for j in range(row_n):
            self.ui.page_li[ind].tableWidget.setRowHeight(j, w + 20*((flag + 3) // 2)) #flag=1,2加一行，3再加一行
        for j in range(5):
            self.ui.page_li[ind].tableWidget.setColumnWidth(j, w)
        #以表格中的英文名和稀有度加载圣物图片
        title_list = list(self.info_table_list[ind].columns)
        if "rarity" in title_list:
            rar_n = 0
            rar_n_list = self.info_table_list[ind]["rarity"].values#稀有度
        else:
            rar_n = -1            
        eng_n_list = self.info_table_list[ind]["english_name"].values#获取英文名列的所有英文名
        chi_n_list = self.info_table_list[ind]["chinese_name"].values#中文名
        
        selections = {0:[], 1:["./images/GoldIcon.png"],2:["./images/Thorium.png"],\
                      3:["./images/Major Curse.png","./images/Minor Curse.png"]}
        if flag == 1:
            g_c_list = self.info_table_list[ind]["shop_cost"].values
        elif flag == 2:
            u_c_list = self.info_table_list[ind]["unlock_cost"].values
        elif flag == 3 and ind <= 1:
            maj_list = self.info_table_list[ind]["major_curse_cost"].values
            min_list = self.info_table_list[ind]["minor_curse_cost"].values
            
        for j, it in enumerate(eng_n_list):
            if flag == 1:
                btn_text = [str(g_c_list[j])]
            elif flag == 2:
                btn_text = [str(u_c_list[j])]
            elif flag == 3 and ind <= 1:
                btn_text = [str(maj_list[j]),str(min_list[j])]
            else:
                btn_text = []
            pic_path = f"./images/{self.pages_name[ind]}/{it}.png"
            #图片有效性判断交给MyCustomWidget
            if rar_n != -1:
                self.btn_list[ind].append(OneButtonOneLabel(self.ui.page_li[ind].tableWidget,\
                 j, pic_path, self.get_rarity_color(rar_n_list[j]), chi_n_list[j], btn_pic=selections[flag], btn_text=btn_text))
            else:
                self.btn_list[ind].append(OneButtonOneLabel(self.ui.page_li[ind].tableWidget,\
                 j, pic_path, "black", chi_n_list[j], btn_pic=selections[flag], btn_text=btn_text))  
            self.ui.page_li[ind].tableWidget.setCellWidget(j // 5, j % 5, self.btn_list[ind][j])
            self.btn_list[ind][j].btn.clicked.connect(partial(self.show_table_info, ind, btn_ind=-2))#不设lambda的话，参数会传False
            
    #输入字母，返回稀有度文本
    @staticmethod
    def get_rarity_text(rarity):
        if rarity == "C":
            raritytext = "普通"
        elif rarity == "R":
            raritytext = "稀有"
        elif rarity == "L":
            raritytext = "传说"
        else:
            raritytext = "未知"
        return raritytext
    #输入字母，返回稀有度颜色
    @staticmethod
    def get_rarity_color(rarity):
        if rarity == "C":
            raritycolor = "white"
        elif rarity == "R":
            raritycolor = "yellow"
        elif rarity == "L":
            raritycolor = "red"
        else:
            raritycolor = "black"
        return raritycolor
    
    #输入html字符串，返回加工后的字符串文本
    @staticmethod
    def get_styled_text(text):
        new_text = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <style type="text/css">
            .color-pink-03{
                color: #ee230d;
            }<!10分>
            .color-pink-02 {
                color: #ff654e;
            }<!9分>
            .color-pink-01 {
                color: #ff968d;
            }<!8分>
            .color-yellow-04 {
                color: #ff9201;
            }<!祝福橙7分>
            .color-yellow-03 {
                color: #f8ba00;
            }<!6分>
            .color-green-03 {
                color: #1db100;
            }<!怪物绿>
            .color-green-02 {
                color: #60d837;
            }<!负面效果绿5分>
            .color-purple-04 {
                color: #99195e;
            }<!诅咒紫>
            .color-blue-02 {
                color: #02a2ff;
            }<!药水蓝，4分>
            .color-blue-01 {
                color: #56c1fe;
            }<!3分>
            .color-gray-03 {
                color: #5f5f5f;
            }<!2分>
            .color-gray-02 {
                color: #929292;
            }<!1分>
            .color-gray-01 {
                color: #000000;
            }<!0分>
            .font-size-16 {
                font-size: 15px;
            }
            .font-size-20 {
                font-size: 20px;
            }
        </style>
        </head>
        <body>
        """ + text + """
        </body>
        </html>
        """
        return new_text
    
    #检查指定评分文本来变化颜色
    @staticmethod
    def get_colored_text(text):
        res = re.findall(r"\d+分", text)
        color_dic = {"0分":"color-gray-01", "1分":"color-gray-02", "2分":"color-gray-03",\
                "3分":"color-blue-01", "4分":"color-blue-02", "5分":"color-green-02",\
                "6分":"color-yellow-03", "7分":"color-yellow-04", "8分":"color-pink-01",\
                "9分":"color-pink-02", "10分":"color-pink-03"}
        for item in res: 
            new_item = f"<span class={color_dic[item]}>{item}</span>"
            text = text.replace(item, new_item)
        new_text = MainWindow.get_styled_text(f"<p><strong>{text}</strong></p>")
        return new_text
    
    #获取物品坐标，更新页面信息,默认为无
    def show_table_info(self, ind, btn_ind):
        if btn_ind == -2: #从圣物列表页获取圣物详情页
            sendbtn = self.sender()
            self.btn_ind[ind] = sendbtn.index
        else: #通过圣物详情页左右翻页
            self.btn_ind[ind] = btn_ind % self.table_num[ind]
            
        #根据按钮序号(从0开始)获取详细信息
        btn_no = self.btn_ind[ind]
        relic_info_list = list(self.info_table_list[ind].iloc[btn_no])
        #固定地，表格第0~2列是id、中文名称、英文名称
        self.ui.page_info_li[ind].tableWidget.setItem(1, 1, QTableWidgetItem(str(relic_info_list[0])))
        name = relic_info_list[1]
        self.ui.page_info_li[ind].lab_name.setText(name)#圣物详情页上方圣物名
        english_name = relic_info_list[2]
        rarity = "" #默认稀有度为空，便于图片颜色的判断
        #根据表头名称确定表格隐藏哪些内容(评分栏之后另算)
        #表格中可能需要隐藏的行名称（以及对应的行号）
        optional_list = ["rarity", "type", "is_unique", "shop_cost", "unlock_cost", "synthetic_cost", "major_curse_cost", "leveling_up_by"]
        optional_rowno_list = [2, 3, 5, 6, 7, 10, 8, 12]
        for i in range(2, 13):            
            self.ui.page_info_li[ind].tableWidget.hideRow(i) #隐藏
        self.ui.page_info_li[ind].effect_frame.hide()
        self.ui.page_info_li[ind].tab_effect.hide()
        self.ui.page_info_li[ind].comment_frame.hide()
        self.ui.page_info_li[ind].score_frame.hide()
        self.ui.page_info_li[ind].dang_and_disc_frame.hide()     
           
        title_list = list(self.info_table_list[ind].columns)
        for i in range(3, len(title_list)): #根据表头填内容(去除id、中英文项)
            if title_list[i] == "rarity":
                rarity = relic_info_list[i]
                self.ui.page_info_li[ind].tableWidget.setItem(optional_rowno_list[0], 1, QTableWidgetItem(self.get_rarity_text(rarity)))
                self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[0])
            elif title_list[i] == "type":
                self.ui.page_info_li[ind].tableWidget.setItem(optional_rowno_list[1], 1, QTableWidgetItem(relic_info_list[i]))
                self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[1])
            elif title_list[i] == "unlock_method":
                unlock_method = relic_info_list[i]
                self.ui.page_info_li[ind].tableWidget.setItem(4, 1, QTableWidgetItem(unlock_method))
                self.ui.page_info_li[ind].tableWidget.showRow(4)
            elif title_list[i] == "is_unique":
                is_unique = relic_info_list[i]            
                btn2 = QtWidgets.QCheckBox(is_unique, self.ui.page_info_li[ind].tableWidget)
                if is_unique != "否":
                    btn2.setChecked(True)
                else:
                    btn2.setChecked(False)
                btn2.setEnabled(False)
                self.ui.page_info_li[ind].tableWidget.setCellWidget(optional_rowno_list[2], 1, btn2)
                self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[2])
            elif title_list[i] == "shop_cost":
                shop_cost = int(relic_info_list[i])
                if shop_cost != 0:
                    self.ui.page_info_li[ind].tableWidget.setItem(optional_rowno_list[3], 1, QTableWidgetItem(QIcon("./images/GoldIcon.png"),str(shop_cost)))
                    self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[3])
            elif title_list[i] == "unlock_cost":
                unlock_cost = int(relic_info_list[i])
                if unlock_cost != 0:
                    self.ui.page_info_li[ind].tableWidget.setItem(optional_rowno_list[4], 1, QTableWidgetItem(QIcon("./images/Thorium.png"),str(unlock_cost)))
                    self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[4])
            elif title_list[i] == "synthetic_cost":
                if relic_info_list[i] != "":
                    temp_li = relic_info_list[i].split(",")
                    self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[5])
                    self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[5]+1)        
                    f_relic = temp_li[0] #同时拥有XXX和XXX
                    l_relic = temp_li[1]
                    self.f_relic_no = self.get_table_info(ind, f_relic)
                    f_relic_name = self.get_table_info(ind, f_relic, True)
                    self.l_relic_no = self.get_table_info(ind, l_relic)
                    l_relic_name = self.get_table_info(ind, l_relic, True)
                    self.f_btn = QtWidgets.QPushButton(QIcon(f"./images/{self.pages_name[ind]}/{f_relic_name}.png"),"",self.ui.page_info_li[ind].tableWidget)            
                    self.f_btn.setIconSize(QtCore.QSize(64, 64))
                    self.f_btn.setCursor(QtGui.QCursor(QtGui.QPixmap("./images/Ellipses_5.png").scaled(40, 30)))
                    self.l_btn = QtWidgets.QPushButton(QIcon(f"./images/{self.pages_name[ind]}/{l_relic_name}.png"),"",self.ui.page_info_li[ind].tableWidget)            
                    self.l_btn.setIconSize(QtCore.QSize(64, 64))
                    self.l_btn.setCursor(QtGui.QCursor(QtGui.QPixmap("./images/Ellipses_5.png").scaled(40, 30)))
                    self.f_btn.setStyleSheet('background: rgba(255,255,255,0.5);')
                    self.l_btn.setStyleSheet('background: rgba(255,255,255,0.5);')
                    self.f_btn.setFlat(True)
                    self.l_btn.setFlat(True)                
                    self.f_btn.clicked.connect(lambda: self.show_table_info(ind, self.f_relic_no))
                    self.l_btn.clicked.connect(lambda: self.show_table_info(ind, self.l_relic_no))
                    self.ui.page_info_li[ind].tableWidget.setCellWidget(optional_rowno_list[5], 1, self.f_btn)
                    self.ui.page_info_li[ind].tableWidget.setCellWidget(optional_rowno_list[5]+1, 1, self.l_btn)
            elif title_list[i] == "major_curse_cost":   
                if relic_info_list[i] != "":         
                    self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[6])
                    self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[6]+1)
                    mj_cost = relic_info_list[i]
                    mn_cost = relic_info_list[i+1]
                    self.ui.page_info_li[ind].tableWidget.setItem(optional_rowno_list[6], 1, QTableWidgetItem(QIcon("./images/Major Curse.png"), str(int(mj_cost))))
                    self.ui.page_info_li[ind].tableWidget.setItem(optional_rowno_list[6]+1, 1, QTableWidgetItem(QIcon("./images/Minor Curse.png"), str(int(mn_cost))))
            elif title_list[i] == "leveling_up_by":            
                self.ui.page_info_li[ind].tableWidget.setItem(optional_rowno_list[7], 1, QTableWidgetItem(relic_info_list[i]))
                self.ui.page_info_li[ind].tableWidget.showRow(optional_rowno_list[7])    
            elif title_list[i] == "effect":      
                self.ui.page_info_li[ind].text_effect.setHtml(self.get_styled_text(relic_info_list[i]))
                self.ui.page_info_li[ind].effect_frame.show()
            elif title_list[i] == "level1_effect_name":
                self.ui.page_info_li[ind].tab_label[0].setText(relic_info_list[i])
                self.ui.page_info_li[ind].tab_effect.show()
            elif title_list[i] == "level2_effect_name":
                self.ui.page_info_li[ind].tab_label[1].setText(relic_info_list[i])
            elif title_list[i] == "level3_effect_name":
                self.ui.page_info_li[ind].tab_label[2].setText(relic_info_list[i])
            elif title_list[i] == "level1_effect":
                self.ui.page_info_li[ind].tab_text[0].setHtml(self.get_styled_text(relic_info_list[i]))
            elif title_list[i] == "level2_effect":
                self.ui.page_info_li[ind].tab_text[1].setHtml(self.get_styled_text(relic_info_list[i]))
            elif title_list[i] == "level3_effect":
                self.ui.page_info_li[ind].tab_text[2].setHtml(self.get_styled_text(relic_info_list[i]))
            elif title_list[i] == "comment":      
                self.ui.page_info_li[ind].text_comment.setHtml(self.get_styled_text(relic_info_list[i]))
                self.ui.page_info_li[ind].comment_frame.show()
            elif title_list[i] == "score":   
                self.ui.page_info_li[ind].lab_score_content.setText(self.get_colored_text(relic_info_list[i]))
                self.ui.page_info_li[ind].score_frame.show()          
            elif title_list[i] == "danger":   
                self.ui.page_info_li[ind].lab_danger_content.setText(self.get_colored_text(relic_info_list[i]))
            elif title_list[i] == "discomfort":   
                self.ui.page_info_li[ind].lab_discomfort_content.setText(self.get_colored_text(relic_info_list[i]))
                self.ui.page_info_li[ind].dang_and_disc_frame.show() 
        #圣物详情页的图片按钮
        pic_path = f"./images/{self.pages_name[ind]}/{english_name}.png"
        if not os.path.isfile(pic_path): #不存在路径则填充空白图
            pic_path = "./images/UI_Blank.png"
        btn = QtWidgets.QPushButton(QIcon(pic_path), "", self.ui.page_info_li[ind].tableWidget)            
        btn.setIconSize(QSize(95, 95))
        style_btn = f'''QPushButton{{
        border: 5px solid {self.get_rarity_color(rarity)};
        margin: 3px; 
        border-radius: 8px;
        background: rgba(255,255,255,0.5);
        }}'''
        btn.setStyleSheet(style_btn)
        self.ui.page_info_li[ind].tableWidget.setCellWidget(0, 0, btn)
        self.ui.page_info_li[ind].tableWidget.setRowHeight(0, 105)

        self.ui.stackedWidget.setCurrentIndex(1 + ind + self.page_info_num) #跳转至详情页
        #self.btn_list[0][0].btnClick_signal.connect(lambda idx: print("idx:",idx))
        
if __name__=="__main__":  
    app = QApplication(sys.argv)  
    win = MainWindow()
    #加载qss样式表
    styleFile = './resources/mystyle.qss'
    with open(styleFile,'r',encoding='UTF-8') as f: #默认GBK编码会失效
        qssStyle = f.read()
    win.setStyleSheet(qssStyle)
    win.show()  
    #增加页面时需要更新
    for i in range(len(win.pages_name)):
        win.update_pages(i)
        win.set_menu(i)
    sys.exit(app.exec_())  