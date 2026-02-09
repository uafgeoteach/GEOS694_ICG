# LAB 4: Classes in Python
UAF GEOS694: Introduction to Computational Geosciences  
Bryant Chow

### Description
This lab will give you a chance to work with Classes to practice the mechanics of writing them, and understanding how they may be used in a research context. For this lab we will look at USGS stream gauge data and build a Python class around it to help us analyze this data.

### Instructions
- For visual clarity I break the lab into main tasks with sub-tasks below. 
- Each sub-task may build on previous tasks so don't skip around.
- `TO DO TASK ?` are the reflection questions you will submit on Canvas, you will not submit any figures.
- You will be asked to upload your code to GitHub so practice readability through proper code formatting and style (PEP-8)
- Ask for help from your classmates, google/stackoverflow, me, ChatGPT (in that order) if needed.
- Get as far as you can in Lab session, I will not ask you to proceed further unless you want to.

### Context

Imagine you are a UAF geoscience graduate student (difficult, I know), and your advisor has tasked you
with analyzing all USGS stream gauges in Alaska to understand water throughput during a recent storm. If succesful, this may expand to looking at all storms in the historical record. You foresee that this will not just be a one-off, and decide this is a perfect opportunity to try out Classes and object oriented programming concepts you learned about in class. 


## Task 1: Stream gauge Data

In this task we will read and plot our example data so we can see what we are working with:

1. Download the example stream gauge data from GitHub (`phelan_creek_stream_gauge_2024-09-07_to_2024-09-14.txt`). 
-    You can `Download Raw File` button directly from GitHub, no need to pull from GitHub.  
2. Use VSCode or a text editor to view the data file and understand what it shows you.
3. In a new script file named `streamgauge.py`, copy-paste the function `read_gauge_file()` below
4. Write the remainder of the code to read in the gauge date, place this under under `if _name__ == "__main__":`
5. Write a new function `plot` that plots the gauge data, call this under the main code you wrote in (4)
6. Create a figure of the plotted data   

> **NOTE**: *I could have asked you to write the function yourselves, but since this lab is focused on creating classes, I wrote it ahead of time so you can spend time doing more important things. And so that you are all working from the same data.*

```python
import numpy as np

def read_gauge_file(fid):
    """
    Read USGS gauge data and convert date and time to minutes since start

    parameters
    fid (str): path to data

    returns
    timestamp (list): ???
    hgt (np.array): gauge height in ft
    """
    date, time, hgt = np.loadtxt(fid, skiprows=28, usecols=[2,3,5], 
                                    dtype=str).T

    hgt = hgt.astype(float)
    days = [float(d[-2:]) for d in date]  # get DD from YYYY-MM-DD
    hours = [float(t.split(":")[0]) for t in time]  # get HH from HH:MM
    mins = [float(t.split(":")[1]) for t in time]  # get MM from HH:MM

    timestamps = []
    for d, h, m in zip(days, hours, mins):
        timestamp = (d * 24 * 60) + (h * 60) + m
        timestamps.append(timestamp)

    return timestamps, hgt
```

### TO DO TASK 1  
a. Look at the code and figure out what the values in the X-axis represent (i.e., units, relative to what?).   
- Add that descriptor to the functions docstring `timestamp`    
- Add the appropriate label to your plot function   

