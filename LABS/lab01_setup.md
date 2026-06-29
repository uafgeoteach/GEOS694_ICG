# Lab 01: Environment Setup

## Lab Description

This lab will get your personal computer set up for the rest of the semester, and start familiarizing you with tools that we will come back to constantly throughout the course.

## Objectives

- Make sure all students have the correct software for future homeworks and lab sections
- Familiarize students with common tools used in geoscience research
- Begin emphasizing flexibility in working style so that students can be adaptable in the course, and in their research

## Instructions

- General instructions are provided, but it is up to you to figure out how to complete each task — the internet is your friend here.
- Some notes or tips are given in *italic*; some tasks have direct links to documentation.
- If you get stuck anywhere or have questions: Google → ask your fellow classmates → ask me → ask AI tools (in that order!)
- **Don't just copy-paste** — make sure you understand what you are doing.
- These tasks will come up again and again in this class and in your research, so it's important to know *why* you're doing what you're doing.

## Completion

- To show that you successfully completed each task, some form of `proof` is required (copy-pasted text or a screenshot).
- Complete your assignment directly in the submission text box on Canvas.
- If a task asks for screenshots, embed them directly in the text box.
- *Suggested:* Write your answers in a separate document (Google Doc, Word, etc.) and copy-paste into the submission box when done, so you don't lose progress if Canvas refreshes.

---

## Task 1 — Text Editor

Text editors are great for fast, lightweight coding. While IDEs (addressed in Task 4) are more powerful, they are not always accessible — e.g., on a remote environment. Being proficient with a terminal-based text editor gives you maximum flexibility in your working style.

### Choosing a Text Editor

Choose a terminal-based text editor. Commonly available options are:

- **Vim** — Powerful for major text editing, but has a steep learning curve. Installed by default on most UNIX systems. *If you envision needing to write code on remote systems, I would suggest learning Vim.*
  - **Neovim** is a more powerful variant of Vim that supports plugins for customization and added capabilities.
- **Nano** — Easy to use and learn, but primarily a text editor. May or may not be installed on remote systems (it is available on Chinook). *For those who mainly work on their own computer and on small codes, Nano may be preferable.*
- **Emacs** — Like a self-contained operating system where you are expected to always be working inside the program. Not always installed on remote systems (it is available on Chinook). Has a solid community — if you use Emacs, I'd be interested to hear what you like about it.

### Steps

