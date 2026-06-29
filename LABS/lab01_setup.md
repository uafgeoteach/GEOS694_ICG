





Lab Description:

This lab will get our personal computer setup for the rest of the semester, and start familiarizing you with tools that we will come back to constantly throughout the course.

Objectives

Make sure all students have the correct software for future homeworks and lab sections
Familiarize students with common tools used in geoscience research
Begin emphasizing flexibility in working style so that students can be adaptable in the course, and in their research

Instructions:

I provided general instructions but it is up to you to figure out how to complete the task, the internet is your friend here.
Some notes or tips are given in italic, some tasks have direct links to documentation.
If you get stuck anywhere or have questions: Google, ask your fellow classmates, ask me, ask AI tools (in that order!)
Don't just copy-paste, make sure you understand what you are doing.
These tasks will come up again and again in this class and in your research, so it's good to make sure you know why you're doing what you're doing.

Completion:

To show that you successfully completed the task there will be some sort of `proof` required such as copy-pasted text or a screenshot.
You can complete your assignment directly in the submission text box on Canvas
If a task asks for screenshots just embed those directly in the text box.
I suggest doing this in a separate text document (Google Doc, Word, etc.) and then copy-pasting into the submission box when you're done, so that you don't lose progress if Canvas refreshes. 




#	Task	Proof
1	

Text Editor

