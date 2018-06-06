import os

def path_normalize(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    return path

def run(command, rundir = os.getcwd()):
    rundir = path_normalize(rundir)
    os.chdir(rundir)
    curdir = path_normalize(os.getcwd())
    ret = None
    if type(command) == str:
        ret = os.system(command)
    elif type(command) == list:
        ret = os.system(' '.join(command))
    os.chdir(curdir)
    return ret
