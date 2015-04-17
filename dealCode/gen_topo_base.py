#coding=utf-8
#!/usr/bin/env python
'''
修改之处
1、修改了过滤规则，把permit改成deny
2、修改了local-preference，customer的local-preference设为了100，peer的设为了50，provider的设为了10.
用法
1、gen_topo_wth的文件用法是genTopo.py configfile victimAS attackerAS，输入被攻击和攻击的AS可以直接生成配置文件。
2、gen_topo_base的用法是genTopo.py configfile，事件另外输入，例如第三个附件，这种用法适合大量事件模拟。'''
import sys
import networkx as nx
import random

NUMBER_OF_PREFIX=1
NUMBER_OF_FAILED_LINKS=0
basetime=10000.0
EVENT_INTERVAL=5000.0
degrees={}
selectedAS=[]
selectedLinks=[]
edgedAS=[]
coreAS=[]

G = None
def splitstr(line, pat):
    ele = [];
    i = 0;
    tmpstr = "";
    while i <= len(line):
        if i < len(line) and line[i] != pat:
            tmpstr = tmpstr + line[i];
        else:
            if tmpstr != "":
                ele.append(int(tmpstr));
                tmpstr = "";
        i = i + 1;
    return ele;

def readnextcmd(fh):
    try:
        line = fh.readline();
        while len(line) > 0 and (line[0]=='#' or len(splitstr(line[:-1],'|')) == 0):
            line = fh.readline();
        return splitstr(line[:-1], '|');
    except:
        print "Exception: ",sys.exc_info()[0];
        raise;
        
def readConfig(filename):
    global G;
    try:
        f = open(filename, "r");
        cmd = readnextcmd(f);
        while len(cmd) > 0:
            G.add_edge(cmd[0], cmd[1], relation=cmd[2]);
            G.add_edge(cmd[1], cmd[0], relation=-cmd[2]);
            cmd = readnextcmd(f);
        f.close();
    except:
        print "Exception: ", sys.exc_info()[0];
        raise;
def getRouterId(node):
    return "%d.%d.%d.%d" %((node/10000), (node%10000)/1000, (node%1000)/100, node%100)    

def preference(relations, u, v):
    if relations[(u,v)] > 0:
        return 100
    else:
        return 10
#
# Get all it's client provider and peer
# and it's sibling's client provider and peer
def businessGroup(Graph, relations, marked, node):
    clients = []
    providers = []
    peers = []
    if marked.has_key(node):
        return [[],[],[]]
    if not marked.has_key(node):
        marked[node] = True
    for v in G.edges_iter(node):
        if relations[v] == 0:
            peers.append(v)
        elif relations[v] == -1:
            clients.append(v)
        elif relations[v] == 1:
            providers.append(v)
        elif relations[v] == -2 or relations[v] == 2:
            [sib_clients, sib_prov, sib_peer] = businessGroup(Graph, relations, marked, v[1])
            clients.extend(sib_clients)
            providers.extend(sib_prov)
            peers.extend(sib_peer)
        else:
            print "error business relation"
            exit(1)
    # print "clients %s peers %s providers %s" %(clients, peers, providers)
    return [clients, providers, peers]

def needExportFilter(node, peers, providers):
    cnt=0
    for i in peers:
        if i[0]==node:
            cnt = cnt + 1
    for i in providers:
        if i[0]==node:
            cnt = cnt + 1
    return cnt>0 and len(peers)+len(providers)>1

def strRelations(relations, edge):
    if relations[edge] == 0:
        return "peers"
    elif relations[edge] == -1:
        return "clients"
    elif relations[edge] == 1:
        return "providers"
    elif relations[edge] == -2 or relations[edge] == 2:
        return "siblings"
    else:
        print "error business relations"
        exit(1)
    return "None"

def writeExportConfig(node, clients, providers, peers):
    peernum = len(peers) + len(providers)
    clientnum = len(clients)
    deny = ""
    print "route-map 2pref%d_%s deny 10" %(node, "filters")
    for edge in peers:
        if edge[0]==node:
            deny = deny + "|^" + str(edge[1])
        else:
            deny = deny + "|" + str(edge[0])+"_"+str(edge[1])
    for edge in providers:
        if edge[0]==node:
            deny = deny + "|^" + str(edge[1])
        else:
            deny = deny + "|" + str(edge[0])+"_"+str(edge[1])
    print " match as-path %s" %(deny[1:])
    print "" 

def writeImportConfig():
    tmplist = [("peers",50),("clients",100),("providers",10),("siblings", 100)]
    for v in tmplist:
        print "route-map 1pref_%s permit 10" %(v[0])
        print " set local-preference %d" %(v[1])
        print ""

def writeNeighborConfig(relations, node):
    marked = {}
    [clients, providers, peers] = businessGroup(G, relations, marked, node)
    flagExportFilter = needExportFilter(node, peers, providers)
    for edge in G.edges_iter(node):
        # print edge
        print " neighbor %s remote-as %d" %(getRouterId(edge[1]),edge[1])
        print " neighbor %s advertisement-interval 30" %(getRouterId(edge[1]))
        print " neighbor %s route-map 1pref_%s in" %(getRouterId(edge[1]), strRelations(relations, edge))
        if flagExportFilter and (relations[(edge[0],edge[1])] == 0 or relations[(edge[0],edge[1])] == 1):
            print " neighbor %s route-map 2pref%d_%s out" %(getRouterId(edge[1]), edge[0], "filters")
    print ""
    if flagExportFilter :
        writeExportConfig(node, clients, providers, peers)
    print ""


def writeEventConfig2():
    print "event announce-prefix  91.217.242.0 2.0" 

    print "event terminate 40000"
    print "debug show-receive-events"
    print "debug show-final-ribs"
    print "config epic"

def writeConfig():
    global G;
    relations=nx.get_edge_attributes(G, 'relation');
    print "!config hijacking simulation"
    print ""
    srcnode = None
    for node in G.nodes_iter():
        if srcnode is None:
            srcnode = node
        print "router bgp %s" %(node);
        print " bgp router-id %s" %(getRouterId(node));
        writeNeighborConfig(relations, node)
    writeImportConfig()
    

def writeAnalysis():
    global G,degrees;
    relations=nx.get_edge_attributes(G, 'relation')
    # print "node clients providers peers"
    for node in G.nodes_iter():
        marked = {}
        [clients, providers, peers] = businessGroup(G, relations, marked, node)
        degrees[node] = [len(clients), len(providers), len(peers)]

if len(sys.argv) < 2:
    print "Usage: genTopo.py configfile\n";
    sys.exit(-1);        

G = nx.DiGraph();

readConfig(sys.argv[1]);
writeAnalysis();
writeConfig();
#writeEventConfig2();
