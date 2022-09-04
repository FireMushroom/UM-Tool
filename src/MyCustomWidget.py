'''
Created on 2022年7月18日

@author: 61963
'''
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon

class OneButtonOneLabel(QWidget):
    '''
    :desciption: 一个上按钮下标签的垂直布局，用于展示物件
    '''
    btnClick_signal = pyqtSignal(int) #信号返回按钮序号
    def __init__(self, parent=None, index=0, pic="", color="", text="", size=105, border=True, btn_pic=[], btn_text=[]):
        '''
        :function: 创建含一个按钮+标签的垂直布局
        :param parent:容器
        :param index:按钮编号(从0开始)
        :param pic:按钮图片路径
        :param color:按钮边框颜色
        :param text:标签显示内容      
        :param size:调整按钮大小
        :param border:是否需要圆角边框
        '''
        super(OneButtonOneLabel, self).__init__(parent)
        size = parent.width() / 5
        self.resize(size, size)
        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addStretch(1)
        self.vbox.setSpacing(1)
        self.setLayout(self.vbox)
        if not os.path.isfile(pic): #不存在路径则填充空白图
            pic = "../images/UI_Blank.png"
                
        self.btn = QPushButton(QtGui.QIcon(pic),"",self)            
        self.btn.setIconSize(QtCore.QSize(size - 10, size - 10))
        if not border:
            style_btn = f'''QPushButton{{
            background: rgba(255,255,255,0.6);
            }}
            QPushButton:pressed{{
            background: rgba(255,255,255,0.75);
            }}'''
        else:
            style_btn = f'''QPushButton{{border: 5px solid {color};
            margin: 3px; 
            border-radius: 8px;
            background: rgba(255,255,255,0.5);
            }}
            QPushButton:hover{{
            background: rgba(255,255,255,0.75);
            }}
            QPushButton:pressed{{
            background: rgba(255,255,255,1);
            }}'''
        self.btn.setStyleSheet(style_btn)
        self.btn.setCursor(QtGui.QCursor(QtGui.QPixmap("./images/Ellipses_5.png").scaled(40, 30)))
        self.vbox.addWidget(self.btn)

        self.lab1 = QLabel(self)
        self.lab1.setText(text)
        self.lab1.setAlignment(QtCore.Qt.AlignCenter)
        self.lab1.setFixedSize(size, 20)
        #gbk编码成字节流，一个中文2B，超7个字则缩小字体
        if len(text.encode("gbk")) <= 14: 
            font_size = 16
        else:
            font_size = 13 
        style_lab = f'''QLabel{{
        font: bold;
        font-size: {font_size}px;
        font-family: "Arial", "微软雅黑", "宋体", sans-serif;
        }}'''
        self.lab1.setStyleSheet(style_lab)
        self.vbox.addWidget(self.lab1)
        self.btn.index = index #记录按钮编号
        #self.btn.color = color #识别按钮框色
        style_btn2 = f'''QPushButton{{
        border-radius: 4px;
        background: rgba(255,255,255,0.5);
        font: bold 14px;
        color: blue;
        font-family: Arial, "微软雅黑", "宋体", sans-serif;
        }}
        QPushButton:hover{{
        background: rgba(255,255,255,0.5);
        }}
        QPushButton:pressed{{
        background: rgba(255,255,255,0.5);
        }}'''
        btn_num = len(btn_text)
        if btn_num > 0:
            for i in range(btn_num):
                if btn_text[i] != "": #不是空值
                    new_btn = QPushButton(QIcon(btn_pic[i]),btn_text[i],self)
                    new_btn.setStyleSheet(style_btn2)
                    new_btn.setFixedSize(size, 20)
                    self.vbox.addWidget(new_btn)
        
    def mousePressEvent(self, evt):
        super().mousePressEvent(evt)
        self.btnClick_signal.emit(self.btn.index)
        
        