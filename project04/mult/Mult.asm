@total
M=0
(LOOP)
@R0
D=M
@STOP
D;JEQ

@R1
D=M
@total
M=D+M
@R0
M=M-1
@LOOP
0;JMP

(STOP)
@total
D=M
@R2
M=D

(END)
@END
0;JMP