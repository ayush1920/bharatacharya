import threading
import time
global threadlist
global threadlimit
import sys
usagedict={}

usagedict["limit"] ="""
function    - setlimit | setlimit(limit)
usage       - set limit for maximum number of threads
parameters  -
compulsory :  limit - number of simultaneous threads
Eamples    :
              set limit:
                import multithread as mt
                mt.setlimit(20)
"""

usagedict["init"] ="""
function    - init | init(fun, args=[])
usage       - initiate new thread
parameters  -
compulsory :  fun - name of the target function

optional   :  arguments - args[] arguments for the function

Eamples    :
              Initialize without parameters -
                import multithread as mt
                mt.init(function1)
                
              Initialize with parameter -
                import multithread as mt
                mt.init(function1, [1,2,3])
"""

usagedict["check"] ="""
function    - checkfinished | checkfinished()
usage       - pauses the main thread till all thread ends
parameters  : No Parameter

Eamples    :
              wait for all threads to finish
                import multithread as mt
                mt.checkfinished()
"""

usagedict["killall"] ="""
function    - killall | killall(switch)
usage       - Stops further initialisation of thread and kills main thread
parameters  :
optional    - switch | Default : 1
              If switch is 0 main thread won't be stopped
              To break such a loop use break to stop creating threads

              If switch is 1 main thread will exit leading to end of program

Eamples    :
              Kill child and main thread
                import multithread as mt
                mt.killall()

              Kill child thread
                import multithread as mt
                Some loop:
                    mt.killall(0)
                    break
                // next command
"""

threadlist = []
threadlimit = 10

def setlimit(limit):
    global threadlimit
    threadlimit=limit
    print("--- Limit set -"+str(limit)+"----")

def init(fun, args=[]):
    global threadlist
    if len(threadlist)< threadlimit:
        threadlist.append(threading.Thread(target = fun,args = args))
        threadlist[-1].start()
    else:
        while(True):
            dn=0
            for _ in range(len(threadlist)):
                if not threadlist[_].isAlive():
                    threadlist[_] = threading.Thread(target = fun,args =args)
                    threadlist[_].start()
                    dn=1
                    break
            if dn==1:
                break
    return

def checkfinished():
    while(True):
        dd=0
        for _ in threadlist:
            if _.isAlive():
                dd=1
                time.sleep(1)
                break
        if dd==0:
            break
    
def killall(switch = 1):
    global threadlist
    while(True):
        dd=0
        time.sleep(1)
        for _ in range(len(threadlist)):
            if threadlist[_].isAlive():
                dd=1
        if dd==0:
            break
    if switch==1:
        print("Thread killed.\nExit...")
        sys.exit()
    else:
        print("If no break is implemented the threads will continue")

def usage(find=""):
    find = find.lower()
    if find =="init" or find=="initialise" or find=="start" or find=="startthread" or find =="initialize":
        print(usagedict["init"])
    elif find =="killall" or find =="stop"  or find =="kill" or find=="end":
        print(usagedict["killall"])
    elif find =="check" or find=="finished" or find=="check finished" or find =="checkfinished" or find=="finish":
        print(usagedict["ckeck"])
    elif find=="threadlimit" or find=="limit" or find=="setlimit" or find =="set limit":
        print(usagedict["limit"])
    else:
        for _ in usagedict:
            print(usagedict[_])
    print("")
