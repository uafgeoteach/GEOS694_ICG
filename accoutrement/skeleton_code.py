"""
Meta: This is an example of how you might structure your code when re-writing or
starting from scratch, it acts as a template or planning document from which
the rest of your code can follow

Description of why this file exists, what it will be used for, and any 
additional information required to understand it.

A rubric for how this code should be called or used in practice

    $ python skeleton_code.py fid modifier

Requirements: What packages do you need to install, any version conflicts?
"""
import sys
import matplotlib.pyplot as plt


def read_file(fid, expected_len=100):
    """
    Description of function, expected inputs, requirements for file structure
    Checks that output array is expected length

    Arguments:
        fid (str): file identifier for reading
    """
    return

    # To be written
    
    # Check appropriate file length
    assert(len(data) == expected_len), \
        f"file length inconsisten: {len(data)} != {expected_len}"
    return data


def do_stuff(data, modifier):
    """
    Description of what you want `do_stuff` to do and how it does it

    Arguments
        input_a (float): Description of input_a
        input_b (float): Description of input_b
    """
    return


    # To be written
    return output_a


def plot_stuff(data):
    """
    Description of what you want your plot to be

    Arguments:
        data (list): data array that has been modified
    """
    return

    # To be written
    plt.show()


def main():
    fid = sys.argv[1] 
    modifier = sys.argv[2]

    data = read_file(fid)
    modified_data = do_stuff(data, modifier)
    plot_stuff(modified_data)

if __name__ == "__main__":
    main()