Text editors are great, I do half my coding in a text editor because it is fast and lightweight.
While Integrated Development Environments (IDE's, addressed in the later task) are much more powerful tools, they are not always easily accessible, e.g., on a remote environment
It is a good idea to be proficient with a text editor such that you have maximum flexibility in your working style.
Choose a terminal-based text editor of your choice, commonly available are: Vim, Emacs, Nano. 
Vim is powerful for doing major text editing, but has a steep learning curve
Vim is installed by default on most UNIX systems
Neovim is a more powerful version of Vim that allows plugins for customization/added capabilities.
I use Vim so I am biased, but I will also be able to help you the most if you use it.
> If you envision needing to write code on remote systems, I would suggest learning Vim.
Nano is easy to use and learn, but primarily a text editor.
Nano may or may not be installed on remote systems (it is available on Chinook)
If you just need to be able to quickly modify config files or make small updates to codes, Nano may be preferred.
> For those that mainly work on their own computer and on small codes, Nano may be preferable.
Emacs is like a self contained operating system where you are expected to always be working inside the program.
As a remote text editor I think it is just okay
Emacs is not always installed on remote systems (it is available on Chinook).
I have not used Emacs but it has a solid community.
If you use Emacs I'd be interested to hear what you like about it.
Online, search for a "cheatsheet" document for how to use this text editor (even if you're already experienced, you might learn something new!).  Save a PDF onto your computer for reference.
Figure out how to permanently enable a guide/line length marker in your text editor.
Set a guide/line length marker at 80 characters.
I like to keep all my codes at 80 character length, you can choose your preferred length but try to keep it <200
This value is arbitrary in modern coding, but historically stems from IBM punch cards which had a physical width of 80 columns

However the modern benefit is that you can easily view multiple codes side by side, and on small screens like phones.
With your text editor, create a new Python file with the following title: `GEOS694_<last_name>_HW1.py` (where <last_name> is your own last name)
Within this new file, write a "hello world" Python program and confirm that your guide is visible.
Take a screenshot of the file for `Proof`.
Exit the text editor while saving the file. Save the file somewhere accessible, you will need it for later tasks.

Optional:

What are some other ways you can customize your text editor to be more powerful?
Did you know about Vimdiff, where you can look at the differences between two files and edit them together using Vim?
	

Task: Embed a screenshot of the Python file you created, opened up in the text editor.

Reflection: What is something new on the cheatsheet that you didn't know you could do?


2	

Chinook and SSH

UAF's Chinook is a high performance computer (HPC) operated by the GI's Research Computing Services (RCS). It is open for all UAF staff/students/faculty to use.
For those that did not already have accounts, RCS has created accounts for you using your UA username. 
We want to ensure that we can successfully log in now so that we can use Chinook throughout the semester.
We'll also take this opportunity to streamline our SSH process, which should help when working on remote systems.

Note: We'll be doing work both on your [computer], and SSH'ed onto [Chinook]. I've tried to make it clear for each step where you should be working

Warning: Some of these tasks may have you running commands on your terminal, don't just copy-paste wildly, make sure you understand what you are running. If you are unsure, ask Google, your classmates, or your instructor!

[Computer] From your terminal program, SSH onto Chinook using your UA login and password. 
[Computer] Figure out how to create an SSH Config File so that you only need to run `ssh chinook` to login to Chinook.
An SSH Config File stores information regarding logging into remote systems (like your username, and the remote system's name).
This greatly simplifies logging into other systems by allowing you to write `ssh <system>` instead of `ssh -XY username@hostname`.
[Computer] Figure out how to set up `SSH keys` and set up SSH keys on Chinook.
SSH keys are a public-private key pair that you can use for logging into remote systems.
This simplifies logging into remote systems because you don't have to remember a password.
You don't have to attach a password to your private key
GitHub tutorial: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

In order to put your public key on Chinook, you should just have to run `ssh-copy-url chinook` from the terminal
[Chinook] Make a directory called `GEOS694` in your Chinook home directory
[Chinook] Using your preferred text editor, write a "hello world" Python program and save it to the GEOS694 directory.
[Computer] Fetch the "hello world" program from Chinook (using rsync, sftp, scp, etc.). 
	

From a fresh terminal, SSH into Chinook and run `cd GEOS694; ls`. Copy-paste the full terminal input/output to the submission text box.





3	

Conda Environment

Python is built on libraries. And libraries are built on other libraries. 
Individual libraries are constantly updating and changing, so only certain versions work together.
Package managers like Conda (also Pip, Poetry, uv) make sure that all these libraries play nicely with each other.

Conda vs. Mamba?

In geosciences, Conda (written in Python) has become the most popular package manager due to community backing.
User-developed software can be made available to install easily through public repositories like Conda-Forge. 
Mamba is a drop-in re-implementation of Conda in C++ that is much faster under-the-hood.
Anaconda/Mamba are full-fledged software that come pre-installed with thousands of scientific packages, a GUI etc., targeted at data scientists who want an all-in-one install.
Micromamba/Miniconda are stripped down to only contain the package manager, users are responsible for installing their own packages and managing their own environments.
In Geosciences, we prefer Micromamba/Miniconda because we are often downloading packages on our own, and often only use a handful of packages at once.
I will refer to this ecosystem as Conda, but I may be referring to either/or Conda/Mamba
> For first time users or people who want to start fresh, I suggest going with: Micromamba




Install Mamba or Conda on your own computer, if you don't already have it.
If you already have these installed, make sure they are up to date
Create a new `Conda` environment named `geos694` with Python 3.13
In your Conda config, set channel `conda-forge` above the default (https://conda-forge.org/docs/user/transitioning_from_defaults/)
The `defaults` channel of Conda are set by the Anaconda organization. They may be older than the latest available versions but are deemed more stable so that their Anaconda software always works.
`Conda-forge` is another "channel" to install software. It is community-driven and usually points to the most up to date versions of software. Python-based research software is usually hosted on `Conda-forge`.
Install the following packages to your `geos694` environment:
ObsPy
IPython
ipdb
	

List what version of Python, and which version of ObsPy, was installed in your environment.





4	

IDE (Integrated Development Environment)

IDE's are, aptly named, one-stop-shops for software development. The ideas that when developing, everything you need is contained in your IDE (e.g., built-in terminal, debugging, interfacing with GitHub, connecting to remote systems.)
At a minimum it is a fancy text editor with syntax highlighting, but...
At a maximum it can run your code as you write it to tell you where you're making mistakes, or where your code will fail, before you ever hit run.
With AI tool integration, IDE's can probably write an entire codebase for you with general prompting (i.e., "vibecoding").

Note:

In this class we'll use VSCode, but there are others (e.g., PyCharm, Spyder)
If you have a preferred IDE you are welcome to use that, but just note that if we do any IDE-specific tasks I'll be working from VSCode.

We will only take advantage of a limited amount of IDE capabilities, I leave it up to you to explore more if you are interested.
Download and install Visual Studio Code (VSCode), if you haven't already.
Open VSCode and figure out how to set a "ruler" at 80 character width
Figure out how to get VSCode to recognize and use your `GEOS694` Conda environment as the Python interpreter.
You may need to install the `Python` extension from the VSCode marketplace
To do so, in VSCode navigate from the top menu: Code -> Settings -> Extensions, and search Python. Click install
This will show you how to select the interpreter: https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment
In VSCode, write a program that prints a random number between 1 and 10 using NumPy's `random` module

Using VSCode's built-in terminal, run the Python script you just made.
	

Task: Embed a screenshot the entire IDE window which shows your program, the line ruler, and the output of your program in the built-in terminal.





5	

Git/GitHub

Version control helps us keep track of progress, turn back errors, and collaboratively develop software.
It is incredibly helpful for keeping track of the evolution of a code, working on code collaboratively, and sharing code. It means you don't have to keep track of files like: `my_thesis_code_1-12-26_v2_final_i-mean-it.py`
Git has dominated the landscape and is what we'll use in this class (others that exist: SVN, Subversion, Mercurial).
GitHub is the an online platform that interfaces with the Git version control software, but is not required to use Git.

Tip:

In this task you will clone a repository from GitHub. I like to keep all my Git repos in a central location on my computer, such as `~/REPOS`, to make it easier to find things.  You may find it useful to do the same. 

Ensure that you have Git on your computer. You can check if you do by running `git --version` in your terminal (Mac should have it by default).
If you don't have Git on your computer, install it.
Sign up for a GitHub account if you don't already have one: https://github.com/signup 
Set up SSH keys between your local computer and your GitHub account

On GitHub, fork the class repository to your personal GitHub account (Definition of forking)

Clone this forked repository to your own computer (Definition of cloning)
When you clone the repo, clone the SSH version, not the HTTPS version
If you're doing this from GitHub, after you click the green 'Clone' button, choose the 'SSH' tab 
On your computer, within this cloned repository, make a new directory called `HW1`
Move the files you made in Tasks 1 and 4 into the `HW1` repository
From your terminal, add, commit and push all these new files to your forked class repository, ensuring that your SSH keys are working as expected (i.e., you're not prompted for a password).
	Link to your personal GitHub account in the submission text box showing your forked repository and uploaded files in HW1 directory.
6	

Reflection

Please answer the following with a few words each. 

Was this lab easy, standard or difficult?
Approximately how long did you spend on the entire lab?
What, if any, tasks did you find the most difficult?
Did you learn anything new? 
Can this lab be updated or modified in any way to make things easier, or more challenging?
	Write down reflections in the submission text box.

Congrats! You're done.

Please submit the text and screenshot proof here on Canvas before next week's lab to get full points.

You may take off once you are done if you finish early, thanks!


