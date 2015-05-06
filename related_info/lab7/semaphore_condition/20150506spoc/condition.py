#coding=utf-8
#!/usr/bin/env python
  
import threading  
import time

flag = [5, 1, 1, 1, 1, 1]
queue = list()
condition = threading.Condition()
mutex_flag = threading.Semaphore(1)
mutex_queue = threading.Semaphore(1)
mywait = 0

class MyThread(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)

    def run(self):
        global flag, qwn, queue, mutex_flag, mutex_queue, mywait
        while True:
            qwflag = 0
            if condition.acquire():
                if flag[0] > 0:
                    flag[0] -= 1
                    for i in range(1, 6):
                        if flag[i] == 1:
                            flag[i] = 0
                            temp = i
                            print 'pid %s use printer %3d\n' % (self.name, temp)
                            qwflag = 1
                            break
                else:
                    condition.release()
            if qwflag == 1:
                break
        condition.release()
        time.sleep(1)
        print 'pid %s sleep over\n' % (self.name)
        while True:
            qwflag = 0
            if condition.acquire():
                qwflag = 1
                print 'pid %s return printer %3d\n' % (self.name, temp)
                flag[0] += 1
                flag[temp] = 1
                condition.release()
            if qwflag == 1:
                break
        
if __name__ == "__main__":  
    for i in range(0, 10):  
        my_thread = MyThread()  
        my_thread.start()
    print 'end\n'
