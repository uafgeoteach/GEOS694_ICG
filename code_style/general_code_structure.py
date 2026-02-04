"""
Docstring describing what this function does, like an abstract. There are 
different ways to format this docstring, some of the weird formatting is so that
it works with documentation tools. You are welcome to format however you see fit


How to Use
    Here is how I call this code, its expected inputs and outputs:
    $ python do_stuff.py argument1 argument2

Caveats
    - What should I be aware of when running this code? 
    - That it will take a while?
    - That it will fail if my data are not in the correct order?

References
    1. This code was inspired by this code from over there
    2. The equation used in this function is from this book `Book Title`

Authors
    Me, myself, I
"""
import ...

CONSTANT = value


def do_stuff(x, y, z):
    """
    Docstring describing what do_stuff does

    See Reference 2 for the math used below

    :type x: what type is x supposed to be?
    :param x: what does x represent physically?
    :rtype: what type is returned
    :return: what does the returned value represent?
    """
    # doing some stuff, see ref. in docstring for math 
    out = x + y + z

    # doing some other stuff
    # ...

    # NOTE: When this function finishes, all of the variables inside are except
    # for those that are in the return
    return out


def other_function():
    #...
    return other stuff


def main():
    """
    This is the main body of the code, it takes all of the other things and
    puts them together. It does not have to be called mai
    """
    cool_variable = 5
    cooler_variable = 6
    coolest_variable = 7

    okay_variable = do_stuff(x=cool_variable, y=cooler_variable, 
                             z=coolest_variable)

    better_variable = do_stuff(x=okay_variable, y=cool_variable,
                               z=cooler_variable)

    # whatever else you need to do
    # ...

    print(better_variable)

    # Note that main does not return anything, this is the end of the program


if __name__ == "__main__":
    # Parameters defined in `main` go into the GLOBAL namespace (i.e., they
    # are retained throughout the entire script and may have downstream 
    # consequences)
    main()


