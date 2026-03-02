# Lab 7: Bring Your Own Code (BYOC)

**Motivation:** In this lab you will have the opportunity to write or improve your own research codes with guidance. 
I offer a few approaches below, please pick the path that best suits your current needs.

## Instructions

1. Select one of the `Options` below.
2. Complete `Tasks` through implementation or reflection.
3. Get as far as you can during lab today and upload what you have to GitHub by the end of Lab.
4. I will provide comments/suggestions/feedback on your code via GitHub, you may leave question or comments 
throughout your code if you want me to focus on anything particular.


### Instructor Remarks
Take this as an opportunity to 1) try something that you don't think you will use outside of this class, 2) as an opportunity revisit code that you deem as "good enough" but could be cleaner, 3) as a chance to try out that new idea that you didn't think you would have time for. 

One of the the **assessment mechanisms** will be whether one of your 
classmates will be able to run and understand your code **without** any discussion with you. Keep that in mind as you work.


I will give opportunities in future labs/homeworks to continue working on this, so set yourself up for 
a multiple sessions of work. Ultimately I will grade the cumulative labs with the following rubric:

- 45% - Adherance to `Tasks` below
- 40% - Amount of new work (i.e., how much is different from start to finish)
- 15% - Accessibility (can your classmate, or me, run this without help?)


## Options

Please choose **one** of the following options to complete the `Tasks` below.

### Option #1: Modify Existing Code

Take your existing research code and improve it. 

Be sure to commit your code before you start making changes and provide me a link
to the commit where you started making your changes. Consider branch development
and committing small and often to ensure you can get back to a working state.

### Option #2: Re-write Existing Code

Take your existing research code and re-build it from scratch. 

You might consider this option if you have a mature code, but it is written in such 
a way that it cannot be easily restructured in place. Your final code does not have to 
be as fully featured as the original, but it should have similar basic characteristics.

Be sure to retain a copy of the original code for comparison. Consider incorporating
tests in both versions so that you can tell if your new code behaves the same as the old.

### Option #3: Start a New Code

If you don't have research code for #1 or #2, write something new from scratch. 

It will help to outline exactly what you want your code to do before you set out, consider 
writing out a skeleton first and then filling in details after. 

If you are having trouble thinking about ideas for what you could work on, let me know
and we can discuss.


## Tasks

Given the `option` you selected above, please complete the following tasks.

### Task 1: Implement **all** of the following in your code 

1. **PEP-8 Formatting**: Intuitive variable names, descriptive comments, elaboration where necessary, 
appropriate case (camel vs. snake), syntax, line limits etc.. Remember these are *guidelines*, not rules, **consistency** is the most important thing. If you stray from convention please reflect, in words, on why.
2. **Version Control (Local and Remote):** Commit small and often. Don't do 3 hours of work and then commit
one big change that says *"my changes"*. Work on one definable piece at a time and get into the habit of 
committing changes with reasonable commit messages before moving onto the next piece.
3. **Functions**: Think about the acronym DRY (*Don't Repeat Yourself*). Keep an eye out for: repeated code blocks, pieces of code that would benefit from isolation and organization, long winded runs of code.
4. **Documentation**: At a minimum, a doc-string at the top of your code explaining what the code does,
its inputs and outputs, and how to use the code. If you need more tools for explanation, like tables, figures, then consider a README file.
5. **Accessibility**: Anyone in our class should be able to look at your code and (without consulting with you) be able to understand what it does, download/install it, run an example, and evaluate whether or not it is "working". This may require having an example script, or example data, associated with the code.

### Task 2: Implement *at least* 1 of the following in your code 

For the other(s) that you do not implement, reflect on how you would implement it with words and pseudo code. Or, why you did not/would not implement.

> Note: "Not enough time", "too difficult" are not good reflections. Think about whether this would actually be useful in your research code. If you don't know whether it will be, take that as a challenge to try. 

6. **Classes**: Classes bundle data and functions. If you find yourself continually operating, accessing and modifying a set of data, or passing the same collection of input parameters between functions, then a class may be a useful abstraction. 
    - Note that your entire code does not have to be a Class. Like functions, Classes can abstract small independent units that are then utilized by the rest of the code.
7. **Parallel/Concurrency**: If your problem is parallelizable try to structure your code so that it leverages this. You do not have to use a complex package like `concurrent.futures` if you don't want to, you may also take the Bash script, Python subprocess, or multiple-terminal approach. Ensure that your documentation conveys the approach and use case clearly.

### Task 3: Implement *at least* 1 of the following in your code 

For the other(s) that you do not implement, reflect on how you would implement it with words and pseudo code. Or, why you did not/would not implement.

8. **Parameter Input System**: Most of our code can benefit from quick modifications from the user. Implement a parameter input system that allows for this, using any of the following (no `sys.argv`!): 
    - parameter file (e.g., .py, .txt, .json, .yaml, .toml)
    - argparser
    - input()
    > Note: This ties into (5) above, a random user needs to understand how they call your code and what each of the 
    parameters is, and whether their order, case, type is important. 
9. **State Saving**: Results saving and re-loading. We have not covered this in class yet, but
one way to make work faster and more reproducible is to build in capabilities to save results, and read them in
later, rather than re-process you data each time. You can use things like text files, domain specific file formats, 
binary files (.npy) etc. to do so. Create a system that allows you to save and re-load results or working state
to help speed up your research.
10. **Testing**: This can be as simple as checks throughout your code to ensure functions, code blocks, parameters, outputs, etc. behave as expected. You may use logic blocks, `assert` statements, try-except etc. A more advanced application of this would be to use a dedicated testing package like `unittest` or `Pytest`, which we have not covered (if you would like to go this route I can help you through). 
11. **Branching Development**: Use a branch to develop a feature and then merge it back into your main branch. This is especially useful if you have a code that works and you don't want to break existing functionality. Think of this as the version control approach of creating a copy of your file.
