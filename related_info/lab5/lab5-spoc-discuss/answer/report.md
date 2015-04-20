# 完成功能
```
    1. 增加一个用户进程：在init_main函数中增加1个int pid2 = kernel_thread(user_main, NULL, 0);
    2. 把进程的生命周期和调度动态执行过程完整地展现出来：
        从创建后的PROC_UNINIT到唤醒后的PROC_RUNNABLE(实际上应该是READY)；
		显示正在运行(run)的线程信息；
		显示切换前后的线程信息(注意区分next的状态：READY或者PROC_ZOMBIE),根据cr3判断所处在内核态还是用户态，并输出；
		处理do_wait()函数；
		处理do_yield()函数：显示yield进程的信息；
		处理do_exit()函数，显示虚拟地址映射、页表、内存空间的释放，显示子进程退出唤醒父进程；
		处理do_kill()函数，显示kill掉的进程的id；
		释放线程的资源，对应线程彻底消亡(Dead)。
```

# 具体实现
```
	1. 增加一个用户进程。
		在init_main函数中增加1个int pid2 = kernel_thread(user_main, NULL, 0);
	2. 把进程的生命周期和调度动态执行过程完整地展现出来：
		为了分辨出自己新增的的输出，对自己的输出信息增加了分辨信息：输出的语句以"qw"为开头。
		2.1 从创建后的PROC_UNINIT到唤醒后的PROC_RUNNABLE(实际上应该是READY)：
			在wakeup_proc()函数中输出wakeup前后的进程的id与状态。
		2.2 显示正在运行(run)的线程信息：
			在proc_run()中输出正在运行的进程id与状态。
		2.3 显示切换前后的线程信息(注意区分next的状态：READY或者PROC_ZOMBIE)：
			在proc_run()中的switch_to()前后输出当前进程的信息、下一个进程(通过链表)的信息。
			下一个进程的状态可能为PROC_ZOMBIE或者PROC_RUNNABLE(实际上应该是READY)。
			根据cr3判断所处在内核态还是用户态，并输出。
		2.4 处理do_wait()函数：
			输出child的状态为PROC_ZOMBIE时的信息；
			输出转为PROC_SLEEPING的进程的转换前后信息。
		2.5 处理do_yield()函数：
			显示yield进程的信息；
		2.6 处理do_exit()函数：
			显示虚拟地址映射、页表、内存空间的释放；
			显示子进程退出唤醒父进程；
		2.7 处理do_kill()函数：
			显示kill掉的进程的id。
		2.8 释放线程的资源，对应线程彻底消亡(Dead)：
			在do_wait()函数中，用remove_links将消亡的进程移除链表并进行释放资源时，输出对应的DEAD状态。
```

