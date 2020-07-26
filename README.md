# README #

This is my work from *The Elements of Computing Systems: Building a Modern Computer from First Principles* by Nisan and Shocken.

The software suite required to test or use any of these files is available for download from the [official website](https://www.nand2tetris.org/). There are also lectures available online, but I didn't use them as I felt that the textbook explained everything well enough and better suited my learning style.

### Basic premise

The basic premise of the book is best explained in the Preface:

> We wrote this book because we felt that many computer science students are missing the forest for the trees. The typical student is marshaled through a series of courses 
> in programming theory, and engineering, without pausing to appreciate the beauty of the picture at large. And the picture at large is such that hardware and software systems 
> are tightly interrelated through a hidden web of abstractions, interfaces, and contract-based implementations. Failure to see this intricate enterprise in the flesh leaves 
> many studetns and professionals with an uneasy feeling that, well, they don't fully understand what's going on inside computers.
    
> We believe that the best way to understand how computers work is to build one from scratch. With that in mind, we came up with the following concept. Let's specify a simple 
> but sufficiently powerful computer system, and have the students build its hardware platform and the software hierarchy from the ground up, starting with nothing more than 
> elementary logic gates. And while we are at it, let's do it right We say this because building a general-purpose computer from first principles is a huge undertaking. 
> Therefore, we identified a unique educational opportunity not only to build the thing, but also to illustrate, in a hands-on fashion, how to effectively plan and manage 
> large-scale hardware and software development projects. In addition, we sought to demonstrate the ability to construct, through recursive ascent and human reasoning, 
> fantastically complex and useful systems from nothing more than a few primitive building blocks.

### Overview of work

The folders in this repo reflect the chapters of the book. Broadly, these are ordered as follows:

1. Building boolean logic chips: not, and, or, xor and mux (with some permutations in 1 bit, 8 bit and 16 bit). A nand chip is given as the atomic part from which all other chips can be built. All chip "construction" is done using a hardware description language which is simulated using the supplied software.
2. Building boolean arithmetic chips (increments and adders) and the arithmetic logic unit (ALU).
3. Building sequential logic chips and memory chips (registers, program counter, and RAM ranging from 8-bit to 16k).
4. Learning the Hack assembly language, which our virtual computer will use later.
5. Use the chips constructed in chapters 1-3 to construct the virtual "Hack" computer. This is a complete, if simple, 16-bit von Neumann computer comprised of 32k ROM (instruction memory), 24k usable RAM (including memory maps), and CPU. Keyboard input and screen output is handled via memory mapping.
6. Write an assembler to convert the Hack assembly language into bytecode suitable for the Hack computer.
7. Write a stack-based virtual machine, which compiles down into the Hack assembly language. This is split into 2 chapters, starting with arithmetic commands and memory access commands.
8. Write the rest of the virtual machine, specifically the program flow commands (branching) and function calling commands (calling functions and returning from them).
9. An introduction to the "Jack" language, which is a high-level general purpose object oriented programming language. Jack roughly imitates Java and C#.
10. Write the first part of a compiler for the Jack language, namely a tokenizer and parser which consumes a file and produces and XML output that correctly identifies the different types of tokens used in the source file (e.g. keywords, symbols, identifiers, constants)
11. Write the rest of the compiler for the Jack language, replacing the XML output with a code writer module that produces actual VM code, and adding a symbol table.
12. Write the operating system, which is a series of Jack classes that handle common tasks, extend the language, and interface with hardware. (The book acknowledges that it uses the term "operating system" loosely.) This includes:
    - Array and String classes
    - Math functions
    - Keyboard input
    - Printing text to screen
    - Drawing to screen
    - Memory management (particularly dynamic memory allocation and deallocation, noting that Jack leaves some "trapdoors" down into lower level functionality)

### Notes

This was all a learning exercise - *it is not optimised code*. The goal was to learn how computers and programming languages work (and improve my general programming skills) - not to get a perfectly working implementation. In other words, it was a pedagogical tool first and foremost. There is much to improve if I were to review this code, but now that I have completed the textbook once over, I think my time is better spent elsewhere.

The Hack assembler and the VM were implemented in Typescript, because I wanted to learn more about Typescript at that time. I can't particularly recommend that course of action. I switched to Python for the high-level compiler.

Git commits were for myself and no-one else, so they are messy and unstructured, mostly for the purpose of backing up my work from session to session rather than implementing proper version control.

I didn't accomplish this by myself - although the book was pitched at just the right level for me, there were some tasks where I had to furiously Google and search the [Nand2Tetris Questions and Answers Forum](http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/) and StackOverflow. Trying to implement mathematical operations in an efficient way, for example, when you've forgotten how to do long division.

This is being shared:
- To help others that may be working through the book, although I don't promise that my code will always be helpful or advisable
- To help others who are trying to evaluate the book and decide whether it's worth their time
- As a record of my activity

I also wanted to share what I have learned, even if it is retrospectively, per [Learn in Public](https://www.swyx.io/writing/learn-in-public/).

### Interesting things I learned

I should keep better notes as I go. However, here is an unordered list of some of the more interesting things I learned in the book:

- The point where computer science and boolean logic rub up against physical properties of objects (electrical engineering) - to go deeper is to enter the physical world.
- How boolean logic works and how you can execute mathematical operations through bitwise operations.
- How logic gates work and how combining them puts you on a course of rapidly escalating abstractions until you’ve lost sight of where you’ve come from.
- Similarly, how combining abstractions means that once you’ve implemented a particular feature, you quickly forget about its inner workings as you move to a higher level. For example, Jack is only a few steps removed from bytecode. Once you implement the assembler, you forget about the format of the bytecode; once you implement the VM, you forget about the assembly language; and once you implement Jack, you forget about everything else. Of course, you don't forget about it completely - rather, you can compartmentalise it and focus on the appropriate level of abstraction for your task. Knowing how each step of the compilation works still gives you powerful insights into what you're writing.
- However, higher levels of abstraction can also close off certain operations. Once you implement the VM, you can only write the bytecode (and combinations of bytecode) that the VM permits. In this way, higher levels of abstraction may give you more practical power, but also more guardrails on what you can do.
- The power of data structures. Moving from manipulating registers in RAM to a stack based VM makes it clear how powerful an abstract data structure is, rather than being limited by the physical architecture.
- How inefficiencies low in the stack can be magnified at higher levels. For example, a VM command that is expressed inefficiently in assembly may be magnified a thousandfold at higher levels. As I was writing my Jack OS in chapter 12, I was often wincing at how many lines on lines of assembly must be being produced for the simplest of operations. On the other hand, this provides an obvious target for any optimisation efforts.
- How understanding what can be done in a single CPU cycle can inform your choices in higher level programming - you understand the detail of what is a “cheap” and “expensive” operation. For example, you might realise that your division algorithm is more expensive than your multiplication algorithm, and structure your code accordingly (or optimise it).
- Similarly, you gain a more intuitive understanding of what it means for work to be done at the hardware vs. software level, and what implications this has for hardware design.
- How a deeper understanding mathematics allows you to see more efficient methods of carrying out certain operations. For example, the book advises you to implement a square root function `y = sqrt(x)` by expressing it as `y^2 = x` and using binary search to find the solution. This is obviously a pretty simple inversion of the mathematical operation, but the book is filled with clever solutions like this so that you don't end up writing O(n^2) code.
- How “objects” in OOP are pure fiction, created for the benefit of the programmer. It doesn't add any extra functionality from the machine's perspective. Hence one of my favourite quotes from the author:
    > Programs must be written for people to read, and only incidentally for machines to execute.
- Trying to “flatten out” objects into their fields (variables) and methods (functions), and making sure that the right pointers were passed around to methods in Ch 11, was quite challenging.
- How much work the OS/standard libraries do, even when a language is fully written - lots of heavy lifting involved to do maths, write output, draw graphics, etc. It's fairly amusing to have created a fully-formed language by the end of Ch 11 and not actually being able to do anything useful with it.
- The challenge of being able to understand how technology *really* works these days. This was an extremely simplified implementation for conceptual understanding, but real-life designs and implementations are far more complex.
- The authors present a suggested architecture for your solutions in the each chapter of the book, largely by specifying the classes you should write and the API they should adhere to. Merely implementing their suggested structure turned out to be instructive for how object oriented code is structured.

Overall, I really enjoyed this textbook, and would strongly recommend it to anyone who is interested.