# lab8 report 计22班 覃伟 2012011278

## 练习1 完成读文件操作的实现
```
1. 如果读取的开始位置并不是对其某个block的开始处，那么先读取该block的数据：
	1.1 设置该block需要读取的内容的大小size=(nblks!=0)?(SFS_BLKSIZE-blkoff):(endpos-offset);
	1.2 通过sfs_bmap_load_nolock函数得到实际的磁盘编号，操作失败跳到out部分；
	1.3 通过sfs_buf_op进行实际的读操作，操作失败跳到out部分；
	1.4 更新已经读取长度alen+=size;
	1.5 如果nblks=0表示读取完了，跳到out部分；
	1.6 更新存放数据位置buf+=size;读取开始块blkno++;剩余读取块数nblks--。
2. 读取中间首尾对齐的块：
	2.1 设置读取的内容的大小size=SFS_BLKSIZE;
	2.2 通过sfs_bmap_load_nolock函数得到实际的磁盘编号，操作失败跳到out部分；
	2.3 通过sfs_buf_op进行实际的读操作，操作失败跳到out部分;
	2.4 更新已经读取长度alen+=size、存放数据位置buf+=size、
          读取开始块blkno++、剩余读取块数nblks--。
3. 如果结束地址并不是块结束的整数倍，表示不对其，有剩余部分需要读取：
	3.1 得到剩余读取部分的长度size = endpos % SFS_BLKSIZE;
	3.2 通过sfs_bmap_load_nolock函数得到实际的磁盘编号，操作失败跳到out部分；
	3.3 通过sfs_buf_op进行实际的读操作，操作失败跳到out部分;
	3.4 更新已经读取长度alen+=size
```

### 问答题 给出设计实现”UNIX的PIPE机制“的概要设方案，鼓励给出详细设计方案。
```
使用系统调用来实现管道的初始化与读写等操作，用创建文件的方式来管理一个数据缓冲区，
维护头指针(用于读文件)与尾指针(用于写文件)，头指针=尾指针表明没有写入的数据。
用信号量或者管程来实现文件的读写，保证同一个时间只有有一个进程在写文件。
```

## 练习2 完成基于文件系统的执行程序机制的实现
```
1. 为进程创建一个新的内存区域(同lab7)
2. 创建新的页表(同lab7)
3. 复制内容、数据、BSS：
	3.1 通过文件头部读取(同lab7)
    3.2 通过程序头部读取
	3.3 通过mm_map函数去创建代码段与数据段的vma
    3.4 通过callpgdir_alloc_page函数去分配代码段、数据段的页，并复制文件的内容
    3.5 通过callpgdir_alloc_page函数去分配BSS，并将非配的页置零
4. 通过mm_map函数创建用户栈
5. 设置好进程的内存空间、CR3、页表项
6. 根据argc与argv给用户栈设置参数
7. 设置用户栈的中断帧trapframe
```

### 问答题
给出设计实现基于”UNIX的硬链接和软链接机制“的概要设方案，鼓励给出详细设计方案
```
     硬链接指文件与索引结点inode直接相连，在创建硬链接时，把新创建的文件的inode
指向目标路径对应的inode，并将该inode的引用次数加1；在删除的时候，将对应inode的
引用次数减1，当且仅当inode的引用次数降为0时，才真正删除并回收inode和原文件。
     软链接又叫符号链接，是包含了另一个文件的路径名的文件，其实质是指向另一个文件
的间接指针，不受文件系统限制。创建软链接时，先创建一个新文件及其对应的inode，
文件中存储目标路径，inode指定为链接类型。在删除时直接删除该链接文件及其对应的
inode即可，不会影响到目标文件。
```

## 程序运行结果
用make qemu后输入ls hello等命令，成功执行，输出如下：
```
ls
 @ is  [directory] 2(hlinks) 23(blocks) 5888(bytes) : @'.'
   [d]   2(h)       23(b)     5888(s)   .
   [d]   2(h)       23(b)     5888(s)   ..
   [-]   1(h)       10(b)    40383(s)   softint
   [-]   1(h)       11(b)    44571(s)   priority
   [-]   1(h)       11(b)    44584(s)   matrix
   [-]   1(h)       10(b)    40391(s)   faultreadkernel
   [-]   1(h)       10(b)    40381(s)   hello
   [-]   1(h)       10(b)    40382(s)   badarg
   [-]   1(h)       10(b)    40404(s)   sleep
   [-]   1(h)       11(b)    44694(s)   sh
   [-]   1(h)       10(b)    40380(s)   spin
   [-]   1(h)       11(b)    44640(s)   ls
   [-]   1(h)       10(b)    40386(s)   badsegment
   [-]   1(h)       10(b)    40435(s)   forktree
   [-]   1(h)       10(b)    40410(s)   forktest
   [-]   1(h)       10(b)    40516(s)   waitkill
   [-]   1(h)       10(b)    40404(s)   divzero
   [-]   1(h)       10(b)    40381(s)   pgdir
   [-]   1(h)       10(b)    40385(s)   sleepkill
   [-]   1(h)       10(b)    40408(s)   testbss
   [-]   1(h)       10(b)    40381(s)   yield
   [-]   1(h)       10(b)    40406(s)   exit
   [-]   1(h)       10(b)    40385(s)   faultread
lsdir: step 4
$ hello
Hello world!!.
I am process 14.
hello pass.
```
使用make qemu 与 bash tools/grade.sh 命令后，输出如下：
```
badsegment:              (3.6s)
  -check result:                             OK
  -check output:                             OK
divzero:                 (2.9s)
  -check result:                             OK
  -check output:                             OK
softint:                 (3.2s)
  -check result:                             OK
  -check output:                             OK
faultread:               (1.5s)
  -check result:                             OK
  -check output:                             OK
faultreadkernel:         (1.7s)
  -check result:                             OK
  -check output:                             OK
hello:                   (3.5s)
  -check result:                             OK
  -check output:                             OK
testbss:                 (1.5s)
  -check result:                             OK
  -check output:                             OK
pgdir:                   (2.9s)
  -check result:                             OK
  -check output:                             OK
yield:                   (3.1s)
  -check result:                             OK
  -check output:                             OK
badarg:                  (3.0s)
  -check result:                             OK
  -check output:                             OK
exit:                    (3.3s)
  -check result:                             OK
  -check output:                             OK
spin:                    (3.2s)
  -check result:                             OK
  -check output:                             OK
waitkill:                (3.6s)
  -check result:                             OK
  -check output:                             OK
forktest:                (3.2s)
  -check result:                             OK
  -check output:                             OK
forktree:                (2.7s)
  -check result:                             OK
  -check output:                             OK
priority:                (15.6s)
  -check result:                             OK
  -check output:                             OK
sleep:                   (11.7s)
  -check result:                             OK
  -check output:                             OK
sleepkill:               (3.4s)
  -check result:                             OK
  -check output:                             OK
matrix:                  (12.7s)
  -check result:                             OK
  -check output:                             OK
Total Score: 190/190
```
可见，实验正确。

## 列出你认为本实验中重要的知识点，以及与对应的OS原理中的知识点。
```
1. 文件系统
2. 文件
3. 文件描述符
4. 目录
5. 文件别名
6. 文件种类
7. 虚拟文件系统
8. 简单文件系统
9. 文件缓存
10. 打开文件
```

## 列出你认为OS原理中重要的知识点，但在实验中没有对应上
```
1. 文件分配等
2. 冗余磁盘阵列
3. 空间空闲管理
```

