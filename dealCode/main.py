#encoding=utf-8
#Name: wang qing 
#Date: 2015-4-13 Monday
#Program: final deal data
import os
from parser import *
from getIpv6Fib import *

def reduceFIBs(sourcePath, destPath, destDir):
	filelist = os.listdir(sourcePath)
	if os.path.exists(destPath+destDir+'/'):
        		pass
    	else:
       		os.mkdir(destPath+destDir+'/')
	filelist = os.listdir(sourcePath)
	for i in filelist:
		reduceFIB(sourcePath+i, destPath+destDir+'/'+i+'.fib')

def reduceIpv6FIBs(sourcePath, destPath, destDir, percentage):
	filelist = os.listdir(sourcePath)
	if os.path.exists(destPath+destDir+'/'):
		os.popen('rm -rf  ' + destPath+destDir+'/')
		os.mkdir(destPath+destDir+'/')
    	else:
       		os.mkdir(destPath+destDir+'/')
	filelist = os.listdir(sourcePath)
	fw = open(destPath+destDir+'/res.txt', 'w')
	allfibnum = 0
	allipv6fibnum = 0
	for i in filelist:
		res = reduceIpv6Fib(sourcePath+i, destPath+destDir+'/'+i+'.ipv6fib', percentage)
		fw.write(sourcePath+i +"    " + str(res[0]) + "  " + str(res[1]) + "  " + "\n")
		allfibnum += res[0]
		allipv6fibnum += res[1]
	fw.write("all fib" + "  percentage: " + str(percentage) + "    " + str(allfibnum) + "   " + str(allipv6fibnum) + "\n")
	fw.close()
print "main.py"
#reduceFIBs("/home/wq/Work/simbgp/data/vistualData/20150403.0000/", "/home/wq/Work/simbgp/data/FIBData/", "20150403.0000")
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.2", 0.2)
'''reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.4", 0.4)
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.6", 0.6)
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.8", 0.8)
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.1.0", 1)'''
