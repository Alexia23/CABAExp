#coding=utf-8
#Program: use python to draw paint showing results 
import pylab as plt
import numpy as np
import math
def getASNum(filename):
	f = open(filename, 'r');
	t1 = [];
	t2 = [];
	t3 = [];
	lines = f.readlines();
	index = 0;
	sum = 0;
	for line in lines:
		paras = line.split("|");
		index+=1;
		t1.append(index);
		t2.append(int(paras[1]));
		t3.append(int(paras[0]));
		sum += int(paras[1])
	print sum

	'''plt.plot(t1,t2,'o');
	plt.title('Prefix Distribution For AS Quantity');
	plt.xlabel("Increasing As Quantity");
	plt.ylabel("Prefix Number");
	plt.savefig("3.jpg");

	plt.plot(t3,t2,'o');
	plt.title('Prefix Distribution For ASN');
	plt.xlabel("ASN");
	plt.ylabel("Prefix Number");
	plt.savefig("4.jpg");
	'''
	newt2 = sorted(t2);
	
	'''print newt2;
	newt3 = [];
	for i in newt2:
		newt3.append(math.log10(i));
	plt.plot(t1,newt3);
	plt.title('Prefix Distribution For ASN');
	plt.xlabel("Increasing As Quantity Ordered By Prefix Num");
	plt.ylabel("log10(Prefix Number)");
	plt.savefig("7.jpg");'''

	res = [];
	for i in range(1,len(newt2)+1):
		sum = 0;
		for j in range(0,i):
			sum += newt2[j];
		ave = sum*1.0/i;
		res.append(ave);
	for i  in range(0, len(newt2)):
		print str(newt2[i]);
	for i  in range(0, len(t1)):
		print str(t1[i]) + "  " + str(res[i]);
	plt.plot(t1,res);
	plt.title('Prefix Distribution For ASN');
	plt.xlabel("Increasing As Quantity Ordered By Prefix Num");
	plt.ylabel("Average Prefix Number");
	plt.savefig("6.jpg");

namesa = ['perth','isc','linx','kixp','sydney','wide','eqix','saopaulo','nwax','telxatl','jinx','soxrs','sg']

def paintzhexian(filename,savefilename):
	colors = 'rgbcmykrgbcmyk'
	marks='x+vosp*dhH|<2'
	line1="-."
	line2="--"
	line3="-"
	line4=":"
	alines=[]
	for i in range(0,13):
		alines.append("")
	alines[0]=line1
	alines[1]=line2
	alines[2]=line3
	alines[3]=line4
	for i in range(0,13):
		alines[i]=alines[i%4]
	print alines
	alines[11]=line2
	values = {};
	tp = {};
	for i in range(0,13):
		values[i]=[];
		tp[i] = [];
	for i in range(1,6):
		tfilename = filename + "res"+str(i)+".txt";
		f = open(tfilename);
		lines = f.readlines();
		index = 0;
		for line in lines:
			params = line.split(" ");
			t = float(params[-1][0:-1]);
			values[index].append(t);
			if int(params[1]) not in tp[index]:
				tp[index].append(int(params[1]));
			tp[index].append(int(params[2]));
			index+=1;
		f.close();
	x = [0.2,0.4,0.6,0.8,1.0];
	#print values.values();
	for i in values.keys():
		#print "----------" + colors[i]+marks[i]+lines[i];
		plt.plot(x, values[i],  colors[i]+marks[i]+alines[i]);
		if i==0 or i==3 or i==11:
			plt.text(x[1], values[i][1],namesa[i])
	plt.title("The trend for proportion of compressed data");
	plt.xlabel("Proportion of new strategy");
	plt.ylabel("Proportion of compressed data");
	plt.savefig(savefilename);
	return tp;



colors = 'rgbcmyk' # red, green, blue, cyan, magenta, yellow, black

def zhuzhungtuBar(info,routename, savefilename):
	left = 0;
	width = 4;
	bar_groups =[];
	lefts = [];
	for i in range(len(info)):
		for j in range(len(info[i])):
			plt.bar(i*40+j*width, info[i][j],width, color=colors[j], align="center");
		lefts.append(i*40+width);
	plt.xticks(lefts, routename)
	plt.title("red-normal  green-0.2 blue-0.4 cyan-0.6 magenta-0.8 yellow-1.0");
	plt.ylabel("Fib num");
	string ="";
	for names in namesa:
		string += names + ' ';
	plt.xlabel(string)
	plt.savefig(savefilename);
	plt.semilogy(1000);



getASNum("as2addrsNew.txt")

#tp = paintzhexian("/home/cnpt/wqfile/simbgp/data/finalResult/fibresult/20150502/", "orderedAsn.jpg");
#names = [1,2,3,4,5,6,7,8,9,10,11,12,13]

#zhuzhungtuBar(tp.values(), names, "unorderedAsnZZT.jpg");
