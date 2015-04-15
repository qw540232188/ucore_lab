# 完成功能
```
    1. 增加一个内核线程：在proc_init函数中增加1个kernel_thread：init3。
    2. 把进程的生命周期和调度动态执行过程完整地展现出来：
        从创建后的PROC_UNINIT到唤醒后的PROC_RUNNABLE(实际上应该是READY)；
		显示正在运行(run)的线程信息；
		显示切换前后的线程信息(注意区分next的状态：READY或者PROC_ZOMBIE)；
		处理do_wait()函数；
		释放线程的资源，对应线程彻底消亡(Dead)。
	按照链表顺序往下切换，没有调度算法。
	因为没有需要等待子进程的父进程，所以没有WAITING状态。
```

# 具体实现
```
	1. 增加一个内核线程。
		在proc_init函数中增加1个kernel_thread：init3。并相应进行各种初始化工作。
	2. 把进程的生命周期和调度动态执行过程完整地展现出来：
		为了分辨出自己新增的的输出，对自己的输出信息增加了分辨信息：输出的语句以"qw"为开头。
		2.1 从创建后的PROC_UNINIT到唤醒后的PROC_RUNNABLE(实际上应该是READY)：
			在wakeup_proc()函数中输出wakeup前后的进程的id与状态。
		2.2 显示正在运行(run)的线程信息：
			在proc_run()中输出正在运行的进程id与状态。
		2.3 显示切换前后的线程信息(注意区分next的状态：READY或者PROC_ZOMBIE)：
			在proc_run()中的switch_to()前后输出当前进程的信息、下一个进程(通过链表)的信息。
			下一个进程的状态可能为PROC_ZOMBIE或者PROC_RUNNABLE(实际上应该是READY)。
		2.4 处理do_wait()函数：
			输出child的状态为PROC_ZOMBIE时的信息；
			输出转为PROC_SLEEPING的进程的转换前后信息。
		2.5 释放线程的资源，对应线程彻底消亡(Dead)：
			在do_wait()函数中，用remove_links将消亡的进程移除链表并进行释放资源时，输出对应的DEAD状态。
	按照链表顺序往下切换，没有调度算法。
	因为没有需要等待子进程的父进程，所以没有WAITING状态。
```

# 输出结果
从结果中看到有各种状态、进程切换、do_wait()、do_exit()的输出。
```
use SLOB allocator
kmalloc_init() succeeded!
qw3 before wake up: id: 1 ; state: PROC_UNINIT
qw4 after wake up: id: 1 ; state: PROC_RUNNABLE
qw3 before wake up: id: 2 ; state: PROC_UNINIT
qw4 after wake up: id: 2 ; state: PROC_RUNNABLE
qw3 before wake up: id: 3 ; state: PROC_UNINIT
qw4 after wake up: id: 3 ; state: PROC_RUNNABLE
proc_init:: Created kernel thread init_main--> pid: 1, name: init1
proc_init:: Created kernel thread init_main--> pid: 2, name: init2
proc_init:: Created kernel thread init_main--> pid: 3, name: init3
++ setup timer interrupts
qw... run id:1 state:PROC_RUNNABLE
qw1... before switch:prev: 0 state PROC_RUNNABLE
qw1... before switch:next: 1 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 1, name = init1
qw... run id:2 state:PROC_RUNNABLE
qw1... before switch:prev: 1 state PROC_RUNNABLE
qw1... before switch:next: 2 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 2, name = init2
qw... run id:3 state:PROC_RUNNABLE
qw1... before switch:prev: 2 state PROC_RUNNABLE
qw1... before switch:next: 3 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 3, name = init3
qw... run id:1 state:PROC_RUNNABLE
qw1... before switch:prev: 3 state PROC_RUNNABLE
qw1... before switch:next: 1 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 1 state PROC_RUNNABLE
qw2... after switch:next: 2 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 1, name = init1 , arg  init main1: Hello world!! 
qw... run id:2 state:PROC_RUNNABLE
qw1... before switch:prev: 1 state PROC_RUNNABLE
qw1... before switch:next: 2 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 2 state PROC_RUNNABLE
qw2... after switch:next: 3 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 2, name = init2 , arg  init main2: Hello world!! 
qw... run id:3 state:PROC_RUNNABLE
qw1... before switch:prev: 2 state PROC_RUNNABLE
qw1... before switch:next: 3 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 3 state PROC_RUNNABLE
qw2... after switch:next: 1 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 3, name = init3 , arg  qw... init main3: Hello world!! 
qw... run id:1 state:PROC_RUNNABLE
qw1... before switch:prev: 3 state PROC_RUNNABLE
qw1... before switch:next: 1 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 1 state PROC_RUNNABLE
qw2... after switch:next: 2 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 1, name = init1 ,  en.., Bye, Bye. :)
qw... before do_exit: proc pid 1 will exit, state is PROC_RUNNABLE
 do_exit: proc pid 1 will exit
 do_exit: proc  parent c02ff008
qw... run id:2 state:PROC_RUNNABLE
qw1... before switch:prev: 1 state PROC_ZOMBIE
qw1... before switch:next: 2 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 2 state PROC_RUNNABLE
qw2... after switch:next: 3 state PROC_RUNNABLE (actrual: READY)
 kernel_thread, pid = 2, name = init2 ,  en.., Bye, Bye. :)
qw... before do_exit: proc pid 2 will exit, state is PROC_RUNNABLE
 do_exit: proc pid 2 will exit
 do_exit: proc  parent c02ff008
qw... run id:3 state:PROC_RUNNABLE
qw1... before switch:prev: 2 state PROC_ZOMBIE
qw1... before switch:next: 3 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 3 state PROC_RUNNABLE
qw2... after switch:next: 1 state PROC_ZOMBIE (actrual: PROC_ZOMBIE)
 kernel_thread, pid = 3, name = init3 ,  en.., Bye, Bye. :)
qw... before do_exit: proc pid 3 will exit, state is PROC_RUNNABLE
 do_exit: proc pid 3 will exit
 do_exit: proc  parent c02ff008
qw... run id:0 state:PROC_RUNNABLE
qw1... before switch:prev: 3 state PROC_ZOMBIE
qw1... before switch:next: 0 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 0 state PROC_RUNNABLE
qw2... after switch:next: 1 state PROC_ZOMBIE (actrual: PROC_ZOMBIE)
do_wait: begin
qw...child zombie: id 1 state PROC_ZOMBIE
do_wait: has kid find child  pid1
qw5...remove_links indicate thread dead, id: 1, state: Dead
do_wait: begin
qw...child zombie: id 2 state PROC_ZOMBIE
do_wait: has kid find child  pid2
qw5...remove_links indicate thread dead, id: 2, state: Dead
do_wait: begin
qw...child zombie: id 3 state PROC_ZOMBIE
do_wait: has kid find child  pid3
qw5...remove_links indicate thread dead, id: 3, state: Dead
do_wait: begin
100 ticks
```
