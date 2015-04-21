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

#run for visual route view
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
libDumpRunCommand("/home/wq/Work/simbgp/data/decompressionData/20150403.0000/", 
	"/home/wq/Work/simbgp/data/vistualData/", "20150403.0000");


def produceConfig(filename, asPrefixInfo):
	f = open(filename, 'r');
	paras = asPrefixInfo.split("|");
	outfilename = filename + str(paras[1]);
	fw = open(outfilename, "w");
	line = f.readline();
	while line:
		fw.write(line);
		if line == "router bgp " + paras[0] + "\n":
			line = f.readline();
			
			fw.write(line);

		line = f.readline();
	for i in range(0, paras[1]):
		outfilename = filename + str(i);
		fw = open(outfilename, 'w');
		line = f.readline();
		while line:
			fw.write(line);
			line = f.readline();
		fwrite("event announce-prefix 1.9.3.91 0000:0x4b:bf00:: 2.0\n")
		fwrite("event terminate 40000.0")

