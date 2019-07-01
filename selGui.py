#!/usr/bin/python
# -*- coding: utf-8 -*-
# By zhuangbin 
import sys
import upstream
import nuke
import re 
import os 


if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtUiTools import QUiLoader
    from PySide import QtCore, QtGui ,QtUiTools as QtWidgets
    
else:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    
from functools import partial

tab = '&nbsp;&nbsp;&nbsp;&nbsp;'

class Panel(QMainWindow):
    
    def __init__(self,parent = QApplication.activeWindow()):
        super(Panel, self).__init__(parent)
        self.pt = QWidget()
        self.setWindowTitle('ErrorToDeadline')
        self.setCentralWidget(self.pt)
        self.set_style_sheet()
        self.btnswitch = False
        
        
    def addknobs(self,Rread,Rwrite = [],RPlugin = []):
        
        pt = self.pt
        pt.c = 0 
        if len(Rread)<3:
            pt.c = 0 
        else:
            pt.c = 2 
            
        pt.action_Layout = QGridLayout()
        pt.right_layout = QVBoxLayout()
        pt.master_layout = QVBoxLayout()
        pt.master_layout_withBtn = QHBoxLayout()
        
        
        
        #text
        
        pt.tx = QLabel()
        pt.tx2 = QLabel()
        pt.tx.setText("<center><font style = 'font-family:Microsoft YaHei' size = '3'>" + "The follwing nodes maybe <br>have some problem to Deadline."+" <br/>"+"<font color = #ffc78e>Click to Focus")
        pt.tx2.setText("My life is brilliant on 2017.07 by Binz")
        pt.tx.adjustSize()
        
        pt.hp = QLabel()
        strHTML = "\
\
<style>k{white-space:pre}</style>\
<k>\
    This Script is for rendering to deadline<br>And it maybe not suitable for local render<br><br>\
Detecting Rule:<br><br>\
#Read:<br>\
    1.File doesn exist <br>\
    2.File on local disk <br><br>\
#write:<br>\
    1.Write node has not Extension<br>\
    2.The Extension type doesn match <br>\
       the file type <br>\
    3.The path contain space characters<br><br>\
#plugin:<br>\
    1.Plugin node not install on server<br>\
</k> "
            
                   
        pt.hp.setText(strHTML)
        
        pt.addPlugintext = QLabel()
        pt.addPlugintext.setText('Select the plugin node and click <br>the button to add into error Pluginslist ')
        pt.addPlugintext.setAlignment(Qt.AlignCenter)
        pt.addPlugintext.adjustSize()
        #pt.tx.setWordWrap(True)
        
        pt.lGroup = QGroupBox("Des")
        pt.lGroup.setLayout(QVBoxLayout())
        pt.lGroup.layout().setAlignment(Qt.AlignCenter)
        pt.lGroup.layout().addWidget(pt.tx)

        pt.lGroup2 = QGroupBox("Thx")
        pt.lGroup2.setLayout(QVBoxLayout())
        pt.lGroup2.layout().setAlignment(Qt.AlignCenter)
        pt.lGroup2.layout().addWidget(pt.tx2)        
        
        pt.lGroup3 = QGroupBox("Help")
        pt.lGroup3.setLayout(QVBoxLayout())
        pt.lGroup3.layout().setAlignment(Qt.AlignCenter)
        pt.lGroup3.layout().addWidget(pt.hp) 
        
        #read 
        
        
        pt.rGroup = QGroupBox("Read")
        if len(Rread)>=3:
            pt.rGroup.setLayout(QGridLayout())
            pt.rGroup.layout().setColumnStretch(pt.c,2)
            pt.rGroup.layout().setRowStretch(0,1)
            pt.rGroup.layout().setRowStretch(1,1)
            pt.rGroup.layout().setRowStretch(2,1)
            pt.rGroup.layout().setRowStretch(3,1)            
        else:
            pt.rGroup.setLayout(QHBoxLayout())
            
            
            
            
            
        #write
        
        pt.wGroup = QGroupBox("Write")
        pt.wGroup.setLayout(QGridLayout())
        pt.wGroup.layout().setAlignment(Qt.AlignCenter)
        pt.wGroup.layout().setColumnStretch(pt.c,2)
        pt.rGroup.layout().setRowStretch(0,1)
        pt.rGroup.layout().setRowStretch(1,1)
        pt.rGroup.layout().setRowStretch(2,1)
        pt.rGroup.layout().setRowStretch(3,1)         

        
        
        #plugin 
        
        pt.pGroup = QGroupBox("Plugin")
        pt.pGroup.setLayout(QGridLayout())
        pt.pGroup.layout().setAlignment(Qt.AlignCenter)
        pt.pGroup.layout().setColumnStretch(pt.c,1)
        pt.pGroup.layout().setRowStretch(0,1)
        pt.pGroup.layout().setRowStretch(1,1)
        pt.pGroup.layout().setRowStretch(2,1)
        pt.pGroup.layout().setRowStretch(3,1)

        #plugin addRule
        
        pt.pRGroup = QGroupBox("AddErrorPlugin")
        pt.pRGroup.setLayout(QVBoxLayout())
        pt.pRGroup.layout().setAlignment(Qt.AlignCenter)
        #pt.pRGroup.setFixedSize(300,100)
        #pt.pRGroup.layout().setColumnStretch(pt.c,2)
        
        
        
        
        for i in Rread:
            if len(Rread) == 0:
                break
            s = i+"#"
            pt.i = QPushButton(s)
            pt.rGroup.layout().addWidget(pt.i)
            pt.i.clicked.connect(partial(self.Focus,s,pt.i))
            if len(Rread) == 1:
                pt.i.setFixedSize(100,23)
            
        for k in Rwrite:
            if len(Rwrite) == 0:
                break
            s2 = k+"#"
            
            pt.k = QPushButton(s2)
            pt.wGroup.layout().addWidget(pt.k)
            pt.wGroup.layout().setRowStretch(0,1)
            pt.wGroup.layout().setRowStretch(1,1)
            pt.wGroup.layout().setRowStretch(2,1)
            pt.wGroup.layout().setRowStretch(3,1)             
            pt.k.clicked.connect(partial(self.Focus,s2,pt.k))   
            if len(Rwrite) == 1:
                pt.k.setFixedSize(100,23)            
            
        for j in RPlugin:
            if len(RPlugin) == 0:
                break
            
            i = list(j)
            del i[7:20]
            temp = "".join(i)
            s3 = temp+"#"
            
            pt.j = QPushButton(s3)
            pt.pGroup.layout().addWidget(pt.j)
            pt.j.clicked.connect(partial(self.Focus,s3,pt.j))
            if len(RPlugin) == 1:
                pt.j.setFixedSize(100,23)  
            
            
        refresh = QPushButton("Refresh")#(Need to Reselect Write Nodes)
        refresh.setToolTip("Need to Reselect Write Nodes")
        refresh.setFixedSize(100,25)
        refresh.setStyleSheet('QPushButton {color: yellow}')
        refresh.clicked.connect(self.fresh)
        
        addPlugin = QPushButton("addErrorPlugin")
        #addPlugin.setFixedSize(100,25)
        addPlugin.clicked.connect(self.add_Plugin)
        
        pt.pRGroup.layout().addWidget(pt.addPlugintext)        
        pt.pRGroup.layout().addWidget(addPlugin)

        
        pt.master_layout.addWidget(pt.lGroup)
        if len(Rread) != 0:
            pt.master_layout.addWidget(pt.rGroup)
            
        if len(Rwrite) != 0:
            pt.master_layout.addWidget(pt.wGroup)
            
        if len(RPlugin) != 0:
            pt.master_layout.addWidget(pt.pGroup)
            
        pt.master_layout.addWidget(refresh,0,Qt.AlignCenter)
        pt.master_layout.addWidget(pt.lGroup2)
        
        pt.right_layout.addWidget(pt.lGroup3)
        pt.right_layout.addWidget(pt.pRGroup)
        
        rq = QWidget()
        rq.setLayout(pt.right_layout)
        


        
        pt.master_layout_withBtn.addLayout(pt.master_layout)
        Btn = QPushButton()
        pt.master_layout_withBtn.addWidget(Btn)
        pt.master_layout_withBtn.setContentsMargins(0,0,0,0)

        
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        icon = QIcon()
        icon.addFile("arr.png")

        Btn.setIcon(icon)
        Btn.setIconSize(QSize(100,100))
        Btn.setFixedSize(13,42)
        #Btn.setStyleSheet('QPushButton {background: green;border: 0px;}')
        Btn.setFlat(True)
        Btn.setCheckable(True)
        Btn.setAutoDefault(False)
        Btn.toggled.connect(rq.setVisible)
        Btn.toggled.connect(partial(self.ccc,Btn))
        pt.action_Layout.setSizeConstraint(QLayout.SetFixedSize)
        pt.action_Layout.addLayout(pt.master_layout_withBtn,0,0)
        pt.action_Layout.addWidget(rq,0,1)

        pt.setLayout(pt.action_Layout)
        rq.hide()
        self.resize(pt.layout().sizeHint())
        
        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
        
        
    def ccc(self,btn,btn2):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        icon2 = QIcon()
        icon2.addFile("arr.png")
        icon = QIcon()
        icon.addFile("arr2.png")
        if self.btnswitch:
            btn.setIcon(icon2)
            self.btnswitch = False
        else:
            btn.setIcon(icon)
            self.btnswitch = True
            
    def xxx(self,s,w):
        
        if self.btnswitch:
            
            s.removeWidget(w)
            self.btnswitch = False
        else:
            s.addWidget(w)
            w.setVisible(True)
            self.btnswitch = True

        self.layout().setSizeConstraint(QLayout.SetFixedSize)
        
        
        
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
        if p.styleSheet() != "QPushButton {color: green;}":
            p.setStyleSheet('QPushButton {color: #ffc78e;}')
        print p.styleSheet()
        
        
    def add_Plugin(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))#强制运行路径到当前路径
        pn = nuke.selectedNodes()
        ps = []
        for i in pn:
            if i.Class() not in ps:
                ps.append(i.Class())

        pns = ','.join(ps)
        su = nuke.ask("Are you sure add "+pns+" to ErrorPlugin")
        if su:
            with open('Bult_in_nodes.txt', 'r') as f2:
                pos2 = []
                for line in f2:
                    if re.search('\n',line):
                        a = list(line)
                        a.remove('\n')
                        b = ''.join(a)
                        if b != '':
                            pos2.append(b)
                    elif line != '':
                        pos2.append(line)    
                        
            with open('plugin.txt', 'a+') as f:
                pos = []
                for line in f:
                    if re.search('\n',line):
                        a = list(line)
                        a.remove('\n')
                        b = ''.join(a)
                        if b != '':
                            pos.append(b)
                    elif line != '':
                        pos.append(line)      
                print pos
                for i in pn:
                    if i.Class() not in pos and i.Class() not in pos2:
                        f.write('\n'+i.Class())
            
            
        
    def set_style_sheet(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        text = open("style.txt").read()
        self.setStyleSheet(text)
        
    def fresh(self):
        
        reload(upstream)
        (read,write,plugin) = upstream.Detecting(0)
        
        if read == [] and write == [] and plugin == []:
            nuke.message("<font style = 'font-family:Microsoft YaHei' size = 3>" + "All problem was Solved")
            self.close()
            return
        elif read == [1] and write == [1] and plugin ==[1]:
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
                
                

        

    
    
    
        
