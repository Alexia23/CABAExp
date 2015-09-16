import sys
#Program install Quagga into a container and then input the network topology and then create container and build network. 
# about IPv6 network [function create sh script]
class route:
	def __init__(self, index, neighbors, prefix):
		self.index = index
		self.neighbors = neighbors
		self.prefix = getPredix(index)
		self.router_id =  getRouterId(int(index))
	def printRoute(self):
		print "ok"

class link:
	def __init__(self, link_index, router1_index, router2_index):
		self.link_index = link_index
		self.router1_index = router1_index
		self.router2_index = router2_index
		self.hd1 = getHd(router1_index)
		self.hd2 = getHd(router2_index)
		self.ipv6addr1 = getIpv6Addr(link_index, router1_index)
		self.ipv6addr2 = getIpv6Addr(link_index, router2_index)
	def printLink(self):
		print str(self.link_index) + "  " + self.router1_index + " " + self.router2_index +"  " + self.hd1 + " " + self.hd2 + " "  + self.ipv6addr1 + " "  + self.ipv6addr2

def getRouterId(node):
    return "%d.%d.%d.%d" %((node/10000), (node%10000)/1000, (node%1000)/100, node%100) 

def getIpv6Addr(link_index, index):
		indexHexStr = str(hex(int(index)))[2:]
		return'11:' + str(hex(int(link_index)))[2:]+"::"+indexHexStr+"/64"
def getHd(index):
	indexHexStr = str(hex(int(index)))[2:]
	res = indexHexStr
	result = ''
	for i in range(0, 12-len(indexHexStr)):
		res+='f'
	for i in range(0,6):
		result += res[i*2:i*2+2]+':'
	return result[0:-1]

def getPredix(index):
	indexHexStr = str(hex(int(index)))[2:]
	res = '10'
	for i in range(8-len(indexHexStr)):
		res+='0'
	res+=indexHexStr;
	res+="00"
	return res[0:4] + ':' + res[4:8]+':'+res[8:12]+"::/64"
def dealAsPeerRelation(filename):
	f = open(filename, 'r')
	line = 'test'
	linkindex = 0
	linkall = []
	routeall = {}
	while line:
		line = f.readline()[0:-1]
		params = line.split('|')
		if len(params) != 2 or cmp(params[0], params[1])==0:
			continue
		params[0].strip()
		params[1].strip()
		if int(params[0]) > int(params[1]):
			linkTemp = link(linkindex, params[1], params[0])
		else:
			linkTemp = link(linkindex, params[0], params[1])

		if not (params[0]  in routeall.keys()):
			routeall[params[0]] = route(params[0],[],'')
		temp = []
		temp.append(params[1])
		temp.append(linkTemp.ipv6addr2)
		if not temp  in routeall[params[0]].neighbors:
			routeall[params[0]].neighbors.append(temp)

		if not params[1]  in routeall.keys():
			routeall[params[1]] = route(params[1],[],'')
		temp = []
		temp.append(params[0])
		temp.append(linkTemp.ipv6addr1)
		if not temp in routeall[params[1]].neighbors:
			routeall[params[1]].neighbors.append(temp)

		linkall.append(linkTemp)
		linkindex += 1
	for i in linkall:
		i.printLink()
	for j in routeall:
		routeall[j].printRoute()
	return linkall, routeall

		
def buildBridge(filename, bridgeName, bridgeIpv4):
	f = open(filename, 'w')
	command = "sudo brctl addbr " + bridgeName + "\n"
	f.write(command)
	#must set ipv4 addr
	command = "sudo ip addr add  " + bridgeIpv4 + " dev  " + bridgeName + "\n"
	f.write(command)
	command = "sudo ip link set dev " + bridgeName + " up\n"
	f.write(command)
	command = "sudo chmod +x " + filename + "\n"
	f.write(command)
	f.close()



def createContainer(filename, imageName, routeInfo):
	f = open(filename, 'w')
	for i in routeInfo:
		command = "docker tag " + imageName + " ubuntu_quagga:router"+str(i)+"\n"
		f.write(command)
		f.write("docker rm router" + str(i)+"\n")
		command = "sudo docker run -i -t -d --volumes-from dbdata --net=none --name=router" + str(i) + " ubuntu_quagga:router" + str(i) + " /bin/bash\n"
		f.write(command)
	command = "sudo chmod +x " + filename + "\n"
	f.write(command)
	f.close()
	
