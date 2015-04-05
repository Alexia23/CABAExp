#decompression
import os
def filenamesList(dirpath):
	filelist = os.listdir(dirpath)
	for i in filelist:
		print i
filenamesList('originData/')