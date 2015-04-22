#coding=utf-8
import pylab as plt
import numpy as np
def getASNum(filename):
	f = open(filename, 'r');
	t1 = [];
	t2 = [];
	t3 = [];
	lines = f.readlines();
	index = 0;
	for line in lines:
		paras = line.split("|");
		index+=1;
		t1.append(index);
		t2.append(int(paras[1]));
		t3.append(int(paras[0]));

	plt.plot(t1,t2,'o');
	plt.title('Prefix Distribution For AS Quantity');
	plt.xlabel("Increasing As Quantity");
	plt.ylabel("Prefix Number");
	plt.savefig("3.jpg");

	plt.plot(t3,t2,'o');
	plt.title('Prefix Distribution For ASN');
	plt.xlabel("ASN");
	plt.ylabel("Prefix Number");
	plt.savefig("4.jpg");
	



def paintzhexian():
	colors = 'rgbcmykrgbcmyk'
	values = {};
	tp = {};
	for i in range(0,13):
		values[i]=[];
		tp[i] = [];
	for i in range(1,6):
		tfilename = "res"+str(i)+".txt";
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
	print values.values();
	for i in values.keys():
		plt.plot(x, values[i], color=colors[i]);
	plt.title("13 Routes Fib Reduction Ratio")
	plt.savefig("5.jpg");
	return tp;



colors = 'rgbcmyk' # red, green, blue, cyan, magenta, yellow, black
namesa = ['perth','isc','linux','kinp','sydney','wide','eqix','saopaulo','nmax','telxatl','jinx','soxrs','sg']
def zhuahungtuBar(info,routename):
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
	plt.savefig("2.jpg");
	plt.semilogy(1000);


#getASNum("as2addrs.txt")
tp = paintzhexian();
names = [1,2,3,4,5,6,7,8,9,10,11,12,13]

zhuahungtuBar(tp.values(), names);
