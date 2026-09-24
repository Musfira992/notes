---
title: "Hello Julia"
date: 2025-11-18
source: https://www.musfirajamil.com/blog/hello-julia
---

# Hello Julia

_A quick tour of the Julia programming language, its performance story, its scientific-computing ecosystem, and how to get started with Pluto notebooks._

Experts are saying Julia "looks like Python, feels like Lisp, runs like Fortran." That made me curious, so I decided to explore more. Here is a summary of what I found.

Julia is a general-purpose, interpreted language developed by a group at MIT, with numerical computing at the core of its design. It was first released in 2012 and slowly matured to a point where version 1.0 was launched in 2018 (currently at v1.7). At its core, Julia is a high-level, dynamic programming language that offers performance approaching that of statically-typed languages like C++, and is increasingly being used by a huge number of universities and tech companies.

* **Performance**: Julia, just like Python, is a dynamic language with optional types. In Python types can change at run-time, costing an overhead as compared to C, which is statically typed. However, Julia uses multiple dispatch, which makes defining types optional, so defining types doesn't lead to that performance boost.

Some bragging rights highlighted by MIT at the v1.0 launch:

> Julia is the only high-level dynamic programming language in the "petaflop club," having achieved 1.5 petaflop/s using 1.3 million threads, 650,000 cores and 9,300 Knights Landing (KNL) nodes to catalogue 188 million stars, galaxies, and other astronomical objects in 14.6 minutes on the world's sixth-most powerful supercomputer.

> "The release of Julia 1.0 signals that Julia is now ready to change the technical world by combining the high-level productivity and ease of use of Python and R with the lightning-fast speed of C++," Edelman says.

**Rich data science and visualisation libraries:** From a data science perspective, anyone who is already pushing the boundaries of Python and is interested in high-performance numerical computing should definitely give Julia a try. Developing high-performance libraries focusing on scientific computing and numerical computation has been prioritised since day one. This means Julia solves the "two language problem," letting you quickly convert prototypes into high-performance implementations without the extra overhead of shifting between two different languages. It is quite similar to Python syntactically, plus you can use all your existing Python libraries in it. You can also call C and Fortran libraries natively.

**Try Julia for data science:** How to get started? MIT has made available a free online course called Introduction to Computational Thinking to help you get started with fundamental concepts of programming with Julia. In addition, the official YouTube channel of Julia is a treasure trove of discussions on advanced topics such as dynamic type systems, parametric polymorphism/multiple dispatch, Lisp-like macros, distributed computing, garbage collection, and libraries for floating point calculations.

I would also recommend installing Pluto, an interactive-computing environment (reactive notebook) for Julia with intelligent syntax analysis. It also comes with an important guarantee: "At any instant, the program state is completely described by the code you see." That makes it more promising than using Jupyter notebooks or MATLAB. Lastly, this cheatsheet will come in handy: [github.com/mitmath/julia-mit](https://github.com/mitmath/julia-mit/blob/master/Julia-cheatsheet.pdf)
