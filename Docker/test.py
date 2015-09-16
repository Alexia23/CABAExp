import sys
def getReation(filename):
# c1: 174 209 286 701 1239 1299 2828 2914 3257 3320 3356 4436 5511 6453 6461 6762 7018 12956
	test=["174","209","286","701","1239", "1299","2828","2914","3257","3320","3356","4436","5511","6453","6461","6762","7018","12956"];
	matrix={}
	values=[]
	for i in range(0,18):
		matrix[test[i]]=i
		p=[];
		for j in range(0,18):
			p.append(0)
		p[i]=1
		values.append(p)


	f=open(filename,'r')
	line="wq";
	while line:
		line = f.readline()[0:-1]
		params = line.split('|')
		if len(params) != 2 or cmp(params[0], params[1])==0:
			continue
		params[0].strip()
		params[1].strip()
		values[matrix[params[0]]][matrix[params[1]]]=1
		values[matrix[params[1]]][matrix[params[0]]]=1

	for i in range(0,18):
		for j in range(0,18):
			if values[i][j]==0:
				print str(i) +"  " +str(j) + "\n"



getReation(sys.argv[1])