b. Looking at the figure, what are the time and data values associated with the largest amplitude? (rough values, this doesn't have to be exactly precise)

## Task 2: Class

The script we have now is great and for all intents and purposes does what we want it to. But we know that we will have to look at, and modify, lots of stream gauge data, so we want to build a structure around the data, with methods to match. In Python we want to build a Class.

1. In the same script file, create a new `class` called `Streamgauge`
2. Inside the new class write the `__init__` contructor which set the following attributes:  
    a. Data File ID (`fid`)  
    b. Station ID  (`station_id`)  
    c. Station Name  (`station_name`)  
    d. Start Time  (`starttime`)  
    e. Data file ID (`fid`)  
3. Establish the following `Class attributes`:   
    a. `time=[]`   
    b. `data=[]`  
    c. `units='ft'`
4. Modiying your existing `read_gauge_file()` function, create a new method `Streamgauge().read_gauge_file`:
    - Remember that you can access the file id through `self.fid`
    - Instead of `return` at the end of the function, have the function populate, or append to, `time` and `data`
5. Modifying your existing `plot()` function, create a new method `Streamgauge().plot()` that plots the `time` and `data` attributes. 
    - `Streamgauge.plot()` should take no inputs.
    - `Streamgauge.plot()` should dynamically create a title with the relevant information referenced from the attributes, in other words, have the title say something like:  
    `Stream gauge <SITE NO> <SITE NAME> <START TIME> <MAX HEIGHT> <gauge UNIT>`
6. Copy the following code block to the bottom of your file and make sure that your script can successfully evaluate it when you call   
`$ python streamgauge.py`:
    ```python
    if __name__ == "__main__":
        fid = "phelan_creek_stream_gauge_2024-09-07_to_2024-09-14.txt"
        sg = Streamgauge(fid=fid, station_id="15478040", 
                         station_name="PHELAN CREEK", starttime="2024-09-07 00:00")
        assert(len(sg.data) == 0)  # check that we haven't read data yet
        
        sg.read_gauge_file()
        assert(len(sg.time) == len(sg.data))  # check that data and time are equal

        sg.plot()
    ```

### TO DO TASK 2

**Reflection**  
a. What is the max gauge height shown on your figure?  
b. At this point do you think its worth the additional overhead of dealing with a class?  (Your answer can be 'no' or 'I don't think so')  
c. Can you think of a way you can simplify the code in (6) based on what's in the data file? (don't implement, just discuss)


## Task 3: More Behavior

In geosciences we often want to do more than read and plot raw data, we want to acquire some information about our signal or do some processing. In a Class, we can do that through implementation of new methods. 

1. Write a method `Streamgauge().convert()` that converts the data array from units of **feet** to units of **meters**. 
    - Be sure it modifies the class attribute `units`, too!
2. Write a method `Streamgauge().demean()` that subtracts the mean value of the data array from the data array
3. Write a method `Streamgauge().shift_time()` that offsets the time axis by a user-input amount of minutes.
4. Make sure that your class can evaluate the following code block, and that the output plot has the modifications that you have made  
    ```python
    if __name__ == "__main__":
        sg = Streamgauge(fid, "15478040", "PHELAN CREEK", "2024-09-07 00:00", "ft")  
        sg.read_gauge_file()   
        sg.plot()   

        sg.convert()   
        sg.demean()   
        sg.shift_time(-100)
        sg.plot()   
    ```

### TO DO TASK 3
**Reflection**: 
- How would you improve on the code block in (4) to make things more accesible, easier to read, after you walk away from it for a year. Think about ways to reduce the manual burden of looking through the whole codebase or typing on a keyboard to figure out what this code is doing. You don't have to do it, just discuss in a few sentences.

## Task 4: Debugging Classes

Debugging classes is the same as in normal scripting, you can use `breakpoint()` OR `import ipdb; ipdb.set_trace()` (for more functionality) to stop the code mid-run and inspect the code state. Let's run the debugger inside the class to see how this works.

1. In your source code, put a debugger call at the **top** of the function `Streamgauge().covert()` 
2. Convert should have access to `data`, from inside the debugger determine the 20th entry of the array, write it down?
3. Exit the debugger and now put a debugger call at the **bottom** of the function `Streamgauge().convert()`
4. Note down the 20th entry of the array()
5. Still in the debugger, run the `plot()` command, make note of whether the time is shifted or not.

### TO DO TASK 4
**Reflection:**
- Are the values different between what you got in (2) and (4)
- What did you have to do to access the object `data` and method `plot` from inside the class? 
- Do you use the Python debugger (or similar) when you are coding?

## Task 5: Scaling

The beauty of classes and object oriented programming is that they are designed to scale (whereas scripts often require re-tooling to do so). Now that you have got this to work on a single data set, your advisor has asked that you scale up to multiple stream gauges. Lucky for you, you're ready for it.

1. Define a function `Streamgauge.main()` that implements the processing and plotting steps in `Task 3.4`
2. Copy the file `phelan_creek_stream_gauge_2024-09-07_to_2024-09-14.txt` to a new file named `phelan_creek_stream_gauge_2024-10-07_to_2024-10-14.txt`
3. In the new file, making the following modifications. Don't do this manually! Vim, Nano, VSCode have ways modify multiple lines at once.
- Data Array (`1755_0065`): Add a leading 1 (e.g., 47.94 -> 147.94)
- Time Array (`datetime`): Change the month to 10 (2024-09-07 -> 2024-10-07)
4. Add the following code block to the bottom of your script and finish the code, make sure it runs:

```python
if __name__ == "__main__":
    for fid in [...]:  # fill in
        Streamgauge(...).main()  # fill in
```

### TO DO TASK 5
**Reflection:** 
Your advisor asks you to do a different processing scheme where you don't convert the data, oh and also another one where you only time shift by -50. But also make sure you can still do this processing step!   
    a. How would you approach this if you were not using classes (i.e., just scripting).   
    b. Describe what you would modify in your `Streamgauge` Class to accomplish all these different things? You can write pseudocode if it is easier.  
    c. Does one approach or the other feel easier to manage?  


## Task 6: Inheritance

Now let's say you have a specific subset of stream gauges from a different agency (e.g., NOAA). In this hypothetical example NOAA stream gauges output units of meters, which affects a lot of the assumptions you make throughout the code, and has some consequences for downstream behavior. You need to find a way to use the same class definition, but adjust for USGS vs NOAA stream gauges.

1. Answer reflection question (a)
2. In the same script, create a new class `NOAAStreamgauge` and have it inherit from `Streamgauge`
3. Overwrite the class attribute `units` so that it is in the correct units of the NOAA stream gauge.
4. Overwrite the function `convert` so that it does nothing when called.
5. Re-define the function `read_gauge_file()` 
- Use the `super()` functionality to call the previous behavior of `Streamgauge`
- After the `super()` call, have the function `NOAAStreamgauge.read_gauge_file()` modify the functionality by printing ("I am a NOAA stream gauge"). 
- Remember that the boilerplate for this looks like:
    ```python
    class Child(Parent):
        def function(self):
            super().function()
            # ...additional functionality goes here
    ```
6. Modify the code block you wrote in `Task 5.4` and see that you get the behavior you want, if you swap out `Streamgauge` for `NOAAStreamgauge`

### TO DO TASK 6
**Reflections**  
    a. How would you implement this change in your class definition (without inheritance), assuming every function needs to be modified.  
    b. What behavior were you expecting in 6?   
    c. Write some pseudocode to define how the code after `if __name__ == "__main__":` block would operate if you were mixing USGS and NOAA stream gauges. Try to make it as concise as possibe.  
    d. Do you think that your implementation in (a) would be better or worse in terms of readability, maintenance, future use, as compared to the approach with inheritance? 

---

### TO DO FINAL  
1. Submit all lab reflections to Canvas submission box  
2. Final reflection (in submission box, too):  
    a. Was this lab easy, standard or difficult?  
    b. Approximately how long did you spend on the entire lab?  
    c. Can this lab be updated or modified in any way to make things easier, or more challenging?  
    d. General feedback if you have any.
3. Upload your `streamgauge.py` file to your course GitHub page.  


