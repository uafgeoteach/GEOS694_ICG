# Lab 02: Code Refactoring

## Lab Description

This lab will have you hands-on working on refactoring a code — that is, restructuring an existing codebase to improve its readability, usability, and maintainability.

## Objectives

- Learn to identify inefficient or inaccessible coding practices and styles
- Begin thinking about how to resolve issues *before* making any changes
- Practice refactoring inefficient code, with an emphasis on debugging and code testing

## Instructions

- General instructions are provided, but it is up to you to figure out how to complete each task — the internet is your friend here.
- Consult the lecture slides, resources therein, and the associated Jupyter notebook.
- **Do not use AI tools or code completion software** — do this on your own to practice understanding these paradigms.

## Resources

The code in this lab focuses on UTM zones. For more background, see:

- [PEP-8 Style Guide](https://peps.python.org/pep-0008/)
- [General Python Code Structure](https://github.com/uafgeoteach/GEOS694_ICG/blob/main/WEEK2/general_code_structure.py)

## Completion

- You are expected to finish up to **Task 6** during lab. If you finish early, continue on until you're done or lab is released.
- Complete your assignment directly in the submission text box on Canvas.
- Put reflections and answers directly in the text box.
- Upload your refactored scripts to your `GEOS694` GitHub repo (naming and directory convention is up to you) and link to it at the bottom of your Canvas submission.

---

## Tasks

### Task 1 — Code Review

Navigate to the following code:
[`convert_utm2geo.py`](https://github.com/uafgeoteach/GEOS694_ICG/blob/main/WEEK2/convert_utm2geo.py)

Answer the following questions in the submission text box:

1. What does this code do?
2. How does this code do what it is meant to do? (i.e., what specific steps does it take?)
3. What are the inputs of the code?
4. What are the outputs of the code?

---

### Task 2 — Identify Style Inconsistencies

Scroll through the code and identify formatting or style inconsistencies, and describe how you would fix each one.

- Keep things **high-level** (e.g., *"import statements are within the main code body — move to the top"* rather than *"import math at line 260 should be at line 15"*).
- Point out line numbers or copy-paste code snippets as reference when flagging something specific.
- You only need to identify each issue **once**.

---

### Task 3 — Plan Your Refactor

In a few sentences (or as many as needed), describe the steps you would take to restructure this code to be easier to read and maintain.

Keep this **high-level** (e.g., *"rename variables, move this block here"*, etc.) — no code required yet.

---

### Task 4 — Run the Original Code

Copy the code into a new file on your computer and run it to determine the **UTM coordinates of Elvey Building**.

- You will need to figure out what **UTM zone** Fairbanks, AK is in.
- You should not need to download any external packages.

---

### Task 5 — Refactor a Simple Function (`_UTMLetterDesignator`)

1. Start a new script and copy-paste the function [`_UTMLetterDesignator`](https://github.com/uafgeoteach/GEOS694_ICG/blob/main/WEEK2/convert_utm2geo.py#L390-L437) into it.
2. Complete the script so that it can be run as a standalone Python program.
3. Verify the function behaves as expected (e.g., `Lat=8` returns the correct designation).
4. **Refactor** the function, focusing on making it concise, readable, and non-repeating.
5. Confirm that your refactored code produces the same behavior as the original.

---

### Task 6 — Refactor a Complicated Function (`UTMtoLL`)

1. Start a new script and perform the same steps as Task 5, but for the function [`UTMtoLL`](https://github.com/uafgeoteach/GEOS694_ICG/blob/main/WEEK2/convert_utm2geo.py#L440-L500).
2. To run this function in isolation, you may need to reference and copy from other parts of the original code.
3. Verify that your refactored version produces the **same results** as the original.
4. You may leave the math variable names as-is, but do ensure the math is laid out readably.

> **Optional:** For the motivated — the comments within the code point toward resources that may give you enough insight into the underlying math variables to make them more explanatory.

---

### Task 7 — Refactor the Main Body

Refactor the [main body of the code](https://github.com/uafgeoteach/GEOS694_ICG/blob/main/WEEK2/convert_utm2geo.py#L516-L567).

- Focus on improving the experience for a **new user** reading or using this code.
- You may keep the same input method (`sys.argv`) or try a different approach — Google around for alternatives.

---

### Task 8 — Refactor the Full Script

Refactor the remainder of the code, ensuring it provides the **same functionality** as the original.

- You may leave the internals of the remaining functions as-is, or lightly modified.
- The focus here is on **reorganizing the overall code flow**, not rewriting the math.

> **Optional:** For the motivated — take a crack at refactoring the main function `utm_geo`.