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
	for i in filelist:
		res = reduceIpv6Fib(sourcePath+i, destPath+destDir+'/'+i+'.ipv6fib', percentage)
		fw.write(sourcePath+i +"            " + str(res[0]) + "           " + str(res[1]) + "           percentage: " + str(res[1]*1.0/res[0]) + "\n")
	fw.close()
print "main.py"

def asn2Ipv6Prefix(asn):
	ipv6Str = str(hex(int(asn)))
	res = ''
	for i in range(10-len(ipv6Str)):
		res+='0'
	res+=ipv6Str;
	res+="00"
	return  res[0:4] + ':' + res[4:8]+':'+res[8:12]+"::"
'''reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.2", 0.2)
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.4", 0.4)
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.6", 0.6)
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.0.8", 0.8)
reduceIpv6FIBs( "/home/wq/Work/simbgp/data/FIBData/20150403.0000/", "/home/wq/Work/simbgp/data/Ipv6FIBData/","20150403.0000.1.0", 1)'''

'''
getAsToAddrs("/home/cnpt/wqfile/simbgp/data/FIBData/20150403.0000/route-views.saopaulo-rib.20150403.0000.out.fib",
 "/home/cnpt/wqfile/CABAsimBgp/tempdata/as2addrs.txt")'''

produceAsn("/home/cnpt/wqfile/CABAsimBgp/tempdata/as2addrs.txt", 10, "/home/cnpt/wqfile/CABAsimBgp/tempdata/as2addrs.out");

