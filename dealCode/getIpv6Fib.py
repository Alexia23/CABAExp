#Name: wang qing 
#Date: 2015-4-3 Friday
#Program: change ipv4 fib  to ipv6 fib for CABA   

#TABLE_DUMP_V2|03/31/15 02:00:00|A|206.126.236.37|6939|1.0.224.0/19|6939 38040 9737|IGP
import random
class RouteInfo:
	def __init__(self, routeName, time, type, addr, asn, prefix, asPath, protocol, sourceAs):
		self.routeName = routeName;
		self.time = time;
		self.type = type;
		self.addr = addr;
		self.asn = asn;
		self.prefix = prefix;
		self.asPath = asPath;
		self.protocol = protocol;
		self.sourceAs = sourceAs;
	def printRouteInfo(self):
		print self.asn;
		print self.asPath;
	def modifyRouteInfo(self, routeInfo):
		paramsRecord = self.asPath.split(' ');
		params = routeInfo.asPath.split(' ');
		numRecord = len(paramsRecord);
		num = len(params);
		if num > numRecord:
			return;
		elif num  < numRecord:
			self = routeInfo;
		elif num == numRecord and int(params[0])< int(paramsRecord[0]):
			self = routeInfo;
		else:
			return;
	def aS2Ipv6Addr(self):
		ipv6Str = str(hex(int(self.sourceAs)))
		res = ''
		for i in range(10-len(ipv6Str)):
			res+='0'
		res+=ipv6Str;
		res+="00"
		self.prefix = res[0:4] + ':' + res[4:8]+':'+res[8:12]+"::"
	def  RouteInfoToStr(self):
		return self.routeName + '|' + self.time+'|' + self.type + '|' + self.addr + '|' + self.asn + '|' + self.prefix + '|' + self.asPath + '|' + self.protocol;



#input route table , output source-as|prefix1|prefix2|......  if the number of source-as is more than one, ignore this data. 
def getAsToAddrs(inputfile, outputfile):
	f = open(inputfile, 'r')
	fw = open(outputfile, 'w')
	line = f.readline()
	as2Addr = {}
	while line:
		params = line.split('|')
		line = f.readline()
		if len(params) < 8:
			continue
		asNums = params[6].split(' ')
		if asNums < 1:
			continue
		if asNums[-1][0] == '{':
			asNums[-1] = asNums[-1][1:-1]
			temp = asNums[-1].split(',')
			if  len(temp) != 1:
				continue
		if asNums[-1] in as2Addr.keys():
			if params[5] in as2Addr[asNums[-1]]:
				continue
			else:
				as2Addr[asNums[-1]].append(params[5])
		else:
			as2Addr[asNums[-1]] = []
			as2Addr[asNums[-1]].append(params[5])
	for i in as2Addr.keys():
		fw.write(i+'|')
		fw.write(str(len(as2Addr[i]))+'|')
		for j in as2Addr[i]:
			fw.write(j + '|')
		fw.write('\n')


#produce asn
def produceAsn(filename, num, outputfile):
	f = open(filename, 'r');
	fw = open(outputfile, 'w');
	asPrefixDistribution = {};
	asPrefixs = {};
	line = f.readline();
	while line:
		paras = line.split('|');
		if paras[1] in asPrefixDistribution.keys():
			asPrefixDistribution[int(paras[1])].append(paras[0]);
		else:
			asPrefixDistribution[int(paras[1])]=[];
			asPrefixDistribution[int(paras[1])].append(paras[0]);
		asPrefixs[paras[0]] = line;
		line = f.readline();
	asPrefixNum = [];
	asPrefixNum = sorted(asPrefixDistribution.keys());
	resAs = [];
	for i in range(0, num):
		left = len(asPrefixNum)/num*i;
		right = len(asPrefixNum)/num*(i+1);
		randomvalue = random.randint(left, right);
		randomasn = random.sample(asPrefixDistribution[asPrefixNum[randomvalue]], 1);
		fw.write(str(randomasn[0]) + " " + asPrefixs[randomasn[0]].split('|')[1] + "\n");
		resAs.append(asPrefixs[randomasn[0]]);

#input FIB table and arranged ASNs, output new FIB table
def  reduceIpv6Fib(inputfile, outputfile, asns):
	f  = open(inputfile, 'r');
	fw = open(outputfile, "w");
	lines = f.readlines();
	results= {};
	index = 0;
	index1 = 0;
	for line in lines:
		params = line.split('|');
		if len(params) < 8:
			continue;
		asNums = params[6].split(' ');
		if asNums < 1:
			continue;
		if asNums[-1][0] == '{':
			asNums[-1] = asNums[-1][1:-1];
			temp = asNums[-1].split(',');
			if len(temp) > 1:
				continue;
		index1 += 1;
		route = RouteInfo(params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7], asNums[-1]);
		if asNums[-1] not in asns: 
			index+= 1;
			fw.write(line);
		else:
			if route.sourceAs in results.keys():
				routeRecord = results[route.sourceAs];
				routeRecord.modifyRouteInfo(route);
			else:
				results[route.sourceAs] = route;
	for value in results.values():
		value.aS2Ipv6Addr();
		fw.write(value.RouteInfoToStr());
	fw.close();
	f.close();
	return index1, len(results)+index
