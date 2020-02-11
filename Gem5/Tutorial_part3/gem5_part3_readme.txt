Steps to use m5_dump_reset_stats() pseudo instruction in the programs.

1) Include the file m5ops.h from "gem5/include/gem5/m5ops.h" in the program where you want to use that instruction.

2) Update the Makefile.x86 from "gem5/util/m5" as follows:

-CFLAGS=-O2 -DM5OP_ADDR=0xFFFF0000
+CFLAGS=-O2

to get the implementation of m5_dump_reset_stats() function.

3) Create a library using ar command which contains the object file "m5op_x86.o" which is created after the make command:

ar rcs libmylib.a /gem5/util/m5/m5op_x86.o

Note that the library name must start with lib_ _ _.

4) Link this library to the c/cpp program which uses the m5_dump_reset_stats() function:

gcc --static program.c -L. -lmylib -o linked_file
(or)
gcc --static -L. -lmylib -o linked_file program.c

The difference between the two commands is where the libraries appear relative to the source files that use them.

Note that the library name is used as -lmylib here and not -llibmylib.

5) This linked file will not be executed in the actual processor but rather in the gem5 simulator because this is a pseudo instruction.
