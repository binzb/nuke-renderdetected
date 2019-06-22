#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        
        
        
    def addknobs(self,Rread,Rwrite = [],RPlugin = []):
        
        pt = self.pt
        pt.c = 0 
        if len(Rread)<3:
            pt.c = 0 
        else:
            pt.c = 2 
        pt.action_layout = QHBoxLayout()
        pt.left_layout = QVBoxLayout()
        pt.master_layout = QVBoxLayout()
        
        
        
        #text
        
        pt.tx = QLabel()
        pt.tx2 = QLabel()
        pt.tx.setText("<center><font style = 'font-family:Microsoft YaHei' size = '3'>" + "The follwing nodes maybe <br>have some problem to Deadline."+" <br/>"+"<font color = #ffc78e>Click to Focus")
        pt.tx2.setText("My life is brilliant on 2017.07")
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
        if len(Rread)>3:
            pt.rGroup.setLayout(QGridLayout())
            pt.rGroup.layout().setColumnStretch(pt.c,2)
        else:
            pt.rGroup.setLayout(QHBoxLayout())
            
            
            
            
        #write
        
        pt.wGroup = QGroupBox("Write")
        pt.wGroup.setLayout(QGridLayout())
        pt.wGroup.layout().setAlignment(Qt.AlignCenter)
        pt.wGroup.layout().setColumnStretch(pt.c,2)
        
        
        
        #plugin 
        
        pt.pGroup = QGroupBox("Plugin")
        pt.pGroup.setLayout(QGridLayout())
        pt.pGroup.layout().setAlignment(Qt.AlignCenter)
        pt.pGroup.layout().setColumnStretch(pt.c,2)

        #plugin addRule
        
        pt.pRGroup = QGroupBox("AddErrorPlugin")
        pt.pRGroup.setLayout(QVBoxLayout())
        pt.pRGroup.layout().setAlignment(Qt.AlignCenter)
        pt.pRGroup.setFixedSize(300,100)
        #pt.pRGroup.layout().setColumnStretch(pt.c,2)
        
        
        
        
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
            
        pt.master_layout.addWidget(refresh)
        pt.master_layout.addWidget(pt.lGroup2)
        
        pt.left_layout.addWidget(pt.lGroup3)
        pt.left_layout.addWidget(pt.pRGroup)
        
        pt.action_layout.addLayout(pt.master_layout)
        pt.action_layout.addLayout(pt.left_layout)
        
        pt.setLayout(pt.action_layout)
        
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
        if p.styleSheet() != "QPushButton {color: green;}":
            p.setStyleSheet('QPushButton {color: #ffc78e;}')
        print p.styleSheet()
        
        
    def add_Plugin(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        pn = nuke.selectedNodes()
        ps = []
        for i in pn:
            if i.Class() not in ps:
                ps.append(i.Class())

        pns = ','.join(ps)
        su = nuke.ask("Are you sure add "+pns+" to ErrorPlugin")
        if su:
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
                    if i.Class() not in pos:
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
                
                

        

    
    
    
        