1. Search online for a **cheatsheet** for your chosen text editor (even if you're already experienced — you might learn something new!). Save a PDF to your computer for reference.
2. Figure out how to **permanently enable a guide/line length marker** in your text editor.
   - Set the guide at **80 characters**.
   - 80 characters is arbitrary in modern coding, but historically stems from IBM punch cards, which had a physical width of 80 columns. The modern benefit is that you can easily view multiple files side by side, and on small screens.
   - You can choose your own preferred length, but try to keep it under 200.
3. Create a new Python file named `GEOS694_<last_name>_HW1.py` (replacing `<last_name>` with your own last name).
4. Within that file, write a **"Hello World"** Python program and confirm that your guide/ruler is visible.
5. **Take a screenshot** of the file open in the text editor.
6. Exit the text editor while saving the file. Save it somewhere accessible — you will need it for later tasks.

### Optional

- What are some other ways you can customize your text editor to be more powerful?
- Did you know about **Vimdiff**, where you can compare two files and edit them together using Vim?

### Proof Required

- **Screenshot:** The Python file you created, open in your text editor.
- **Reflection:** What is something new on the cheatsheet that you didn't already know how to do?

---

## Task 2 — Chinook and SSH

UAF's **Chinook** is a high-performance computer (HPC) operated by the GI's Research Computing Services (RCS), open to all UAF staff, students, and faculty. We want to ensure you can successfully log in now so we can use Chinook throughout the semester.

> **Note:** Some steps below are performed on your **[Computer]**, and some while SSH'd into **[Chinook]**. Each step is labeled accordingly.
>
> **Warning:** Some tasks involve running terminal commands. Don't copy-paste blindly — make sure you understand what you are running. If unsure, ask Google, your classmates, or your instructor.

### Steps

1. **[Computer]** SSH into Chinook using your UA login and password.
2. **[Computer]** Set up an **SSH Config File** so that you only need to run `ssh chinook` to log in.
   - An SSH Config File stores connection information (username, hostname, etc.), so instead of typing `ssh -XY username@hostname` every time, you can just type `ssh <system>`.
3. **[Computer]** Set up **SSH keys** on Chinook.
   - SSH keys are a public-private key pair that allow you to log into remote systems without a password.
   - You do not have to attach a password to your private key.
   - Reference: [GitHub SSH key setup guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
   - To copy your public key to Chinook, run `ssh-copy-id chinook` from your terminal.
4. **[Chinook]** Create a directory called `GEOS694` in your Chinook home directory.
5. **[Chinook]** Using your preferred text editor, write a **"Hello World"** Python program and save it to the `GEOS694` directory.
6. **[Computer]** Fetch the "Hello World" program from Chinook using `rsync`, `sftp`, `scp`, or similar.

### Proof Required

From a fresh terminal, SSH into Chinook and run:

```bash
cd GEOS694; ls
```

Copy-paste the full terminal input and output into the submission text box.

---

## Task 3 — Conda Environment

Python is built on libraries, and libraries are built on other libraries. Individual libraries are constantly updating, so only certain versions work together. Package managers like **Conda** (and alternatives like Pip, Poetry, uv) ensure all these libraries play nicely with each other.

### Conda vs. Mamba

| Tool | Description |
|---|---|
| **Conda** | Most popular package manager in geosciences; community software available via Conda-Forge |
| **Mamba** | A C++ re-implementation of Conda that is significantly faster |
| **Anaconda / Mamba** | Full-featured software with thousands of pre-installed packages and a GUI; targeted at data scientists who want an all-in-one install |
| **Micromamba / Miniconda** | Stripped-down versions containing only the package manager; users install their own packages |

> **Recommendation for new users:** Start with **Micromamba**.

### Steps

1. **Install Mamba or Conda** on your computer if you don't already have it. If you already have it, make sure it is up to date.
2. Create a new Conda environment named `geos694` with **Python 3.13**:
   ```bash
   conda create -n geos694 python=3.13
   ```
3. In your Conda config, set the `conda-forge` channel above the default channel.
   - Reference: [Transitioning from Conda defaults to conda-forge](https://conda-forge.org/docs/user/transitioning_from_defaults/)
   - The `defaults` channel is maintained by Anaconda and prioritizes stability. `conda-forge` is community-driven and typically offers the most up-to-date versions of scientific software.
4. Install the following packages into your `geos694` environment:
   - `ObsPy`
   - `IPython`
   - `ipdb`

### Proof Required

List the version of **Python** and the version of **ObsPy** installed in your environment.

---

## Task 4 — IDE (Integrated Development Environment)

IDEs are one-stop-shops for software development — everything you need is in one place (built-in terminal, debugging, GitHub integration, remote system connections, etc.). At a minimum, an IDE is a fancy text editor with syntax highlighting. At a maximum, it can run your code as you write it to catch errors before you even hit run.

> **Note:** In this class we'll use **VSCode**, but others exist (e.g., PyCharm, Spyder). If you have a preferred IDE you're welcome to use it, but note that IDE-specific tasks will be demonstrated from VSCode.

### Steps

1. Download and install **[Visual Studio Code (VSCode)](https://code.visualstudio.com/)** if you haven't already.
2. Open VSCode and set a **ruler at 80 character width**.
3. Configure VSCode to recognize and use your `geos694` Conda environment as the Python interpreter.
   - You may need to install the **Python extension** from the VSCode marketplace: `Code → Settings → Extensions`, search "Python", and click Install.
   - Reference: [Selecting a Python interpreter in VSCode](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment)
4. In VSCode, write a program that prints a **random number between 1 and 10** using NumPy's `random` module.
5. Run the script using VSCode's **built-in terminal**.

### Proof Required

**Screenshot:** The entire IDE window showing your program, the line ruler, and the output in the built-in terminal.

---

## Task 5 — Git / GitHub

Version control helps you track progress, revert errors, and collaboratively develop software. It means you never have to manage files named things like `my_thesis_code_1-12-26_v2_final_i-mean-it.py`.

- **Git** is the dominant version control system (others: SVN, Subversion, Mercurial).
- **GitHub** is an online platform that interfaces with Git, but is not required to use Git.

> **Tip:** Keep all your Git repositories in a central location such as `~/REPOS` to make them easier to find.

### Steps

1. Ensure you have **Git** installed. Check by running:
   ```bash
   git --version
   ```
   *(Mac should have it by default. If not, install it.)*
2. **Sign up for a GitHub account** if you don't already have one: [github.com/signup](https://github.com/signup)
3. Set up **SSH keys** between your local computer and your GitHub account.
4. On GitHub, **fork** the class repository to your personal GitHub account. ([What is forking?](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo))
5. **Clone** your forked repository to your computer. ([What is cloning?](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository))
   - When cloning, use the **SSH** version (not HTTPS): click the green "Code" button on GitHub, then choose the "SSH" tab.
6. Inside your cloned repository, create a new directory called `HW1`.
7. Move the files you made in **Tasks 1 and 4** into the `HW1` directory.
8. From your terminal, **add, commit, and push** all new files to your forked repository, confirming that your SSH keys are working (i.e., you are not prompted for a password).

### Proof Required

Link to your personal GitHub account showing your forked repository and the uploaded files in the `HW1` directory.

---

## Task 6 — Reflection

Please answer the following with a few words each:

1. Was this lab **easy, standard, or difficult**?
2. Approximately **how long** did you spend on the entire lab?
3. Which tasks, if any, did you find the **most difficult**?
4. Did you **learn anything new**?
5. Can this lab be **updated or modified** to make things easier or more challenging?

### Proof Required

Write your reflections in the submission text box.

---

## Submission Checklist

| # | Task | Proof |
|---|---|---|
| 1 | Text Editor | Screenshot of Python file in editor + reflection on cheatsheet |
| 2 | Chinook and SSH | Copy-pasted terminal output of `cd GEOS694; ls` |
| 3 | Conda Environment | Python version + ObsPy version |
| 4 | IDE | Screenshot of full IDE window with code, ruler, and terminal output |
| 5 | Git/GitHub | Link to your forked GitHub repository with `HW1` files |
| 6 | Reflection | Written responses in submission text box |

**Congrats — you're done!** Please submit your text and screenshot proof on Canvas before next week's lab. You may leave once you are finished if you complete this early.