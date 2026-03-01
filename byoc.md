# Lab 6: Bring Your Own Code (BYOC)

**Motivation:** This is a free-form lab where you have the opportunity to write, re-write,
improve and optimize your own research codes with guidance from the instructor
and your classmates. Due to the wide variety of resources, where some students
have solid research codes, and others have ideas but not much scaffolding,
I offer a few approaches below, feel free to pick the path that best suits your
current needs.

## Instructions

- This lab focuses on implementing topics that we learned in class in your own code. 
- You will do this either through implementation reflection. 
- Do not submit code you have that already exists, this is an opportunity to create or revise and to 
practice implementing. Take this as an opportunity to try the thing that you didn't think you'd use.

## Tasks

### Task 1: Implement **all** of the following in your code 

1. **PEP-8 Formatting**: Intuitive variable names, descriptive comments, elaboration where necessary, 
appropriate case (camel vs. snake), syntax, line limits. Remember these are *guidelines*, not rules, **consistency** is the most
important thing.
2. **Version Control (Local and Remote):** Commit small and often. Don't do 3 hours of work and then commit
one big change that says *"my code"*. This forces you to work on one definable piece at a time. Get into the habit of 
committing changes before moving onto the next piece.
3. **Functions**: Think about the acronym DRY (*Don't Repeat Yourself*). Keep an eye out for: repeated code blocks, pieces of code that would benefit from isolation and organization, long winded runs of code; functions fall out naturally.
4. **Documentation**: At a minimum, a doc-string at the top of your code explaining what the code does,
its inputs and outputs, and how to use the code. If you need more tools for explanation, like tables, figures, then consider a README file.
5. **Accessibility**: Anyone in our class should be able to look at your code and (without consulting with you) be able to understand what it does, download/install it, run an example, and evaluate whether or not it is "working". This may require having an example script, or example data, associated with the code .

### Task 2: Implement *at least* 1 of the following in your code 

For the other(s), reflect, on how you would implement it with words and pseudo code. Or, why you did not/would not implement.

> Note: "Not enough time", "too difficult" are not good reflections. Think about whether this would actually be useful in your research code. If you don't know whether it will be, take that as a challenge to try. If you think it will be, then reflect on how you might implement it using words and pseudocode.

6. **Classes**: Remember, classes bundle data and functions. If you find yourself continually operating, accessing and modifying a set of data, or passing the same collection of input parameters between functions, then a class may be a useful abstraction.
7. **Parallel/Concurrency**: If you notice your problem is parallelizable, or embarassingly parallel, try to structure your code so that it can be parallelized. This does not have to use a complex package like `concurrent.futures`, the bash, Python, or multiple-terminal approach are all valid, but require structuring your code in such a way that you can exploit these features.

### Task 3: Implement *at least* 1 of the following in your code 

For the other(s), reflect, on how you would implement it with words and pseudo code. Or, why you did not/would not implement.

8. **Parameter Input System**: Most of our code can benefit from quick modifications from the user. Implement a parameter input system that allows for this, using any of the following (no `sys.arg`!): 
    - parameter files
    - argparser
    - input()
    > Note: This ties into (5) above, a random user needs to understand how they call your code and what each of the 
    parameters is, and whether their order, case, type is important. 
9. **Testing**: This can be as simple as test functions which ensure functions, code blocks, parameters, outputs, etc. behave as expected. This can also be `assert` statements throughout your code that check behavior and keep things on the rails. The most advanced application of this would be to use a dedicated testing package like `Pytest`. 
10. **Branching Development**: Use a branch to develop a feature and then merge it back into your main branch. This is especially useful if you have a code that works and you don't want to break existing functionality. Think of this as the version control  approach of creating a copy of your file.


## Options

Please choose **one** of the three options and following the Tasks and Instructions above. If you think of a 
mysterious fourth option, feel free to run it by me.

### Option 1: Modify Existing Code

Take your existing research code and improve it. Re-organizing the structure with
functions and classes, changing the syntax, writing for generalizability, 
improving for speed. 

Be sure to commit your code before you start making changes and provide me a link
to the commit where you started making your changes. Consider branch development
and committing small and often to ensure you can get back to a workign state.

### Option 2: Re-write Existing Code

Take your existing research code and start over from scratch. This is similar to 
1 except you would be starting an entirely new file and building up the same 
functionality in a new package. You might consider this option if you wanted to
e.g., implement everything in Classes, but the old code is not written in such 
a way that it can be easily restructured in place.

Be sure to retain a copy of the original code for comparison. Consider incorporating
test functions in both versions so that you can tell if your new code behaves the same
as the old one.

### Option 3: Start a New Code

If you don't have research code that you are enthused about working on, consider 
writing something new from scratch. Here it will help to outline exactly what you
want your code to do before you set out, consider writing out a skeleton first and then filling 
in details after. 

If you are having trouble thinking about ideas for what you could work on, let me know
and we can discuss, I'm sure we can find something useful and interesting for you,
even if it only becomes a small toy problem, it's still helpful that it's connected to your
own research.
