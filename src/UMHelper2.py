# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QColor, QBrush, QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal

#加载窗口UI类
class Ui_MainWindow(object):
    class ItemListPage(QWidget):
        """
        :description: 建立一个列表项的页面类，包含一个标题和一个不可编辑的二维表
        """
        def __init__(self, parent, title):
            super().__init__(parent)      
            self.page = QtWidgets.QWidget()
            self.page.setProperty("level", "page_list")
            #设置圣物页标题样式
            self.label = QtWidgets.QLabel(self.page)
            self.label.setProperty("level", "label_list_title")
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setText(title)
            self.label.setScaledContents(True)
            #圣物列表
            self.tableWidget = QtWidgets.QTableWidget(self.page)
            self.tableWidget.setFixedSize(600, 580)
            self.tableWidget.setProperty("level", "table_list")
            #表格全透明，全隐藏，不可选
            Ui_MainWindow.set_tablewidget_style_sheet(self.tableWidget, bg_transparent=0)
            self.vbox = QtWidgets.QVBoxLayout(self.page)
            self.vbox.addWidget(self.label, 1)
            self.vbox.addWidget(self.tableWidget, 12, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
            self.sort_btn = QtWidgets.QPushButton("排序方式", self.page)
            self.sort_btn.setProperty("level", "btn_of_main_function")
            self.sort_btn.setGeometry(QtCore.QRect(40, 15, 120, 40))
            self.sort_btn.raise_()
        
    class ItemDetailPage:
        """
        :description: 建立一个详情项的页面类，包含一个左侧的缩略信息表、一个右侧的详细信息表和上侧的翻页栏
        """
        def __init__(self): 
            #记录圣物页面整体透明度
            self.opacity = 0.6 
            self.page = QtWidgets.QWidget()
            self.page.setProperty("level", "page_detail")
            self.page.setGeometry(QtCore.QRect(0, 0, 531, 511))
            self.page.setContentsMargins(0, 10, 40, 40)
            self.init_upper_bar()
            self.init_left_table()
            self.init_right_info()
            self.lowerLayout = QtWidgets.QHBoxLayout()
            self.lowerLayout.setObjectName("lowerLayout")
            self.lowerLayout.addWidget(self.tableWidget,1)
            self.lowerLayout.addLayout(self.infoLayout,2)
            self.pageVLayout = QtWidgets.QVBoxLayout(self.page)
            self.pageVLayout.setContentsMargins(0, 0, 0, 0)
            self.pageVLayout.setObjectName("pageVLayout")
            self.pageVLayout.addLayout(self.upperLayout)
            self.pageVLayout.addLayout(self.lowerLayout)
        #最上边的横条 
        def init_upper_bar(self):
            self.btn_return = QtWidgets.QPushButton(QIcon("./images/UI_Return.png"), "返回", self.page)
            self.btn_return.setProperty("level", "btn_of_main_function")
            self.btn_return.setIconSize(QtCore.QSize(40, 40))
            self.btn_left = QtWidgets.QPushButton(QIcon("./images/UI_LeftArrow.png"), "", self.page)
            self.btn_left.setProperty("level", "btn_of_main_function")
            self.btn_left.setIconSize(QtCore.QSize(40, 40))
            self.lab_name = QtWidgets.QLabel(self.page)
            self.lab_name.setProperty("level", "label_info_name")
            self.lab_name.setAlignment(QtCore.Qt.AlignCenter)
            self.btn_right = QtWidgets.QPushButton(QIcon("./images/UI_RightArrow.png"), "", self.page)
            self.btn_right.setProperty("level", "btn_of_main_function")
            self.btn_right.setIconSize(QtCore.QSize(40, 40))
            self.upperLayout = QtWidgets.QHBoxLayout()
            self.upperLayout.setObjectName("upperLayout")
            self.upperLayout.setSpacing(10)
            self.upperLayout.addWidget(self.btn_return, 3)
            self.upperLayout.addWidget(self.btn_left, 1)
            self.upperLayout.addWidget(self.lab_name, 7)
            self.upperLayout.addWidget(self.btn_right, 1)
        #圣物详情页左侧    
        def init_left_table(self):
            self.tableWidget = QtWidgets.QTableWidget(self.page)
            self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            self.tableWidget.setShowGrid(True)
            self.tableWidget.setProperty("level", "table_info")
            self.tableWidget.setColumnCount(2)
            head_list = ["编号", "稀有度", "类型", "解锁方式", "独特圣物", "商店价格", "制作价格", "恶魔房代价", "", "合成材料", "", "主要经验来源"]
            row_num = len(head_list) + 1 #图片行+标题行数
            self.tableWidget.setRowCount(row_num)
            #表格背景半透明，隐藏上表头，不可选
            Ui_MainWindow.set_tablewidget_style_sheet(self.tableWidget, bg_transparent=self.opacity, flags="11001")
            for k in range(row_num - 1):
                item = QtWidgets.QTableWidgetItem(head_list[k])
                item.setFont(QFont('微软雅黑', 9, QFont.Black))
                self.tableWidget.setItem(k + 1, 0, item)
                if k != 0 and head_list[k] == "": #标题为空，和上一行合并
                    self.tableWidget.setSpan(k, 0, 2, 1)
            #合并单元格
            self.tableWidget.setSpan(0, 0, 1, 2) #第一行图片
            #设置水平方向宽度
            #设置自适应，0为等宽，默认=defaultSectionSize，但用户可调整
            #1为随窗口改变网格的大小，不可手工调整
            #2为每栏宽度固定，=defaultSectionSize
            #3为每栏宽度根据内容显示，不可手工调制
            self.tableWidget.horizontalHeader().setSectionResizeMode(1)
            self.tableWidget.verticalHeader().setSectionResizeMode(3)
            self.tableWidget.setContentsMargins(0, 0, 20, 20)
        
        #圣物详情页右侧    
        def init_right_info(self):
            self.infoLayout = QtWidgets.QVBoxLayout()
            self.infoLayout.setSpacing(7)
            self.infoLayout.setObjectName("infoLayout")
            #效果模块
            self.lab_effect_header = QtWidgets.QLabel("效果：", self.page)
            self.lab_effect_header.setProperty("level", "label_info_header")
            self.text_effect = QtWidgets.QTextBrowser(self.page)
            self.text_effect.setOpenExternalLinks(True)
            self.text_effect.setProperty("level", "text_info")
            effect_layout = QtWidgets.QVBoxLayout(self.page)
            effect_layout.addWidget(self.lab_effect_header)
            effect_layout.addWidget(self.text_effect)
            self.effect_frame = QtWidgets.QFrame(self.page)
            self.effect_frame.setLayout(effect_layout)
            self.infoLayout.addWidget(self.effect_frame, 5)
            #等级能力模块,需要一个选项卡
            self.tab_effect = QtWidgets.QTabWidget(self.page)
            self.tab_label = [] #存三个选项卡标签,显示技能名称
            self.tab_text = [] #存三个选项卡文本框，显示技能效果
            for i in range(3): #要有3页选项卡
                tab = QtWidgets.QWidget()
                vlayout = QtWidgets.QVBoxLayout(self.page)
                self.tab_label.append(QtWidgets.QLabel(self.page))
                self.tab_label[i].setProperty("level", "label_info_header_small")
                self.tab_text.append(QtWidgets.QTextBrowser(self.page))
                self.tab_text[i].setProperty("level", "text_info")
                self.tab_text[i].setOpenExternalLinks(True)
                vlayout.addWidget(self.tab_label[i])
                vlayout.addWidget(self.tab_text[i])
                tab.setLayout(vlayout)
                self.tab_effect.addTab(tab, f"技能{i+1}")
            self.infoLayout.addWidget(self.tab_effect, 5)
            #简评模块
            self.comment_frame = QtWidgets.QFrame(self.page)
            self.lab_comment_header = QtWidgets.QLabel("简评：", self.page)
            self.lab_comment_header.setProperty("level", "label_info_header")
            self.text_comment = QtWidgets.QTextBrowser(self.page)
            self.text_comment.setOpenExternalLinks(True)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(2)
            sizePolicy.setVerticalStretch(4)
            sizePolicy.setHeightForWidth(self.text_comment.sizePolicy().hasHeightForWidth())
            self.text_comment.setSizePolicy(sizePolicy)
            self.text_comment.setProperty("level", "text_info")
            comment_layout = QtWidgets.QVBoxLayout(self.page)
            comment_layout.addWidget(self.lab_comment_header)
            comment_layout.addWidget(self.text_comment)
            self.comment_frame.setLayout(comment_layout)
            self.infoLayout.addWidget(self.comment_frame, 5)
            
            #评分模块
            self.lab_score_header = QtWidgets.QLabel("评分：", self.page)
            self.lab_score_header.setProperty("level", "label_info_header")    
            self.lab_score_content = QtWidgets.QLabel(self.page)
            self.lab_score_content.setAlignment(QtCore.Qt.AlignCenter)
            self.lab_score_content.setProperty("level", "label_score")
            self.score_bar = QtWidgets.QHBoxLayout()
            self.score_bar.setObjectName("score_bar")
            self.score_bar.addWidget(self.lab_score_header, 1)
            self.score_bar.addWidget(self.lab_score_content, 9)
            self.score_frame = QtWidgets.QFrame()
            self.score_frame.setLayout(self.score_bar)
            self.infoLayout.addWidget(self.score_frame, 0)
            #危险度+不适度模块
            self.lab_danger_header = QtWidgets.QLabel("危险度：", self.page)
            self.lab_danger_header.setProperty("level", "label_info_header_small")
            self.lab_danger_content = QtWidgets.QLabel(self.page)
            self.lab_danger_content.setAlignment(QtCore.Qt.AlignCenter)
            self.lab_danger_content.setProperty("level", "label_score_small")
            self.danger_bar = QtWidgets.QHBoxLayout()
            self.danger_bar.setObjectName("danger_bar")
            self.danger_bar.addWidget(self.lab_danger_header, 1)
            self.danger_bar.addWidget(self.lab_danger_content, 9)
            self.lab_discomfort_header = QtWidgets.QLabel("不适度：", self.page)
            self.lab_discomfort_header.setProperty("level", "label_info_header_small")
            self.lab_discomfort_content = QtWidgets.QLabel(self.page)
            self.lab_discomfort_content.setAlignment(QtCore.Qt.AlignCenter)
            self.lab_discomfort_content.setProperty("level", "label_score_small")
            self.discomfort_bar = QtWidgets.QHBoxLayout()
            self.discomfort_bar.setObjectName("discomfort_bar")
            self.discomfort_bar.addWidget(self.lab_discomfort_header, 1)
            self.discomfort_bar.addWidget(self.lab_discomfort_content, 9)
            self.dang_and_disc_bar = QtWidgets.QVBoxLayout()
            self.dang_and_disc_bar.addLayout(self.danger_bar)
            self.dang_and_disc_bar.addLayout(self.discomfort_bar)
            self.dang_and_disc_frame = QtWidgets.QFrame()
            self.dang_and_disc_frame.setLayout(self.dang_and_disc_bar)
            self.dang_and_disc_frame.setFrameShape(0) #无边框
            self.infoLayout.addWidget(self.dang_and_disc_frame, 0)

                
    def setupUi(self, MainWindow):                    
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 750)
        MainWindow.setFixedSize(MainWindow.width(),MainWindow.height())
        #加载评分字体
        QtGui.QFontDatabase.addApplicationFont("./resources/Font/HYshangweishoushuW.ttf")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        #右上角按钮的公共参数
        self.top_margin = 8
        self.btn_w = 25
        self.btn_h = 25
        #关闭按钮
        close_icon = QIcon("./images/UI_whiteX.png")
        self.close_btn = QtWidgets.QPushButton(close_icon, "", MainWindow)
        self.close_btn.setProperty("level", "btn_of_main_function")
        self.close_btn.setIconSize(QtCore.QSize(self.btn_w, self.btn_h))
        self.close_btn.adjustSize()
        win_w = MainWindow.width()
        close_btn_x = win_w - self.btn_w - self.top_margin - 5
        self.close_btn.move(close_btn_x, self.top_margin)
        self.close_btn.pressed.connect(MainWindow.close)
        #最小化按钮
        # min_icon = QIcon("./images/UI_Mushroom.png")
        # self.min_btn = QtWidgets.QPushButton(min_icon, "", MainWindow)
        # self.min_btn.resize(self.btn_w, self.btn_h)
        # min_btn_x = close_btn_x - self.btn_w
        # self.min_btn.move(min_btn_x, self.top_margin)
        # self.min_btn.pressed.connect(MainWindow.showMinimized)

        
        #建立首页
        self.version = "1.1.0" #当前版本号
        self.page_index = QtWidgets.QWidget(self.stackedWidget)
        self.page_index.setObjectName("page_index")
        self.cover_layout = QtWidgets.QVBoxLayout(self.page_index)
        self.cover_name = QtWidgets.QLabel(self.page_index, objectName="label_cover_name")
        self.cover_name.setProperty("level", "label_list_title")
        self.cover_name.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self.cover_version = QtWidgets.QLabel(f"\n当前版本: {self.version}\n\n作者: 火焰大喷菇", self.page_index)
        self.cover_version.setProperty("level", "label_list_title")
        self.cover_version.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.read_me = QtWidgets.QTextBrowser(self.page_index)
        self.read_me.setHtml("""<b>使用说明:</b><br>
制作本软件的初衷是<b>便于玩家查询UM专栏信息</b>。因为我在B站的攻略以专栏为主，且因版本更新又有几次补充，圣物、药水图鉴相对分散，查询困难.<br>
现在使用本软件,可点击<font color="red"><b>左侧按钮</b></font>快速导航到对应模块，再<font color="green"><b>点击图片</b></font>，查看</b>详细效果、简评、评分</b>等信息.<br>
退出请点击<font color="blue"><b>右上角的×</b></font><br>
软件目前处于早期版本，如<u>遇到bug，或是有功能上的建议，欢迎加QQ交流群:<b>598427123</b></u><br>
更全的攻略资讯请点击查看<a href="https://www.bilibili.com/read/cv14661146">这篇专栏</a><br>
1.1.0增加了排序功能，便于在巫术<font color="purple"><b>混乱献祭</b></font>影响下根据代价查询道具。在圣物/药水查询界面，<b>按价格排序</b>可查看各圣物卖给黑兔的价格，乘一定倍率可得商店的出售价格；<b>按稀有度排序</b>可查看传奇圣物/药水在恶魔房出售的代价<br>
上次更新时间: <i><b>2022.9.4</b></i>""")
        self.read_me.setProperty("level", "text_info")
        self.read_me.setOpenExternalLinks(True)
        self.cover_layout.addWidget(self.cover_name,3)
        self.cover_layout.addWidget(self.cover_version,3)
        self.cover_layout.addWidget(self.read_me,4)
        self.cover_layout.setContentsMargins(30, 0, 30, 60)
        self.stackedWidget.addWidget(self.page_index)
        
        #建立圣物/药水等页面
        self.page_li = [] #储存页面
        #页面标题（新增表格需要修改)
        page_title = ["圣物Relic", "药水Potion", "祝福Blessing", "诅咒Curse", "同伴Familiar"]
        for i, title in enumerate(page_title):   
            self.page_li.append(Ui_MainWindow.ItemListPage(self.stackedWidget, title))
            self.stackedWidget.addWidget(self.page_li[i].page)

        #建立圣物/药水详情页
        self.page_info_li = [] #储存详情页
        for i in range(len(page_title)):
            self.page_info_li.append(Ui_MainWindow.ItemDetailPage())       
            self.stackedWidget.addWidget(self.page_info_li[i].page)
        
        #建立左侧菜单按钮
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setObjectName("layoutWidget")
        #按钮名字列表，依此创建对应按钮
        self.menu_btn_name_list = ["首页", "圣物", "药水", "祝福", "诅咒", "同伴"] 
        self.menu_btn_list = []
        for i in range(len(self.menu_btn_name_list)):
            btn = QtWidgets.QPushButton(QIcon(f"./images/btn_{i}.png"), self.menu_btn_name_list[i], self.layoutWidget)
            btn.setProperty("level", "btn_of_main_function")
            btn.setIconSize(QtCore.QSize(40, 40))
            btn.setMaximumSize(140, 50)
            self.menu_btn_list.append(btn)
        #将菜单按钮安装到最左侧的栅格布局
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        for i in range(len(self.menu_btn_list)):
            self.gridLayout.addWidget(self.menu_btn_list[i], i, 0, 1, 1)
            self.menu_btn_list[i].adjustSize()
        #设置控件在最上层
        self.layoutWidget.raise_()
        self.stackedWidget.raise_()
        self.central_hlayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.central_hlayout.addWidget(self.layoutWidget,2)
        self.central_hlayout.addWidget(self.stackedWidget,5)
           
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)#隐藏边框
        MainWindow.setWindowIcon(QtGui.QIcon("./images/icon.png"))
        self.retranslateUi(MainWindow) #翻译器
        self.stackedWidget.setCurrentIndex(0)
        for i in range(len(page_title)):
            self.page_info_li[i].btn_return.clicked.connect(self.menu_btn_list[i+1].click) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        #通过查询已安装的翻译文件返回sourceText的翻译文本
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"UnderMine专栏图鉴手册V{self.version}   作者:火焰大喷菇"))
        self.cover_name.setText(_translate("MainWindow", "欢迎使用UnderMine专栏图鉴手册"))
        for i in range(2):
            self.page_info_li[i].btn_return.setText(_translate("MainWindow", "返回"))
            self.page_info_li[i].lab_name.setText(_translate("MainWindow", "Item_name"))
        #设置左侧菜单按钮的文本
        for i, name in enumerate(self.menu_btn_name_list):
            self.menu_btn_list[i].setText(_translate("MainWindow", name))
    
    #设置按钮图片样式
    @staticmethod    
    def set_style_sheet(pushbutton, pic_path=None):
        style = """
        QPushButton{
        background: #426F42 no-repeat center;
        border: 5px solid #5C3317;
        border-radius: 8px;
        font-size: 20px;
        color: white;
        font-family: "微软雅黑", "宋体", sans-serif;
        }
        QPushButton:hover{
        border: 5px solid #A67D3D;
        color: #FFFF00;
        }
        QPushButton:pressed{
        border: 5px solid #CFB53B;
        }
        """
        pushbutton.setStyleSheet(style)
        if pic_path:
            pushbutton.setIcon(QtGui.QIcon(pic_path))
            pushbutton.setIconSize(QtCore.QSize(40, 40))
            
    #设置标签样式
    @staticmethod    
    def set_style_sheet2(label, pic_path=None):
        style = """
        QLabel{
        font: bold;
        font-size: 20px;
        font-family: "方正粗雅宋_GBK", "微软雅黑", "宋体", sans-serif;
        }
        """
        label.setStyleSheet(style)
        # 标签填充为图片
        if pic_path:
            label.setPixmap(QPixmap(pic_path))
            label.setScaledContents(True)
   
    #设置表格样式
    #bg_transparent表示设置不透明度
    #flags是5位二进制位组成的字符串,默认全选
    #分别表示隐藏上侧表头、左侧表头、网格线、边框、单元格完全不可选且选中无反应
    @staticmethod    
    def set_tablewidget_style_sheet(tableWidget, bg_transparent=1, flags="11111"):
        #更改表格背景透明度
        if 0 <= bg_transparent < 1:
            pll = tableWidget.palette()
            pll.setBrush(QPalette.Base, QBrush(QColor(255, 255, 255, bg_transparent * 255)))
            tableWidget.setPalette(pll)

        #隐藏表头(上侧表头，左侧表头）
        if flags[0] == "1":
            tableWidget.verticalHeader().setVisible(False)
        if flags[1] == "1":
            tableWidget.horizontalHeader().setVisible(False)
        #隐藏网格线
        if flags[2] == "1":
            tableWidget.setShowGrid(False)
        #隐藏边框
        if flags[3] == "1":
            tableWidget.setFrameShape(0)
        #点击表格无背景色变化，取消选中虚框
        if flags[4] == "1":
            tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        #设置不可修改、不可选择
            tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            tableWidget.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
            
        