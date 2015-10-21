#author:wangqing
#time:    2015-10-21
# get fib info ipv6fib

import sys
def aS2Ipv6Addr(asn):
	ipv6Str = str(hex(int(asn)))
	res = ''
	for i in range(10-len(ipv6Str)):
		res+='0'
	res+=ipv6Str;
	res+="00"
	return res[0:4] + ':' + res[4:8]+':'+res[8:12]+"::"


def reduceIpv6Fib(inputfile, outputfile):
	f = open(inputfile, 'r')
	fw = open(outputfile, 'w')
	line = f.readline()
	asnMark = {}
	while line:
		params = line.split(" ")
		if params[2][-1] == "\n":
			params[2] = params[2][:-1]
		if params[2] in asnMark.keys():
			line = f.readline()
			continue
		else:
			asnMark[params[2]] = 1
			params[0] = aS2Ipv6Addr(params[2])
		fw.write(params[0] + " " + params[1] + " " + params[2] + "\n")
		line = f.readline()
	f.close()
	fw.close()


reduceIpv6Fib(sys.argv[1], sys.argv[2])
