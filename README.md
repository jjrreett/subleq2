# Subleq to the moon

## What is Subleq
Subleq is a One-Instruction Set Computer Architecture. OISC
Refer to [A Simple Multi-Processor Computer Based on Subleq by Oleg Mazonka and Alex Koldin](https://arxiv.org/pdf/1106.2593.pdf) for reference. This project is based heavily off their work. 

## What is my goal
The ultimate stated goal of this project is to build a physical computer using TTL (74 series) chips. Then using that computer land a simulated spacecraft on an celestial body. This project was inspired by a long time fascination with building a computer from scratch, the apollo guidance computer, in particular this talk by [Robert Wills](https://www.youtube.com/watch?v=B1J2RMorJXM) and the CuriousMarc AGC project ([see this video](https://www.youtube.com/watch?v=r_eBGSe5zEQ&t))

## How
### Physical computer (Hardware In the Loop/HIL)
#### First lets simulate it 
To make the physical computer, I have architected a subleq computer on paper and tested on [hneemann's Digital project](https://github.com/hneemann/Digital). Those files can be found under the simulator/ dir. 

Note to self. `java -jar /Downloads/Digital/Digital.jar` to run Digital. 

Currently the file simulator/mem is where Digital pull the data from to load into ram. RAM chips are usually volatile, so either the computer will need to bootstrap itself on reboot or I will need to find a non-volatile solution to RAM. 
- [ ] Solve Bootstrap problem 

Currently I am using Digital's logical blocks. However, Digital has many of the 74xx chips preloaded. So I can use Digital to as a schematic to the circuit I will need to build. 
- [ ] Rebuild simulator using 74xx chips

Other TODOs:
- [ ] refactor architecture to have little endian address byte order
- [ ] figure out how to increment double address and performance implications 
- [ ] think about IO ports and how I want to interact with them

#### Build it 
TODO 

### Flight Simulator
I was thinking it would be cool to hook this up to KSP. That would be cool because it get me a GUI, but comes with a bit of overhead? It might not be as hard as I think, but I am causous. 
I could build a sim with matlab/simulink/simscape. But that is decidedly closed source. 
I could do it in a game engine, but I don't want to learn one unless its easy. 
I could write a simulator manually, but I want a GUI and I want to actually finish this project 

### Code
I have to build a RTOS that can compile to a custom architecture. I have chosen to write my owen assembly language.
compiler/contains the start to that. 
This is a python module that can tokenize the input stream, ./program.subleq for now. Then parse that token stack into an ast. Then render the ast to machine code. 
Then I either write the os in the assembly language (adding some higher level features along the way), or build a language on top of the assembly. 
Ahhhhh lots of work. 
