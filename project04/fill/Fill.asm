// key=1
@key
M=0

// color=0
@color
M=0

// ncol=32
@32
D=A
@ncol
M=D

(LOOP)
@key
D=M

// if (key-RAM[KBD]==0) goto LOOP
@KBD
D=D-M // D=key-RAM[KBD]
@LOOP
D;JEQ

// key=RAM[KBD]
@KBD
D=M
@key
M=D

// choose black or white (BWEND)
  // if (key==0) goto WHITE 
  @key
  D=M
  @WHITE
  D;JEQ

  // if (key!=0) color=-1
  @color
  M=-1
  @BWEND
  0;JMP

  (WHITE) // color=0
  @color
  M=0
(BWEND) 

// rowc=0
@0
D=A
@rowc
M=D

// rowpixel
@0
D=A
@rowpixel
M=D

(LOOP1)
// if (rowc==256) goto STOP1
@256
D=A
@rowc
D=D-M // rowc-256
@STOP1
D;JEQ

  // colc=0
  @0
  D=A
  @colc
  M=D

  (LOOP2)
  // if (colc-32==0) goto STOP2
  @32
  D=A
  @colc
  D=M-D
  @STOP2
  D;JEQ

  // loc=SCREEN+rowpixel+colc
  @SCREEN
  D=A
  @rowpixel
  D=D+M
  @colc
  D=D+M
  @loc
  M=D

  // RAM[SCREEN]=color
  @color
  D=M
  @loc
  A=M
  M=D

  // colc += 1
  @colc
  M=M+1

  @LOOP2
  0;JMP

  (STOP2)

// rowc += 1
@rowc
M=M+1

//rowpixel += 32
@32
D=A
@rowpixel
M=D+M

@LOOP1
0;JMP

(STOP1)

@LOOP
0;JMP