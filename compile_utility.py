import os
import subprocess
import sys

def path_normalize(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    path = os.path.normcase(path)
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    return path

verbose = False

def check_output(output):
    if output[0] != 0:
        if not verbose:
            print output[1]
        return False
    return True

def run(command, rundir = os.getcwd()):
    rundir = path_normalize(rundir)
    
    if verbose:
        print "\n******************************************"
        print "command      : %s"%(command,)
        print "cwd          : %s"%(rundir,)


    if type(command) == str:
        command = [command]
    
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=rundir, shell=True)
    if not popen:
        return (-1, None)
    output = popen.communicate()
    return_code = popen.wait()

    if output[1] or verbose:
        if verbose:
            print "stderr       : "
        sys.stderr.write(output[1] + "\n")
    if verbose:
        print "recturn code : %s" % (return_code,)
        print "stdout       : "
        print output[0]
        print "******************************************\n"
    return (return_code, output[0])
