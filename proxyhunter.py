#support config file use 10 10.1 10.1.1 10.1.1.1 four kind patterns indicate hosts for check whether is a proxy server
#write only ip. no time cost 2014/9/10
import os, sys, socket, struct, select, time
import datetime
import threading  
 
sys.path.append("../mymodule")
import mt,func	
func.SHOW_LOG = False
#testdmode = 0 #just test a fix proxy to hunter
 
#default check this url

url = "http://www.tianya.cn/"    #"http://mail.google.com"
pattern = "<title>天涯社区_全球华人网上家园</title>"   #"http://mail.google.com/mail"

#url2 = "http://www.taobao.com/"    #"http://mail.google.com"
#pattern2 = "delta.taobao.com"   #"http://mail.google.com/mail"
    
def checkproxy(proxy , _url, _pattern  ):   
    timebefore =  time.time()
    content = func.httplib_version("GET",  _url,  None, None, proxy)
    timecost =  time.time()-timebefore   
    if content is None:
       print ("proxyhunter: failed to get response from %s use proxy %s"%(_url, proxy))
    
    if content is not None:       
      # print(content)
       if content.find(_pattern) != -1:                                         
            #print("proxyhunter: connected %s using proxy %s, cost %s s  " %(_url, proxy.ljust(20),   timecost))            
            return timecost            
       else:
       	   # content2 = content.decode('utf-8')
           # if content2.find(_pattern) != -1:                                         
           #    print("proxyhunter: connected %s using proxy %s, cost %s s  " %(_url, proxy.ljust(20),   timecost))            
           #    return timecost                   	    
            print("proxyhunter: get response from %s using proxy %s , but not find pattern %s     " %(_url, proxy.ljust(20), _pattern ))
            
            
    return 0 #failed    
    
                        
  
proxylist = []   
lock = threading.Lock()
def checkhostfunc(dest_addr, timeout = 1 ):       
    for port in [808, 8080]:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(timeout)    	
      result = s.connect_ex((dest_addr, port))
      s.close()
     
      if result == 0:                    
      	    proxy = "%s:%s" %(dest_addr, port)
            timecost = checkproxy(proxy, url, pattern)
            if timecost > 0:
            	 lock.acquire()
            	 #proxylist.append("%s %s\n" %(proxy.ljust(20), timecost))
            	 proxylist.append("%s" %(proxy.ljust(20)))
            	 lock.release()                 
            	 #timecost2 = checkproxy(proxy, url2, pattern2)
             	 #if timecost2 > 0:
                 #  print("proxyhunter: connected %s using proxy %s, cost %s s  " %(url2, proxy.ljust(20),   timecost))        
#                   lock.release()'''
    return None

def addtohostlist(eachnet, hostlist):
      NetNum = len(eachnet.split('.'))
      if   NetNum == 4:                   
      	   hostlist.append(eachnet)
      elif NetNum == 3:                   
         for eachhost in hostrange:
            host = "%s.%d" %(eachnet, eachhost)      
            hostlist.append(host)
      elif NetNum == 2:              	  
         for eachhost in hostrange:
         	   for eachhost2 in hostrange:
         	      host = "%s.%d.%d" %(eachnet, eachhost, eachhost2)      
         	      hostlist.append(host)
      elif NetNum == 1:              	
         for eachhost in hostrange:
         	for eachhost2 in hostrange:
         		for eachhost3 in hostrange:
         		    host = "%s.%d.%d.%d" %(eachnet, eachhost, eachhost2, eachhost3)      
         		    hostlist.append(host)
    
  
if __name__ == '__main__':


    hostlist = []
   
    timestart=  time.time()
   
    netlines = []
    if (len(sys.argv) > 1) :  
       argv1 = sys.argv[1]              
    else:
       argv1  = 'findhost.cfg'   
    if 'cfg' in argv1 : 
        configurefilename = argv1
        if not os.path.exists(configurefilename):
           sys.stderr.write('proxyhunter:  ERROR: sys.argv[1] was not found! missing .cfg filename or net address!')
           sys.exit(1)
        configurefile = open(configurefilename,'r')
        netlines = configurefile.readlines()
        configurefile.close()
    else:
        netlines.append(argv1)

    hostrange = range(1,255)  
    for eachLine in netlines: 
      eachnet = eachLine.strip()
      if len(eachnet) == 0:
          continue             
      addtohostlist(eachnet, hostlist)

        	
   
        
    thread_num = 3000
    if (len(hostlist) <  thread_num):
    	thread_num = len(hostlist)
    print(" I will check %d hosts using %s threads. \n " % (len(hostlist), thread_num))	
    	
    mt = mt.MT(checkhostfunc, hostlist, thread_num)
    mt.start()
    mt.join()
    
    #resultfilename =  'P' + datetime.date.today().strftime('%Y%m%d')+'.txt'
    resultfilename =  'proxy.txt'
    fpresult = open(resultfilename,'a')   
    if len(proxylist) > 0 :
       fpresult.write(datetime.datetime.fromtimestamp(time.time()).strftime('\n%Y-%m-%d %H:%M:%S\n'))
    for proxy in proxylist:
      fpresult.write("%s\n"%proxy)
    fpresult.flush()
    fpresult.close()
  
    print("proxyhunter   run cost %s s.  %s proxy servers found.\n" % (time.time()-timestart, len(proxylist))) 
    
  
      
