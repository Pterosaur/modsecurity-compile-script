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

def run(command, rundir = os.getcwd()):
    rundir = path_normalize(rundir)
    
    print "******************************************"
    print "command      : %s"%(command,)
    print "cwd          : %s"%(rundir,)


    if type(command) == str:
        command = [command]
    
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=rundir, shell=True)
    if not popen:
        return (-1, None)
    output = popen.communicate()
    return_code = popen.wait()

    if verbose:
        print "\nstdout       : "
        print "\n".join(map(lambda line : "+ " + line, output[0].split('\n')))

    if output[1]:
        print "stderr       : "
        sys.stderr.write("\n".join(map(lambda line : "> " + line, output[1].split('\n'))) + "\n")

    print "recturn code : %s" % (return_code,)
    print "******************************************\n"
    if return_code != 0:
        raise ValueError("%s : %s (%s)" % (rundir, command, return_code))
    return (return_code, output[0])
