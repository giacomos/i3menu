# -*- coding: utf-8 -*-
import os
import six


def which(program):
    """ check if an program exists and returns the path
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def safe_encode(string):
    """Safely unicode objects to UTF-8. If it's a binary string, just return
    it.
    """
    if isinstance(string, six.text_type):
        string = string.encode('utf-8')
    return string


def safe_decode(string):
    """Safely unicode objects to UTF-8. If it's a binary string, just return
    it.
    """
    if isinstance(string, six.string_types):
        return string
    return string.decode('utf-8')


def safe_join(lst, sep):
    try:
        return sep.join([safe_encode(e) for e in lst])
    except TypeError:
        return safe_decode(six.b(sep).join([safe_encode(e) for e in lst]))
