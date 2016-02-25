# -*- coding: utf-8 -*-
import os


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


def safe_list_get(l, idx, default):
    try:
        idx = int(idx)
        return l[idx]
    except Exception, e:
        print e
        return default
