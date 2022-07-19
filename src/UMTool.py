import sys     
from PyQt5.QtWidgets import QApplication, QMainWindow , QAbstractItemView, QTableWidget,\
    QVBoxLayout, QPushButton
#from UMHelper import Ui_MainWindow
from UMHelper2 import Ui_MainWindow
import os.path
#import pymysql
from PyQt5.Qt import QTableWidgetItem, QPixmap, QLabel
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QIcon, QPainter
from PyQt5.QtCore import QSize, Qt
import xlrd
from MyCustomWidget import OneButtonOneLabel

class MainWindow(QMainWindow):
    def __init__(self, parent=None):    
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_2.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_3.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_4.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_5.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.pushButton_6.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(5))
       # self.ui.tableWidget.itemClicked.connect(self.show_relic_info)
    #绘制背景图片    
    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setOpacity(0.6)#设置透明度
        pixmap = QPixmap(r"../images/UI_BookProps1.png")
        painter.drawPixmap(self.rect(), pixmap)

    #加载圣物查询界面的图像    
    def updateRelic(self):
        relic_table = xlrd.open_workbook("Relic_new.xls").sheets()[0]
        relic_n = relic_table.nrows - 1
        self.btn_list = []
        row_n = relic_n // 5 + 1 #圣物呈现行数，每行5个,有一行是表头
        print(row_n)
        
        self.ui.tableWidget.setIconSize(QSize(100,100))
        self.ui.tableWidget.setRowCount(row_n)
        self.ui.tableWidget.setColumnCount(5)
        #隐藏表头
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.horizontalHeader().setVisible(False)
        #设置不可修改、不可选择
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        for i in range(row_n):
            self.ui.tableWidget.setRowHeight(i,125)
        for i in range(5):
            self.ui.tableWidget.setColumnWidth(i,105)
        
        #以英文名加载圣物图片
        eng_n = relic_table.row_values(0).index("english_name")#获取表标题
        chi_n = relic_table.row_values(0).index("chinese_name")
        eng_n_list = relic_table.col_values(eng_n, start_rowx=1)#获取英文名列的所有英文名
        chi_n_list = relic_table.col_values(chi_n, start_rowx=1)
        for i, it in enumerate(eng_n_list):
            pic_path = r"..\images\Relics\{}.png".format(it)
            if os.path.isfile(pic_path):
                newPic = QTableWidgetItem(QIcon(pic_path),'')
                newPic.setTextAlignment(Qt.AlignCenter)
                self.btn_list.append(OneButtonOneLabel(None, i + 1, pic_path, chi_n_list[i]))
                #self.ui.gridLayout2.addWidget(self.btn_list[count], count // 5, count % 5, 1, 1)    
                self.ui.tableWidget.setCellWidget(i // 5, i % 5, self.btn_list[i])
                self.btn_list[i].btn.clicked.connect(self.show_relic_info)     
            
    #输入字母，返回稀有度文本
    @staticmethod
    def get_rality_text(rality):
        if rality == "C":
            ralitytext = "普通"
        elif rality == "R":
            ralitytext = "稀有"
        elif rality == "L":
            ralitytext = "传说"
        else:
            ralitytext = "未知"
        return ralitytext
    
    #输入标题+html字符串，返回加工后的字符串文本
    @staticmethod
    def get_styled_text(text, name):
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
            }<!7分>
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
                color: #d6d5d5;
            }<!0分>
            .font-size-16 {
                font-size: 16px;
            }
            .font-size-20 {
                font-size: 20px;
            }
        </style>
        </head>
        <body>

        <h2>""" + name + """：</h2>
        """ + text + """
        </p>
        </body>
        </html>
        """
        return new_text
    
    def show_relic_info(self):#获取圣物坐标，更新页面信息
        # for i in self.ui.tableWidget.selectionModel().selection().indexes():
            # relic_no = (i.row()) * 5 + i.column() + 1
            # print(relic_no)
        sendbtn = self.sender()
        relic_no = sendbtn.index
        relic_table = xlrd.open_workbook("Relic_new.xls").sheets()[0]
        relic_info_list = relic_table.row_values(relic_no) #获取圣物详细信息
        self.ui.stackedWidget.setCurrentIndex(3)
        print(relic_info_list)
        name = relic_info_list[1]
        english_name = relic_info_list[2]
        rality = relic_info_list[3]
        unlock_method = relic_info_list[4]
        shop_cost = relic_info_list[5]
        unlock_cost = relic_info_list[6]
        effect = relic_info_list[7]
        #effect = self.preprocessText(effect)
        comment = relic_info_list[8]
        score = relic_info_list[9]
        pic_path = r"..\images\Relics\{}.png".format(english_name)
        pic = QTableWidgetItem(QIcon(pic_path),'')
        pic.setTextAlignment(Qt.AlignCenter)
        
        self.ui.tableWidget_2.setItem(0, 0, pic)
        self.ui.tableWidget_2.setSpan(0, 0, 1, 2)
        self.ui.tableWidget_2.setIconSize(QSize(100,100))
        self.ui.tableWidget_2.setRowHeight(0,105)
        #self.ui.tableWidget_2.setColumnWidth(1,105)
        self.ui.tableWidget_2.setItem(1, 1, QTableWidgetItem(str(relic_no)))

        
        self.ui.tableWidget_2.setItem(2, 1, QTableWidgetItem(self.get_rality_text(rality)))
        self.ui.tableWidget_2.setItem(3, 1, QTableWidgetItem(unlock_method))
        self.ui.tableWidget_2.setRowHeight(3,150)
        self.ui.lineEdit_2.setText(name)
         
        self.ui.textEdit.setHtml(self.get_styled_text(effect, "效果"))
        self.ui.textEdit_2.setHtml(self.get_styled_text(comment, "简评"))
        scoretext = "评分：" + score
        self.ui.lineEdit.setText(scoretext)
                
        
    # def connectdb(self, sqls):
        # conn = pymysql.connect(host='localhost',port=3306,user='root',password='wjl69612705',database='undermine',charset="utf8")
        # #创建一个可执行SQL语句的光标对象
        # cursor = conn.cursor()
        # #执行sql语句
        # cursor.execute(sqls)
        # #以二维元组形式获取多条查询数据
        # ret = cursor.fetchall()
        # #关闭光标与连接
        # cursor.close()
        # conn.close()
        # return ret
            
    # def updateRelic_sql(self):
        # sql1 = """
        # select pic_path from relic
        # """
        # relic_pic_list = self.connectdb(sql1)
        # count = 0 #表格从第0行，第0列开始
        # row_n = len(relic_pic_list) // 5
        # #表格有n行5列，设置图片大小，并让行列宽适应图片
        # self.ui.tableWidget.setIconSize(QSize(100,100))
        # self.ui.tableWidget.setRowCount(row_n)
        # self.ui.tableWidget.setColumnCount(5)
        # #隐藏表头
        # self.ui.tableWidget.verticalHeader().setVisible(False)
        # self.ui.tableWidget.horizontalHeader().setVisible(False)
        # #设置不可修改、不可选择
        # self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.ui.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        # for i in range(row_n):
            # self.ui.tableWidget.setRowHeight(i,105)
        # for i in range(5):
            # self.ui.tableWidget.setColumnWidth(i,105)
            #
        # for it in relic_pic_list:
            # #name = it[0]
            # pic_path = it[0] #元组每项为(名称，地址)
            # if os.path.isfile(pic_path):
                # newPic = QTableWidgetItem(QIcon(pic_path),'')
                # newPic.setTextAlignment(Qt.AlignCenter)
                # self.ui.tableWidget.setItem(count // 5, count % 5 ,newPic)
                # count += 1
                
    # def show_relic_info_sql(self):#获取圣物坐标，更新页面信息
        # for i in self.ui.tableWidget.selectionModel().selection().indexes():
            # relic_no = (i.row()) * 5 + (i.column()+1)
            # print(relic_no)
        # sql2 = "select * from relic where id=" + str(relic_no)
        # self.ui.stackedWidget.setCurrentIndex(3)
        # relic_info_list = self.connectdb(sql2)[0]
        # print(relic_info_list)
        # name = relic_info_list[1]
        # english = relic_info_list[2]
        # rality = relic_info_list[3]
        # unlock_method = relic_info_list[4]
        # shop_cost = relic_info_list[5]
        # unlock_cost = relic_info_list[6]
        # effect = relic_info_list[7]
        # effect = self.preprocessText(effect)
        # score = relic_info_list[8]
        # pic_path = relic_info_list[9]
        # pic = QTableWidgetItem(QIcon(pic_path),'')
        # pic.setTextAlignment(Qt.AlignCenter)
        # validarity = relic_info_list[10]
        #
        # self.ui.tableWidget_2.setItem(0, 0, pic)
        # self.ui.tableWidget_2.setSpan(0, 0, 1, 2)
        # self.ui.tableWidget_2.setIconSize(QSize(100,100))
        # self.ui.tableWidget_2.setRowHeight(0,105)
        # #self.ui.tableWidget_2.setColumnWidth(1,105)
        # self.ui.tableWidget_2.setItem(1, 1, QTableWidgetItem(str(relic_no)))
        # if rality == "C":
            # ralitytext = "普通"
        # elif rality == "R":
            # ralitytext = "稀有"
        # elif rality == "L":
            # ralitytext = "传说"
        # else:
            # ralitytext = "未知"
        # self.ui.tableWidget_2.setItem(2, 1, QTableWidgetItem(ralitytext))
        # self.ui.tableWidget_2.setItem(3, 1, QTableWidgetItem(unlock_method))
        # self.ui.tableWidget_2.setRowHeight(3,100)
        # self.ui.lineEdit_2.setText(name)
        # effecttext = """
        # <!DOCTYPE html>
        # <html>
        # <head>
        # <meta charset="utf-8">
        # </head>
        # <body>
        # <p>
        # """ + effect + """
        # </p>
        # </body>
        # </html>
        # """
        #
        # #"效果："+ effect
        # self.ui.textEdit.setHtml(effecttext)
        # scoretext = "评分：" + str(score) + "分"
        # self.ui.lineEdit.setText(scoretext)
  
        
if __name__=="__main__":  
    app = QApplication(sys.argv)  
    win = MainWindow()  
    win.show()  
    win.updateRelic()  
    sys.exit(app.exec_())  