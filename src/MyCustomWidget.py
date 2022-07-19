'''
Created on 2022年7月18日

@author: 61963
'''
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QWidget, QLabel

class OneButtonOneLabel(QWidget):
    '''
    :desciption: 一个上按钮下标签的垂直布局，用于展示圣物
    '''
    def __init__(self, parent=None, index=0, pic=None, text=0 ):
        '''
        :function: 创建含一个按钮+标签的垂直布局
        :param pic:按钮图片路径
        :param text:标签显示内容
        :param parent:我母鸡啊
        '''
        super(OneButtonOneLabel, self).__init__(parent)
        self.resize(105, 105)
        #self.layout = QtWidgets.QVBoxLayout()
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.addStretch(1)
        self.vbox.setSpacing(1)
        self.setLayout(self.vbox)
        if os.path.isfile(pic):
            
            self.btn = QtWidgets.QPushButton(QtGui.QIcon(pic),"")
            
            self.btn.setStyleSheet('QPushButton{margin:3px};')
            
            self.btn.setIconSize(QtCore.QSize(95, 95))
            
            self.vbox.addWidget(self.btn)

        self.lab1 = QLabel(self)
        self.lab1.setText(text)
        self.lab1.setAlignment(QtCore.Qt.AlignCenter)
        self.lab1.setFixedSize(95, 20)
        self.vbox.addWidget(self.lab1)
        self.btn.index = index #识别按钮发送方
        
        
        