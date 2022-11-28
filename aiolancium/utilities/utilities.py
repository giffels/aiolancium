from functools import partial


def get_method_name(arg):
    while isinstance(arg, partial):
        arg = arg.args[0]
    return arg
