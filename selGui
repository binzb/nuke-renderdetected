#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import upstream
import nuke
import re 
import os 


if nuke.NUKE_VERSION_MAJOR < 11:
    from Pyside.QtGui import *
    from Pyside.QtCore import *
    from Pyside.QtUiTools import QUiloader
    from Pyside import QtCore, QtGui ,QtUiTools as QtWidgets
    
else:
    from Pyside2.QtGui import *
    from Pyside2.QtCore import *
    from Pyside2.QtWidgets import *
    
from functools import partial



class Panel(QMainWindow):
    
    def __init__(self,parent = QApplication.activeWindow()):
        super(Panel, self).__init__(parent)
        self.pt = QtWidget()
        self.setWindowTitle('ErrorToDeadline')
        self.setCentralWidget(self.pt)
        self.set_style_sheet()
        
        
        
    def addknobs(self,Rread,Rwrite = [],RPlugin = []):
        
        pt = self.pt
        pt.c = 0 
        if len(Rread)<3:
            pt.c = 0 
        else:
            pt.c = 2 
        action_layout = QHBoxLayout()
        pt.master_layout = QVBoxLayout()
        
        
        #text
        
        pt.tx = QLabel()
        pt.tx2 = QLabel()
        pt.tx.setText("<font style = 'font-family:Microsoft YaHei' size = '3'>" + "The follwing nodes maybe have some problem"+"\n"+"Click to Focus")
        pt.tx2.setText("My life is brilliant on 2017.07")
        pt.tx.adjustSize()
        
        
        pt.lGroup = QGroupBox("Des")
        pt.lGroup.setLayout(QVboxLayout())
        pt.lGroup.layout().setAlignment(Qt.AlignHcenter)
        pt.lGroup.layout().addWidget(pt.tx)

        pt.lGroup2 = QGroupBox("Thx")
        pt.lGroup2.setLayout(QVboxLayout())
        pt.lGroup2.layout().setAlignment(Qt.AlignHcenter)
        pt.lGroup2.layout().addWidget(pt.tx)        
        
        
        #read 
        
        
        pt.rGroup = QGroupBox("Read")
        if len(Rread)>3:
            pt.rGroup.setLayout(QGridLayout())
            pt.rGroup.layout().setColumnStretch(pt.c,2)
        else:
            pt.rGroup.setLayout(QHBoxLayout())
            
            
            
            
        #write
        
        pt.wGroup = QGridLayout("Write")
        pt.wGroup = setLayout(QGridLayout())
        pt.wGroup.layout().setAlignment(Qt.AlignHcenter)
        pt.wGroup.layout().setColumnStretch(pt.c,2)
        
        
        
        #plugin 
        
        pt.pGroup = QGroupBox("Plugin")
        pt.pGroup.setLayout(QGridLayout())
        pt.pGroup.layout().setAlignment(Qt.AlignHcenter)
        pt.pGroup.layout().setColumnStretch(pt.c,2)
        
        
        
        
        for i in Rread:
            if len(Rread) == 0:
                break
            s = i+"#"
            pt.i = QPushButton(s)
            pt.rGroup.layout().addWidget(pt.i)
            pt.i.clicked.connect(partial(self.Focus,s,pt.i))
            
        for k in Rwrite:
            if len(Rwrite) == 0:
                break
            s2 = k+"#"
            pt.k = QPushButton(s2)
            pt.wGroup.layout().addWidget(pt.k)
            pt.k.clicked.connect(partial(self.Focus,s2,pt.k))   
            
        for j in RPlugin:
            if len(RPlugin) == 0:
                break
            s3 = j+"#"
            pt.j = QPushButton(s3)
            pt.pGroup.layout().addWidget(pt.j)
            pt.j.clicked.connect(partial(self.Focus,s3,pt.j))
            
            
        refresh = QPushButton("Reflesh(Need to Reselect Write Nodes)")
        refresh.setStyleSheet('QPushButton {color: yellow}')
        refresh.clicked.connect(self.fresh)
        
        
        pt.master_layout.addWidget(pt.lGroup)
        if len(Rread) != 0:
            pt.master_layout.addWidget(pt.rGroup)
            
        if len(Rwrite) != 0:
            pt.master_layout.addWidget(pt.wGroup)
            
        if len(RPlugin) != 0:
            pt.master_layout.addWidget(pt.pGroup)
            
        pt.master_layout.addWidget(refresh)
        pt.master_layout.addWidget(pt.lGroup2)
        
        pt.setLayout(pt.master_layout)
        
        self.resize(pt.layout().sizeHint())
        
        
        
        
    def Focus(self,node,p):
        if nuke.selectedNodes() is None:
            pass
        else:
            sn = nuke.selectedNodes()
        if len(sn):
            for b in sn:
                b['selected'].setValue(False)
                
        print node
        
        kn = list(node)
        kn.remove('#')
        knn = ''.join(kn)
        a = nuke.toNode(knn)
        a.knob('selected').setValue(True)
        nuke.zoomToFitSelected()
        p.setStyleSheet('QPushButton {color: #ffc78e;}')
        
        
        
        
    def set_style_sheet(self):
        
        text = open('..\..\style.txt').read()
        self.setStyleSheet(text)
        
    def fresh(self):
        
        reload(upstream)
        (read,write,plugin) = upstream.Detecting(0)
        
        if read = [] and write == [] and plugin == []:
            nuke.message("<font style = 'font-family:Microsoft YaHei' size = 3>" + "All problem was Solved")
            self.close()
            return
        elif read = [1] and write == [1] and plugin ==[1]:
            return
        
        else:
            
            self.clearLayout(read,self.pt.rGroup)
            self.clearLayout(write,self.pt.wGroup)
            self.clearLayout(plugin,self.pt.pGroup)
            
            
    def clearLayout(self,read,lay):
        layout = lay.layout()
        reads = []
        for s in read:
            s = s+"#"
            reads.append(s)
        for i in reversed(range(layout.count())):
            widgetToRemove = layout.itemAt(i).widget()
            
            if reads == []:
                widgetToRemove.setStyleSheet('QPushButton {color: green;}')
            else:
                widgetToRemove.setStyleSheet('QPushButton {color: orange;}')
                
                
            if type(widgetToRemove).__name__ == "QPushButton" and (str(widgetToRemove.text())) in reads:
                
                widgetToRemove.setStyleSheet('QPushButton {color: orange;}')
                continue
            
            else:
                
                widgetToRemove.setStyleSheet('QPushButton {color: green;}')
                
                

        

    
    
    
        
