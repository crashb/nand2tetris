// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
    @0
    M=0
(LISTEN)
    @24576
    D=M
    @KEYUP
    D;JEQ
    @KEYDOWN
    0;JMP
(KEYUP)
    @0
    D=M
    @LISTEN
    D;JEQ
    @0
    M=0
    @FILL
    0;JMP
(KEYDOWN)
    @0
    D=M
    @LISTEN
    D;JNE
    @0
    M=!M
    @FILL
    0;JMP
(FILL)
    @16383
    D=A
    @1
    M=D
(FILLLOOP)
    @1
    D=M
    @24576
    D=D-A
    @LISTEN
    D;JGE
    @0
    D=M
    @1
    M=M+1
    @0
    D=M
    @1
    A=M
    M=D
    @FILLLOOP
    0;JMP
