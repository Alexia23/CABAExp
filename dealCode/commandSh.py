#decompression
import os
def decompressionFiles(sourceDirPath):
	shfile = open("/home/wq/Work/simbgp/data/shfile/decompression.sh", 'w')
	filelist = os.listdir(sourceDirPath)
	for i in filelist:
		string = sourceDirPath
		pos = i.find(' ')
		if pos >= 0:
			string += i[0:pos] + "\\" + i[pos:len(i)]
		else:
			string += i
			shfile.write("bunzip2 " + string + "\n")
	shfile.close()

#use bgpdump to produce the visual text route table
def libDumpRunCommand(sourceDirPath, destPath, destDir):
	shfile = open("/home/wq/Work/simbgp/data/shfile/libDumpRunCommand.sh", 'w')
	if os.path.exists(destPath+destDir+'/'):
        		pass
    	else:
       		os.mkdir(destPath+destDir+'/')
	filelist = os.listdir(sourceDirPath)
	for i in filelist:
		shfile.write("/home/wq/Work/simbgp/code/cidr-report_analysis/libbgpdump/libbgpdump-1.4.99.13/bgpdump -M " 
			+ sourceDirPath + i
		 + " -O " + destPath+destDir+'/'+ i + ".out" + "\n")
	shfile.close()

#decompressionFiles('/home/wq/Work/simbgp/data/decompressionData/20150403.0000/')
'''libDumpRunCommand("/home/wq/Work/simbgp/data/decompressionData/20150403.0000/", 
	"/home/wq/Work/simbgp/data/vistualData/", "20150403.0000");'''

def simBgpCommand(pypath, configpath, shfilepath, num):
	f = open(shfilepath, 'w');
	for i in range(0, num):
		f.write("python " + pypath + " " + configpath +str(i) + "\n");
	f.close();

#CABA embedded ASN
def asn2Ipv6Prefix(asn):
	ipv6Str = str(hex(int(asn)))
	res = ''
	for i in range(10-len(ipv6Str)):
		res+='0'
	res+=ipv6Str;
	res+="00"
	return  res[0:4] + ':' + res[4:8]+':'+res[8:12]+"::"

#produce bgpsim config file
def produceConfig(filename, asPrefixInfo):
	f1 = open(asPrefixInfo, 'r');
	line1 = f1.readline();
	index = 0;
	while line1:
		asn = line1.split(" ")[0];
		outfilename = filename + str(index);
		fw = open(outfilename, "w");
		f = open(filename, 'r');
		line = f.readline();
		while line:
			fw.write(line);
			if line == "router bgp " + asn + "\n":
				line = f.readline();
				temp = line.split(' ');
				routeId = temp[-1][0:-1];
				fw.write(line);
			line = f.readline();
		fw.write("event announce-prefix " + routeId + " " + asn2Ipv6Prefix(asn) + " 2.0\n");
		fw.write("event terminate 40000.0");
		f.close();
		fw.close();
		line1 = f1.readline();
		index+=1;

