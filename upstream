#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import nuke
import re
import nukescripts
import psutil
import string


er1 = ''
er2 = ''
ProxyOne = 0
Readtwo = 0
Pluginthree = 0
rootError = 0
WriteFourth = 2
ErrorRead = []
ErrorPlugin = []
ErrorWrite = []
p = nuke.root()
frame = 0
fill = 4
MRM = "R:/filmServe/"

ismrm = re.search(MRM,p.name())

def selectConnectedNodes(startNodes):
    """sel all nodes in the tree of selected node"""
    
    allDeps = set()
    depsList = [startNodes]
    evaluateAll = True
    while depsList:
        deps = nuke.dependencies(depsList)
        depsList = [i for i in deps if i not in allDeps and not allDeps.add(i)]
        
    for i in allDeps:i['selected'].setValue(True)
    
    return list(nuke.selectedNodes())
    
    
def get_Disklist():
    
    s = str(psutil.disk_partitions())
    disk_list = []
    for c in string.ascii_uppercase:
        disk = c+':'
        if re.search(disk,s):
            disk_list.append(disk)
    return disk_list
    
    
def DeadlineErrorDetection(nodes):
    
    
    global er1
    global ProxyOne
    global ErrorRead
    global Readtwo
    global Pluginthree
    global WriteFourth
    global ErrorPlugin
    global ErrorWrite
    global rootError
    global fill
    
    
    SOURCE_localDisk = get_Disklist()       #local disk_list
    SOURCE2 = ''
    SOURCE3_Plugin = ['OFXuk.co.thefoundry.tinderbox','WorldPos_Lambert_Shader_ik','AFXGlow.gizmo']    #Plugin not in server
    SOURCE4 = ['.####.']
    SOURCE5_seq = ['%d','%02d','%03d','%04d','%05d','%06d','%07d','%08d','#','##','###','####','#####','######','#######','########']
    
    nodeList = selectConnectedNodes(nodes)
    
    
    #unselected or bug 
    
    for uns in nodeList:
        if not uns.Class() == nodes.Class():
            uns['selected'].setValue(False)
            
    
    #Read 
    
    w = nuke.allNodes('Write')
    
    readOne = ['Read','ReadGeo2','Camera2']
    
    Ra = []
    
    for rs in nodeList:
        if (rs.Class() == 'Read' or rs.Class() == 'ReadGeo2' or rs.Class() == 'Camera2'):
            Ra.append(rs)
            
            
    for s in Ra:
        
        if s.Class() == 'Camera2':
            if not s['read_from_file'].getValue():
                continue
            
        #singe read
        
        pat = ''
        ispath = 1 
        for sr in SOURCE5_seq:
            if re.search(sr,s['file'].getValue()):
                ispath = 0 
                pat = sr
                break
            
        if ispath == 1:
            newpath = s['file'].getValue()
            if not os.path.isfile(newpath):
                if not(re.search(str(s.name()),str(ErrorRead))):
                    ErrorRead.append(s.name())
                    
                Readtwo = 1 
                
                
                
        #sequence
        
        for s2 in SOURCE_localDisk:
            
            if(re.match(s2,s['file'].getValue() or not os.path.exists(os.path.dirname(s['file'].getValue()))):
                if not(re.search(str(s.name()),str(ErrorRead))):
                    ErrorRead.append(s.name())
                Readtwo = 1 
                
                
                
                
    #Plugin
    
    
    for s2 in nodeList:
        if s2.Class() != 'Read':
            for i in SOURCE3_Plugin:
                if re.search(i,s2.Class()) and s2.name() not in ErrorPlugin:
                    ErrorPlugin.append(s2.name())
                    Pluginthree = 1 
                    
    for sss in nuke.allNodes():
        if sss.Class() == "EdgeKey" and sss.name() not in ErrorPlugin and p['colorManagement'].value() == 'OCIO':
            ErrorPlugin.append(sss.name())
            Pluginthree = 1 
            
            
            
    #Write
    
    
    if(re.search('\.',nodes['file'].getValue())is not None):
        
        if nodes['file'].getValue().split('.')[-1].lower() == nodes['file_type'].value():
            WriteFourth = 2 
        else:
            WriteFourth = 1 
            ErrorWrite.append(nodes.name())
            
    else:
        ErrorWrite.append(nodes.name())
        print ErrorWrite
        WriteFourth = 1 
    if(re.search(' ',nodes['file'].getValue()) and (nodes.name() not in ErrorWrite)):
        WriteFourth = 1 
        print ErrorWrite
        ErrorWrite.append(nodes.name())
        
    for s31 in SOURCE_localDisk:
        if(re.match(s31,nodes['file'].getValue()) and (nodes.name() not in ErrorWrite)):
            ErrorWrite.append(nodes.name())
            WriteFourth = 1 
            
            
            
            
            
def Deteting(id = 1):
    
    global p 
    global er1
    global er0
    global ProxyOne
    global ErrorRead
    global Readtwo
    global Pluginthree
    global WriteFourth
    global ErrorPlugin
    global ErrorWrite
    global rootError
    
    
    
    
    
    nodes = nuke.selectedNodes()
    
    print nodes
    
    
    if len(nodes)<=0:
        nuke.message("No nodes selected")
        
        return [1],[1],[1]
    else:
        for i in nodes:
            if i.Class() != 'Write':
                nuke.message(i.name()+"is not WriteNode")
                return [1],[1],[1]
                
                
                
    SOURCE_localDisk = get_Disklist()
    
    for rn in SOURCE_localDisk:
        if re.match(rn,p['name'].getValue()):
            er0 = '<font color = "#f9efca"  size = "3"> project not in server\n\n'
            rootError = 1 
            
            
    if (p['proxy'].getValue() == 1):
        
        er1 = '<font color = "#f9efca"  size = "3"> You had  opened the proxy\n\n'
        
        ProxyOne = 1 
        
    else:
        er1 = ""
        
    for sel in nodes:
        
        DeadlineErrorDetection(sel)
        
        
        
    #message
    
    if(ProxyOne == 1 or Readtwo == 1 or Pluginthree == 1 or WriteFourth == 1 or rootError == 1):
        
        
        if len(ErrorPlugin):
            er3 = str(ErrorPlugin)+'\n\n\n'+'The Plugin has not intall'
        else:
            er3 = ""
            
        if len(ErrorRead):
            er2 = str(ErrorPlugin)+'\n\n\n'+'The read nodes is not in server'
        else:
            er2 = ""
            
        if len(ErrorWrite):
            er4 = str(ErrorWrite) + '\n\n\n' + 'The path have some problem'
        else:
            er4 = ""
            
        for resel in nodes:
            resel['selected'].setValue(True)
            
            
        if id == 1:
            nuke.message(er0 + '\n\n\n' + er1 +'\n\n\n' + er2 + '\n\n\n' + er3 + '\n\n\n' + er4 + '\n\n\n' + '\n\n\n' + op)
            
            
            
    Rread = ErrorRead
    RWrite = ErrorWrite
    RPlugin = ErrorPlugin
    return Rread,RWrite,RPlugin
    
    
    #Reset 
    
    
    Readtwo = 0 
    ProxyOne = 0 
    Pluginthree = 0 
    rootError = 0 
    WriteFourth = 2 
    ErrorRead = []
    ErrorPlugin = []
    ErrorWrite = []
    
    
    
    
        
