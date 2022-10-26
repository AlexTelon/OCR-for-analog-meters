import os

def getProcessedFileName(name, quality_percent, color_depth):
    orgNameSplit = os.path.splitext(name)
    newName = orgNameSplit[0]+'_'+color_depth+'_'+str(quality_percent)+'ppt'
    return newName