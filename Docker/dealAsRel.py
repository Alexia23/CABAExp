#author:wangqing
#time:    2015-6-4-10-40
# get AS relations
import sys
AsMap = {}
AsnCus = []
AsnPro = []
def dealRelations(inputfile, outfile):
	f = open(inputfile, 'r')
	fw = open(outfile, 'w')
	line = "-1"
	while line:
		line = f.readline()
		line = line.strip()
		if len(line) < 1 or cmp(line[0:1],'#')==0:
			continue
		params = line.split('|') 
		if len(params) != 3:
			continue
		if cmp(params[2],'0') != 0 and cmp(params[2],'-1') != 0:
			continue
		if cmp(params[2],'0')==0:
			if params[0] in tier1List and params[1] in tier1List:
				fw.write(params[0]+"|"+params[1]+"\n")
		if cmp(params[2],'-1')==0:
			if params[0] in AsMap.keys():
				AsMap[params[0]].append(params[1])
			else:
				AsMap[params[0]] = [];
				AsMap[params[0]].append(params[1])
			if params[1] not in AsnCus:
				AsnCus.append(params[1])
			if params[0] not in AsnPro:
				AsnPro.append(params[0])
	tier1=[]
	for asNum in AsnPro:
		if asNum not in AsnCus:
			tier1.append(asNum)
			print asNum + "   " + str(len(AsMap[asNum]))
	print tier1
	print len(tier1)

['174', '209', '276', '286', '306', '701', '745', '1239', '1299', '1539', '1555', '1569', '1602', '1913', '2153', '2828', '2914', '3257', 
'3320', '3356', '3544', '3754', '4558', '5511', '5800', '6453', '6461', '6762', '6777', '7018', '7597', '7717', '10133', '10764', '12284', 
'13094', '16473', '16905', '17579', '19338', '20225', '22335', '22661', '23745', '23815', '23962', '24133', '24421', '24490', '24748', 
'26105', '27137', '27138', '27139', '27807', '28168', '28697', '29846', '30696', '31025', '32105', '35168', '37374', '37928', '38561',
 '42480', '42861', '44530', '44896', '45309', '47184', '47463', '47775', '49401', '52332', '52359', '52360', '52370', '52375', '52403', 
 '52404', '52482', '55073', '58942', '58943', '59900', '61180', '63516', '133100', '201054']

tier1Str="174 209 286 701 1239 1299 2828 2914 3257 3320 3356 4436 5511 6453 6461 6762 7018 12956"
tier1List=tier1Str.split(" ");
print tier1List
dealRelations( sys.argv[1], sys.argv[2])
