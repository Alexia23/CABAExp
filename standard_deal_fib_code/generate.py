#author:wangqing
#time:    2015-10-21
# get fib info (prefix, nexthop,origin as)

import os
import sys

#one prefix <==> many paths , this function to find the better path (length is shortest and the next hop ASN is smallest)
def  handleOneRouteInfo(onePrefixInfo):
	if len(onePrefixInfo) <= 0:
		return '';
	minPathNum =  4394967295;
	minPathAS = 4394967295;
	markIndex = -1;
	flag = False;
	for i in range(len(onePrefixInfo)):
		paths = onePrefixInfo[i][6].split(' ');
		flag = False;
		if minPathNum > len(paths) and len(paths) > 0:
			flag = True;
		elif minPathNum == len(paths) and len(paths) > 0 and int(paths[0]) < minPathAS:
			flag = True;
		else:
			flag = False;
		if flag == True:
			minPathAS = int(paths[0]);
			minPathNum = len(paths);
			markIndex = i;
	return onePrefixInfo[markIndex];

def prefixInfoListToStr(prefixInfos):
	strTemp = '';
	index = [5, 4]
	if  len(prefixInfos) < 7:
		return ""
	for i in index:
		strTemp += str(prefixInfos[i]);
		strTemp +=' '
	asPath = prefixInfos[6].split(' ')
	if asPath[-1][0] == "{":
		asPath[-1] = asPath[-1][1:-1]
		originAs = asPath[-1].split(",")
		if len(originAs) != 1:
			return ""
		else:
			asPath[-1] = originAs[0]
	strTemp += str(asPath[-1]);
	strTemp += '\n'
	return strTemp


def  reduceFIB(inputFile, outFile):
	f  = open(inputFile, 'r');
	fw = open(outFile,'w');
	line = f.readline();
	lastIPPrefix = '';
	onePrefixInfo = [];
	strTemp=""
	while line != '':
		infos = line.split('|');
		if len(infos) <= 5:
			line = f.readline();
			continue;
		if lastIPPrefix != infos[5]:
			writeinfos = handleOneRouteInfo(onePrefixInfo);
			fw.write(prefixInfoListToStr(writeinfos));
			onePrefixInfo = [];
			lastIPPrefix = infos[5];
			onePrefixInfo.append(infos);
		else:
			onePrefixInfo.append(infos);
		line = f.readline();
	writeinfos = handleOneRouteInfo(onePrefixInfo);
	fw.write(prefixInfoListToStr(writeinfos));
	fw.close();
	f.close();


os.system("bunzip2 -k " + sys.argv[1])
decompfilename =  sys.argv[1] [0:-4]
ribfilename =  decompfilename + ".view"
os.system("~/wqfile/gitcode/CABAExp/libbgpdump/cidr-report_analysis-master/libbgpdump/libbgpdump-1.4.99.13/bgpdump -M " + decompfilename + " -O " + ribfilename)
reduceFIB(ribfilename, sys.argv[2])
os.system("rm -rf  " + decompfilename)
os.system("rm -rf " + ribfilename)