#encoding=utf-8
#Name: wang qing 
#Date: 2015-4-13 Monday
#Program: final deal data
import os
from parser import *

def reduceFIBs(sourcePath, destPath, destDir):
	filelist = os.listdir(sourcePath)
	if os.path.exists(destPath+destDir+'/'):
        		pass
    	else:
       		os.mkdir(destPath+destDir+'/')
	filelist = os.listdir(sourcePath)
	for i in filelist:
		reduceFIB(sourcePath+i, destPath+destDir+'/'+i+'.fib')

print "main.py"
reduceFIBs("/home/wq/Work/simbgp/data/vistualData/20150403.0000/", "/home/wq/Work/simbgp/data/FIBData/", "20150403.0000")