"""
Examples of different ways to do parameter input in Python
"""
import argparse
import sys
import yaml
import matplotlib.pyplot as plt
import numpy as np


def plot_cosx(dx, color, legend):
    """
    This is the functional form of what I am calling in the examples below. 
    However some require modifications so the code is copy-pasted for clarity.
    args
        dx (float): step value for X axis
        color (str): color of the line
        legend (bool): show legend
    """
    x = np.arange(-2 * np.pi, 2 * np.pi, dx)
    y = np.cos(x)
    plt.plot(x, y, c=color, label="sin(x)")
    if legend:
        plt.legend()
    plt.show()

def plot_cosx_force_type(dx, color, legend):
    """
    args
        xmin (float): minimum x value
        xmax (float): maximum x value
        color (str): color of the line
        legend (bool): show legend
    """
    x = np.arange(-2 * np.pi, 2 * np.pi, float(dx))
    y = np.cos(x)
    plt.plot(x, y, c=str(color), label="sin(x)")
    if bool(legend):
        plt.legend()
    plt.show()
1

"""
Sys.argv is simple and easy to implement, but is rigid and requires good 
documentation since order and length of input arguments is enforced. Also it is
not really easy to differentiate parameter types, so you have to do that in your
code directly which can be visually cluttered
"""
def sys_argv():
    """Classic sys.argv requires converting strings to required input types"""
    dx = float(sys.argv[1])
    color = str(sys.argv[2])
    legend = bool(int(sys.argv[3]))
    
    plot_cosx(dx, color, legend)

def sys_argv_alternative():
    """Python allows for dynamic list expansion in the input statement"""
    import ipdb;ipdb.set_trace()
    plot_cosx_force_type(*sys.argv[1:])


"""
input() allows user input at specific points in the code. Similarly the sys.argv
it is inflexible in type, and also introduced a failure point in your code, 
i.e., the user accidentally types the wrong input and errors the code. It is
also more difficult to script and automate. However it is helpful for code 
that requires specific prompting.
"""
def input_strategy():
    x = np.arange(-2 * np.pi, 2 * np.pi, 
                  float(input("Value of `dx` for sin?: ")))
    y = np.cos(x)
    color = str(input("color of string?: "))
    plt.plot(x, y, c=str(color), label="sin(x)")

    legend = input("plot legend?: ")
    if bool(legend):
        plt.legend()
    plt.show()


"""
argparser is Python's more advanced argument parser that allows for a lot of
control and flexibility over input parameters. As soon as you need lots of
options, type enforcement, help messages etc., consider going for argparser.
"""
def plot_cosx_multi(f, dx, color, legend):
    """
    This is the functional form of what I am calling in the examples below. 
    However some require modifications so the code is copy-pasted for clarity.
    args
        f (list): list of frequency multipliers
        dx (float): step value for X axis
        color (str): color of the line
        legend (bool): show legend
    """
    x = np.arange(-2 * np.pi, 2 * np.pi, dx)
    for f_ in f:
        y = np.cos(f_ * x)
        plt.plot(x, y, c=color, label="sin(x)")
    if legend:
        plt.legend()
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description="Plot a sine wave")
    parser.add_argument("-f", "--frequencies", type=float, nargs="+",
                        required=True, help="frequencies to plot for sin waves")
    parser.add_argument("-d", "--discretization", default=.01, type=float,
                        nargs="?", help="discretization of the X axis")
    parser.add_argument("-c", "--color", default="r", type=str, nargs="?",
                        help="color of the line")
    parser.add_argument("-l", "--legend", default=False, action="store_true",
                        help="turn on the legend")
    
    return parser


def argparser_strategy():
    """Argparser with some catches incase no arguments given"""
    parser = parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()

    f = args.frequencies
    dx = args.discretization
    c = args.color
    l = args.legend

    plot_cosx_multi(f, dx, c, l)


"""
Parameter files are useful when you have a lot of parameter that might not 
change often. Or if you want a way to maintain a record of input parameters, 
or if you have complicated input data. There are multiple ways of doing input
files, some common ones are 1) text files, 2) JSON, 3) YAML, 4) TOML
"""

def yaml_strategy():
    with open("example_input.yaml", "r") as f:
        params = yaml.load(f, Loader=yaml.SafeLoader)
    breakpoint()

    plot_cosx_multi(**params)

def py_strategy():
    from example_input import f, c, dx, l

    plot_cosx_multi(f, dx, c, l)



if __name__ == "__main__":
    # sys_argv()
    # sys_argv_alternative()
    # input_strategy()
    # argparser_strategy()
    # yaml_strategy()
    py_strategy()
