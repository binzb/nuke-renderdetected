import os
import nuke
import re
import upstream
import selGui


menubar = nuke.menu("nuke")
menubar.addCommand("RenderDetected/submit",

"""
try:
    srPanel.close()
except:
    pass
  
reload(upstream)
reload(selGui)

(Rread,Rwritr,Rplugin) = upstream.Detecting(0)

if len(Rread) != 0 or len(Rwrite) != 0 pr len(Rplugin) != 0:
    if(Rread != [1] and Rwrite != [1] and Rplugin != [1]):
        srPanel = selGui.Panel()
        srPanel = addknobs(Rread,Rwrite,Rplugin)
        srPanel.show()

""","ctrl+shift+alt+d",index = 0)