# 输出结果
从结果中看到有各种状态、进程切换、(内核态和用户态)堆栈切换、do_wait()、     
do_yield()、do_exit()、do_kill()、释放虚拟地址映射、页表、内存空间的输出。
```
use SLOB allocator
check_slab() success
kmalloc_init() succeeded!
check_vma_struct() succeeded!
page fault at 0x00000100: K/W [no page found].
check_pgfault() succeeded!
check_vmm() succeeded.
qw3 before wake up: id: 1 ; state: PROC_UNINIT
qw4 after wake up: id: 1 ; state: PROC_RUNNABLE
ide 0:      10000(sectors), 'QEMU HARDDISK'.
ide 1:     262144(sectors), 'QEMU HARDDISK'.
SWAP: manager = fifo swap manager
BEGIN check_swap: count 31830, total 31830
setup Page Table for vaddr 0X1000, so alloc a page
setup Page Table vaddr 0~4MB OVER!
set up init env for check_swap begin!
page fault at 0x00001000: K/W [no page found].
page fault at 0x00002000: K/W [no page found].
page fault at 0x00003000: K/W [no page found].
page fault at 0x00004000: K/W [no page found].
set up init env for check_swap over!
write Virt Page c in fifo_check_swap
write Virt Page a in fifo_check_swap
write Virt Page d in fifo_check_swap
write Virt Page b in fifo_check_swap
write Virt Page e in fifo_check_swap
page fault at 0x00005000: K/W [no page found].
swap_out: i 0, store page in vaddr 0x1000 to disk swap entry 2
write Virt Page b in fifo_check_swap
write Virt Page a in fifo_check_swap
page fault at 0x00001000: K/W [no page found].
do pgfault: ptep c03a8004, pte 200
swap_out: i 0, store page in vaddr 0x2000 to disk swap entry 3
swap_in: load disk swap entry 2 with swap_page in vadr 0x1000
write Virt Page b in fifo_check_swap
page fault at 0x00002000: K/W [no page found].
do pgfault: ptep c03a8008, pte 300
swap_out: i 0, store page in vaddr 0x3000 to disk swap entry 4
swap_in: load disk swap entry 3 with swap_page in vadr 0x2000
write Virt Page c in fifo_check_swap
page fault at 0x00003000: K/W [no page found].
do pgfault: ptep c03a800c, pte 400
swap_out: i 0, store page in vaddr 0x4000 to disk swap entry 5
swap_in: load disk swap entry 4 with swap_page in vadr 0x3000
write Virt Page d in fifo_check_swap
page fault at 0x00004000: K/W [no page found].
do pgfault: ptep c03a8010, pte 500
swap_out: i 0, store page in vaddr 0x5000 to disk swap entry 6
swap_in: load disk swap entry 5 with swap_page in vadr 0x4000
count is 5, total is 5
check_swap() succeeded!
++ setup timer interrupts
qw... run id:1 state:PROC_RUNNABLE
qw1... before switch:prev: 0 state PROC_RUNNABLE
qw1... before switch:next: 1 state PROC_RUNNABLE (actrual: READY)
qw... create user process original
qw3 before wake up: id: 2 ; state: PROC_UNINIT
qw4 after wake up: id: 2 ; state: PROC_RUNNABLE
qw... create user process A
qw3 before wake up: id: 3 ; state: PROC_UNINIT
qw4 after wake up: id: 3 ; state: PROC_RUNNABLE
qw...before sleep: id 1 state PROC_SLEEPING
qw... run id:3 state:PROC_RUNNABLE
qw1... before switch:prev: 1 state PROC_SLEEPING
qw1... before switch:next: 3 state PROC_RUNNABLE (actrual: READY)
kernel_execve: pid = 3, name = "exit".
I am the parent. Forking the child...
qw3 before wake up: id: 4 ; state: PROC_UNINIT
qw4 after wake up: id: 4 ; state: PROC_RUNNABLE
I am parent, fork a child pid 4
I am the parent, waiting now..
qw...before sleep: id 3 state PROC_SLEEPING
qw... run id:2 state:PROC_RUNNABLE
qw1... before switch:prev: 3 state PROC_SLEEPING
qw1... before switch:next: 2 state PROC_RUNNABLE (actrual: READY)
kernel_execve: pid = 2, name = "exit".
I am the parent. Forking the child...
qw3 before wake up: id: 5 ; state: PROC_UNINIT
qw4 after wake up: id: 5 ; state: PROC_RUNNABLE
I am parent, fork a child pid 5
I am the parent, waiting now..
qw...before sleep: id 2 state PROC_SLEEPING
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 2 state PROC_SLEEPING
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
I am the child.
qw... process 5 do_yield
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_RUNNABLE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
I am the child.
qw... process 4 do_yield
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_RUNNABLE
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 5 state PROC_RUNNABLE
qw2... after switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 5 kernel ? 0
qw7... after switch process 4 kernel ? 0
qw... process 5 do_yield
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_RUNNABLE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 4 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 4 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw... process 4 do_yield
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_RUNNABLE
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 5 state PROC_RUNNABLE
qw2... after switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 5 kernel ? 0
qw7... after switch process 4 kernel ? 0
qw... process 5 do_yield
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_RUNNABLE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 4 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 4 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw... process 4 do_yield
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_RUNNABLE
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 5 state PROC_RUNNABLE
qw2... after switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 5 kernel ? 0
qw7... after switch process 4 kernel ? 0
qw... process 5 do_yield
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_RUNNABLE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 4 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 4 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw... process 4 do_yield
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_RUNNABLE
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 5 state PROC_RUNNABLE
qw2... after switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 5 kernel ? 0
qw7... after switch process 4 kernel ? 0
qw... process 5 do_yield
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_RUNNABLE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 4 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 4 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw... process 4 do_yield
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_RUNNABLE
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 5 state PROC_RUNNABLE
qw2... after switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 5 kernel ? 0
qw7... after switch process 4 kernel ? 0
qw... process 5 do_yield
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_RUNNABLE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 4 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 4 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw... process 4 do_yield
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_RUNNABLE
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 5 state PROC_RUNNABLE
qw2... after switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 5 kernel ? 0
qw7... after switch process 4 kernel ? 0
qw... process 5 do_yield
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_RUNNABLE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 4 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 4 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw... process 4 do_yield
qw... run id:5 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_RUNNABLE
qw1... before switch:next: 5 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 5 state PROC_RUNNABLE
qw2... after switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 5 kernel ? 0
qw7... after switch process 4 kernel ? 0
qw... before do_exit: proc pid 5 will exit, state is PROC_RUNNABLE
qw8... proc 5 exit_mmap
qw8... proc 5 put_pgdir
qw8... proc 5 mm_destroy
qw... change to parent: pid 2 state PROC_SLEEPING
qw3 before wake up: id: 2 ; state: PROC_SLEEPING
qw4 after wake up: id: 2 ; state: PROC_RUNNABLE
qw... run id:4 state:PROC_RUNNABLE
qw1... before switch:prev: 5 state PROC_ZOMBIE
qw1... before switch:next: 4 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 4 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_ZOMBIE (actrual: PROC_ZOMBIE)
qw7... before switch process 4 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw... before do_exit: proc pid 4 will exit, state is PROC_RUNNABLE
qw8... proc 4 exit_mmap
qw8... proc 4 put_pgdir
qw8... proc 4 mm_destroy
qw... change to parent: pid 3 state PROC_SLEEPING
qw3 before wake up: id: 3 ; state: PROC_SLEEPING
qw4 after wake up: id: 3 ; state: PROC_RUNNABLE
qw... run id:3 state:PROC_RUNNABLE
qw1... before switch:prev: 4 state PROC_ZOMBIE
qw1... before switch:next: 3 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 3 state PROC_RUNNABLE
qw2... after switch:next: 2 state PROC_RUNNABLE (actrual: READY)
qw7... before switch process 3 kernel ? 0
qw7... after switch process 2 kernel ? 1
qw...child zombie: id 4 state PROC_ZOMBIE
qw5...remove_links indicate thread dead, id: 4, state: Dead
waitpid 4 ok.
exit pass.
qw... before do_exit: proc pid 3 will exit, state is PROC_RUNNABLE
qw8... proc 3 exit_mmap
qw8... proc 3 put_pgdir
qw8... proc 3 mm_destroy
qw... change to parent: pid 1 state PROC_SLEEPING
qw3 before wake up: id: 1 ; state: PROC_SLEEPING
qw4 after wake up: id: 1 ; state: PROC_RUNNABLE
qw... run id:2 state:PROC_RUNNABLE
qw1... before switch:prev: 3 state PROC_ZOMBIE
qw1... before switch:next: 2 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 2 state PROC_RUNNABLE
qw2... after switch:next: 5 state PROC_ZOMBIE (actrual: PROC_ZOMBIE)
qw7... before switch process 2 kernel ? 0
qw7... after switch process 5 kernel ? 0
qw...child zombie: id 5 state PROC_ZOMBIE
qw5...remove_links indicate thread dead, id: 5, state: Dead
waitpid 5 ok.
exit pass.
qw... before do_exit: proc pid 2 will exit, state is PROC_RUNNABLE
qw8... proc 2 exit_mmap
qw8... proc 2 put_pgdir
qw8... proc 2 mm_destroy
qw... run id:1 state:PROC_RUNNABLE
qw1... before switch:prev: 2 state PROC_ZOMBIE
qw1... before switch:next: 1 state PROC_RUNNABLE (actrual: READY)
qw2... after switch:prev: 1 state PROC_RUNNABLE
qw2... after switch:next: 3 state PROC_ZOMBIE (actrual: PROC_ZOMBIE)
qw7... before switch process 1 kernel ? 1
qw7... after switch process 3 kernel ? 1
qw5...remove_links indicate thread dead, id: 3, state: Dead
qw5...remove_links indicate thread dead, id: 2, state: Dead
all user-mode processes have quit.
init check memory pass.
kernel panic at kern/process/proc.c:491:
    initproc exit.
```
