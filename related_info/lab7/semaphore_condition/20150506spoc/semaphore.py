#coding=utf-8
#!/usr/bin/env python
  
import threading  
import time

flag = [5, 1, 1, 1, 1, 1]
queue = list()
qwn = threading.Semaphore(5)
mutex_flag = threading.Semaphore(1)
mutex_queue = threading.Semaphore(1)

class MyThread(threading.Thread):  
    def __init__(self):  
        threading.Thread.__init__(self)

    def run(self):
        global flag, qwn, queue, mutex_flag, mutex_queue
        while True:
            if qwn.acquire():
                break
        if mutex_flag.acquire():
            if flag[0] > 0:
                flag[0] -= 1
                for i in range(1, 6):
                    if flag[i] == 1:
                        flag[i] = 0
                        temp = i
                        break
                mutex_flag.release()
                print 'pid %s use printer %3d\n' % (self.name, temp)
        time.sleep(1)
        print 'pid %s sleep over\n' % (self.name)
        if mutex_flag.acquire():
            print 'pid %s return printer %3d\n' % (self.name, temp)
            flag[0] += 1
            flag[temp] = 1
            mutex_flag.release()
        qwn.release()
        
if __name__ == "__main__":  
    for i in range(0, 10):  
        my_thread = MyThread()  
        my_thread.start()  
