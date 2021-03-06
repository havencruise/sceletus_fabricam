# -*- coding: utf-8 -*-
from fabric import colors
from fabric.api import env, sudo
from fabric.api import puts as fabric_puts
from fabric.context_managers import settings
from fabric.utils import abort

"""
Functions in this file are utilities that remove complexity from the
functions in lib.py.
"""

def puts(debug = None, info=None, success=None, warn=None, error=None):
    """
    Print a string in different colours
    """
    if debug:
        fabric_puts(colors.blue(debug))
    if info:
        fabric_puts(colors.cyan(info))
    elif success:
        fabric_puts(colors.green(success))
    elif warn:
        fabric_puts(colors.yellow(warn))
    elif error:
        fabric_puts(colors.red(error))

def check_on_path(binary):
    """
    Confirms that named binary is installed system-wide.

    """
    error_msg = "Please make sure you have installed `{binary}` " +\
                "or the path to `{binary}` is in $PATH"

    with settings(warn_only=True):
        if env.run("type '%s'" % binary).failed:
            abort(error_msg.format(binary = binary))

def create_directories(path, user, group=None, permission='0750'):
    """
    Create directories owned by the named user and group and with the
    given permissions
    """
    group = group or user

    if user == env.user:
        env.run("mkdir -p %s" % path)
    else:
        sudo("mkdir -p %s" % path)

    sudo("chown -R %s:%s %s" % (user, group, path))
    sudo("chmod -R %s %s" % (permission, path))

def activate_venv():
    """
    Returns a string that will activate the venv which can be used as a
    prefix to other commands
    """
    return "source %s/bin/activate" % env.virtualenv_dir
