#https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects
#FIB
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
	for i in range(len(prefixInfos)-1):
		strTemp += str(prefixInfos[i]);
		strTemp +='|';
	if  len(prefixInfos)>=1:
		strTemp += prefixInfos[len(prefixInfos)-1];
	return strTemp;





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