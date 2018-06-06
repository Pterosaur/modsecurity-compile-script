#!/usr/bin/python

import os
import stat
from compile_utility import *

def check_pcre(pcre):
    import sys
    if not os.path.exists(pcre):
        sys.stderr.write(pcre + " not exists\n")
        return False
    if not os.path.exists(os.path.join(pcre, "pcre_exec.c")):
        sys.stderr.write(pcre + " may be not a right pcre directory\n")
        return False

    return True

def compile_pcre_posix(args):
    pcre = args.pcre
    prefix = args.prefix
    pcre = path_normalize(pcre)
    if not check_pcre(pcre):
        return False
    #configure
    configure = os.path.join(pcre, "configure")
    if prefix is None:
        prefix = os.path.join(pcre,"build")
        prefix = path_normalize(prefix)
        run("mkdir build", pcre)
    else:    
        prefix = path_normalize(prefix)
    configure += " --prefix " + prefix
    if not check_output(run(configure, pcre)):
        return False
    
    #make -j
    if not check_output(run("make -j", pcre)):
        return False

    #make insatll
    if not check_output(run("make install", pcre)):
        return False
    
    return True


def compile_pcre(args):
    #unix
    if os.name == "posix":
        return compile_pcre_posix(args)
    #windows
    elif os.name == "nt":
        pass
    sys.stderr.write('error platform \n')
    return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="compile pcre")
    parser.add_argument("--verbose", action="store_true")
    #unix
    if os.name == "posix":
        parser.add_argument("--pcre",dest="pcre", default=os.getcwd())
        parser.add_argument("--prefix",dest="prefix")    
    #windows
    elif os.name == "nt":
        pass

    args =  parser.parse_args()     
    import compile_utility
    compile_utility.verbose = args.verbose
    compile_pcre(args)