#decompression
import os
def filenamesList(dirpath):
	shfile = open("/home/wq/Work/simbgp/data/decompression.sh", 'w')
	filelist = os.listdir(dirpath)
	for i in filelist:
		pos = i.find(' ')
		string = i[0:pos] + "\\" + i[pos:len(i)]
		shfile.write("bunzip2 " + string + "\n")
	shfile.close()


filenamesList('/home/wq/Work/simbgp/data/')
