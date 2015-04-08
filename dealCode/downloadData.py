#encoding=utf-8
#Name: wang qing 
#Date: 2015-4-3 Friday
#Program: download data
#Ref: http://blog.csdn.net/linda1000/article/details/8255771
from ftplib import FTP
def ftpconnect(ftp_server_name):
    ftp_server = ftp_server_name
    username = ''
    password = ''
    ftp=FTP()
    ftp.set_debuglevel(2)                #打开调试级别2，显示详细信息
    ftp.connect(ftp_server,21)        #连接
    ftp.login(username,password) #登录，如果匿名登录则用空串代替即可
    return ftp

def downloadfile(filepath):  
    ftp = ftpconnect('archive.routeviews.org')    
    #print ftp.getwelcome() #显示ftp服务器欢迎信息
    bufsize = 1024 #设置缓冲块大小      
    fp = open('/home/wq/Work/simbgp/data/' + filepath.split('/')[1] + '- ' + filepath.split('/')[-1] ,'w'); #以写模式在本地打开文件
    #print '/home/wq/Work/simbgp/data/' + filepath.split('/')[1] + '- ' + filepath.split('/')[-1];
    ftp.retrbinary('RETR ' + filepath, fp.write, bufsize) #接收服务器上文件并写入本地文件
    ftp.set_debuglevel(0) #关闭调试
    fp.close()
    ftp.quit() #退出ftp服务器

def getDownloadPath(date, time): #downloadfile("/route-views.eqix/bgpdata/2015.04/RIBS/rib.20150401.0000.bz2")  date:2015.04    time
    ftp = ftpconnect('archive.routeviews.org')
    for dirName in ftp.nlst()[11:-7]:
        path = '/' + dirName + '/bgpdata/' + date + '/RIBS/' + 'rib.'+time+'.bz2';
        #print path
        downloadfile(path)

getDownloadPath('2015.04', '20150403.0000')