def buildVlan(filename, linkInfo, bridgeName):
	f = open(filename, 'w')
	f.write("sudo mkdir -p /var/run/netns\n")
	for onelink in linkInfo:
		f.write( "contain1Name=router"+onelink.router1_index+"\n")
		f.write("pid=$(docker inspect -f '{{.State.Pid}}' $contain1Name)\n")
		f.write("sudo ln -s /proc/$pid/ns/net /var/run/netns/$pid\n")

		f.write("bridgeName="+bridgeName+"\n")
		f.write("bridgeIfName=link1-"+str(onelink.link_index) + "\n")
		f.write("devIfName=eth0-"+str(onelink.link_index)+"\n")
		f.write("sudo ip link add $bridgeIfName type veth peer name $devIfName\n")
		f.write("sudo brctl addif $bridgeName $bridgeIfName\n")
		f.write("sudo ip link set $bridgeIfName up\n")

		f.write("hd="+onelink.hd1+"\n")
		f.write("ipaddr="+onelink.ipv6addr1+"\n")
		f.write("sudo ip link set $devIfName netns $pid\n")
		f.write("sudo ip netns exec $pid ip link set $devIfName address $hd\n")
		f.write("sudo ip netns exec $pid ip link set $devIfName up\n")
		f.write("sudo ip netns exec $pid ip addr add $ipaddr dev $devIfName\n")


		f.write( "contain2Name=router"+onelink.router2_index+"\n")
		f.write("pid=$(docker inspect -f '{{.State.Pid}}' $contain2Name)\n")
		f.write("sudo ln -s /proc/$pid/ns/net /var/run/netns/$pid\n")

		f.write("bridgeIfName=link2-"+str(onelink.link_index) + "\n")
		f.write("devIfName=eth0-"+str(onelink.link_index)+"\n")
		f.write("sudo ip link add $bridgeIfName type veth peer name $devIfName\n")
		f.write("sudo brctl addif $bridgeName $bridgeIfName\n")
		f.write("sudo ip link set $bridgeIfName up\n")

		f.write("hd="+onelink.hd2+"\n")
		f.write("ipaddr="+onelink.ipv6addr2+"\n")
		f.write("sudo ip link set $devIfName netns $pid\n")
		f.write("sudo ip netns exec $pid ip link set $devIfName address $hd\n")
		f.write("sudo ip netns exec $pid ip link set $devIfName up\n")
		f.write("sudo ip netns exec $pid ip addr add $ipaddr dev $devIfName\n")

	f.write( "sudo chmod +x " + filename + "\n")
	f.close()

def  createBgpConf(routeInfo, linkInfo):
	for oneroute in routeInfo.values():
		f = open("/home/cnpt/bgpdconf/bgpd.conf."+oneroute.index, 'w')
		f.write("hostname bgpd\n")
		f.write("password zebra\n")
		f.write("log stdout\n")
		f.write("line vty\n")
		f.write("router bgp "+oneroute.index+"\n")
		#must config router-id ,or not work
		f.write(" bgp router-id "+ oneroute.router_id+"\n")
		#neighbor must outside address-family
		for neighborLink in oneroute.neighbors:
			f.write(" neighbor " + neighborLink[1][0:-3] + " remote-as " + neighborLink[0] + "\n")
		f.write(" address-family ipv6\n")
		f.write(" network " + oneroute.prefix + "\n")
		for neighborLink in oneroute.neighbors:
			f.write(" neighbor " + neighborLink[1] [0:-3]+ "  activate\n")
		f.write(" exit-address-family\n")
		f.close()

def updateBgpConf(filename, routeInfo):
	f = open(filename,'w')
	for oneAns in routeInfo.keys():
		f.write("docker exec router"+oneAns+" cp /home/bgpd.conf."+oneAns + " /etc/quagga/bgpd.conf\n")
		f.write("docker exec router"+oneAns+" zebra -d\n")
		f.write("docker exec router" +oneAns+" bgpd -d\n")
	f.write( "sudo chmod +x " + filename + "\n")
	f.close()

buildBridge('buildBridge.sh', "bridge0", "192.168.5.1/24")

res = dealAsPeerRelation(sys.argv[1])
link_res = res[0]
route_res = res[1]

createContainer('createContainer.sh', "ubuntu_quagga:router", route_res)
buildVlan("buildVlan.sh", link_res, "bridge0")
createBgpConf(route_res,link_res)
updateBgpConf("updateBgpConf.sh", route_res)

