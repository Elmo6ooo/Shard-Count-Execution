#!/usr/bin/python3
from reset import factory_reset
import threading
import os
import sys
import time

#get specific line
def select_line(string, line_index):
    return string.splitlines()[line_index]

#extract results time
def extract_time(log):
    global Time
    for x in range(20):
        tmp = select_line(log, x)
        if "Skipping dynamic download due to local sharding detected." in tmp:
            Time = tmp[0:14]
            break
    Time = Time.replace(Time[2], '.').replace(Time[5],'_').replace(':','.')
    
#extract results session
def extract_session(log, Time):
    global session, pre_session_Fail
    for x in log.splitlines():
        if "Fail" in x:
            for i in range(len(x)):
                if x[i] == 'F':
                    index = i

        elif Time in x:
            new_session_fail = int(x[index:index+6])
            if(new_session_fail < pre_session_Fail):
                pre_session_Fail = new_session_fail
                session = int(x[0:3])
                break
            
        #this might not work when Time[sec] is 59
        elif Time.replace(Time[-1], str(int(Time[-1])+1)) in x: 
            new_session_fail = int(x[index:index+6])
            if(new_session_fail < pre_session_Fail):
                pre_session_Fail = new_session_fail
                session = int(x[0:3])
                break

#factory reset, wifi on, location on
def reset():
    threads = []
    for device in serial_num:
        t = threading.Thread(target =factory_reset , args = (device,))
        threads.append(t)
    #excute thread
    for i in range(len(serial_num)):
        threads[i].start()       
    #wait for end of t
    for i in range(len(serial_num)):
        threads[i].join()
    time.sleep(30)

#check parameters and set parameters
Mode = ''
retry_round = 0
serial_num = []
if sys.argv[1].lower() == False:
    print("Mode parameter is not lowercase!")
    sys.exit()
else:
    Mode = sys.argv[1]

if sys.argv[2].isnumeric() == False:
    print("Retry parameter is not numeric!")
    sys.exit()
else:
    retry_round = int(sys.argv[2])

s = ""
for i in range(3,len(sys.argv)):
    serial_num.append(sys.argv[i])
    s += " -s "+sys.argv[i]

#cd to dir
if Mode == 'gsi':
    os.chdir("/usr/local/google/home/chienliu/Downloads/android-cts/tools")
else:
    os.chdir("/usr/local/google/home/chienliu/Downloads/android-"+Mode+"/tools")

#excute full run
if Mode == 'gsi':
    p = os.popen("./cts-tradefed run commandAndExit cts-on-gsi --shard-count "+str(len(serial_num))+s)
elif Mode == 'sts':
    p = os.popen("./sts-tradefed run commandAndExit sts-dynamic-full --shard-count "+str(len(serial_num))+s)
else:
    p = os.popen("./"+Mode+"-tradefed run commandAndExit "+Mode+" --shard-count "+str(len(serial_num))+s)

#using terminal log to extract time 
Time = ""
extract_time(p.read())

session = 0
pre_session_Fail = 999999
#reset and then retry
for i in range(retry_round):
    #reset()

    #get session from l r
    if Mode == 'gsi':
        p = os.popen("./cts-tradefed l r")
    else:
        p = os.popen("./"+Mode+"-tradefed l r")    
    extract_session(p.read(), Time)
    print(session)

    #run retry
    if Mode == 'gsi':
        p = os.popen("./cts-tradefed run commandAndExit retry -r "+str(session)+" --shard-count "+str(len(serial_num))+s)
    else:
        p = os.popen("./"+Mode+"-tradefed run commandAndExit retry -r "+str(session)+" --shard-count "+str(len(serial_num))+s)

    #using terminal log to extract time 
    Time = ""
    extract_time(p.read())


if Mode == 'gsi':
    p = os.popen("./cts-tradefed l r")
else:
    p = os.popen("./"+Mode+"-tradefed l r")    
print(p.read())