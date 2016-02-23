# -*- coding: utf-8 -*-
import os
import sys
import errno
import subprocess
import i18n

ROFI_PREFIX = '(i3-rofi)'

_ = i18n.language.gettext
DEFAULT_TITLE = _('Select:')


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
    if not idx:
        sys.exit()
    try:
        idx = int(idx)
        return l[idx]
    except IndexError:
        sys.exit(errno.EINVAL)
    except ValueError:
        sys.exit(errno.EINVAL)


def rofi(options, title=DEFAULT_TITLE, **kwargs):
    rofi_cmd = which('rofi')
    title = ' '.join([ROFI_PREFIX, title])
    safe_title = '"%s"' % title
    rofi_args = {'format': 'i'}
    rofi_args.update(kwargs)
    rofi_args_list = ['-dmenu', '-p', safe_title]
    for k,v in rofi_args.iteritems():
        rofi_args_list.append('-' + k)
        if isinstance(v, str):
            rofi_args_list.append(v)
        else:
            rofi_args_list.extend(list(v))
    cmd = 'echo "{options}" | {rofi} {rofi_args}'.format(
        rofi=rofi_cmd,
        rofi_args=' '.join(rofi_args_list),
        options='\n'.join(options),
        title=title,
    )
    proc = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    return proc.stdout.read().strip('\n')
