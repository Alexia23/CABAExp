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


def reduceIpv6Fib(inputfile, asn_substitutefile, outputfile):
	asn_substitute = {}
	fas = open(asn_substitutefile, 'r')
	line = fas.readline()
	while line:
		if line[-1]  == "\n":
			line = line[0:-1]
		params = line.split(" ")
		if len(params) != 2:
			line = fas.readline()
			continue
		if params[0] in asn_substitute.keys():
			line = fas.readline()
			continue
		else:
			asn_substitute[params[0]] = params[1]
		line = fas.readline()

	f = open(inputfile, 'r')
	fw = open(outputfile, 'w')
	line = f.readline()
	asnMark = {}
	while line:
		params = line.split(" ")
		if len(params) != 3:
			line = f.readline()
			continue
		if params[2][-1] == "\n":
			params[2] = params[2][:-1]
		if params[2] not in asn_substitute.keys():
			if params[2] not in asnMark.keys():
				asnMark[params[2]] = 1
				fw.write(params[0] + " " + params[1] + " " + params[2] + "\n")
			line = f.readline()
			continue
		else:
			params[0] = aS2Ipv6Addr(asn_substitute[params[2]])
			params[2] = asn_substitute[params[2]]
			if params[2] not in asnMark.keys():
				asnMark[params[2]] = 1
				fw.write(params[0] + " " + params[1] + " " + params[2] + "\n")
		line = f.readline()
	f.close()
	fw.close()


reduceIpv6Fib(sys.argv[1], sys.argv[2], sys.argv[3])
