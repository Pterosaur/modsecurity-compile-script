#!/usr/bin/python

import os
from compile_utility import *

def check_pcre(pcre):
    import sys
    if not os.path.exists(pcre):
        sys.stderr.write(pcre + " not exists\n")
        return False
    if not os.path.exists(os.path.join(pcre, "pcre_exec.c")):
        sys.stderr.write(pcre + " may be not a right pcre directory\n")
        return False
    configure = os.path.join(pcre, "configure")
    if not os.path.exists(configure):
        sys.stderr.write(configure + " not exists\n")
        return False
    return True

def compile_pcre_posix(args):
    pcre = args.pcre
    prefix = args.prefix
    pcre = path_normalize(pcre)
    if not check_pcre(pcre):
        return
    #configure
    configure = "./configure"
    if prefix is None:
        prefix = os.path.join(pcre,"/build")
        prefix = path_normalize(prefix)
        run("mkdir build", pcre)
    else:    
        prefix = path_normalize(prefix)
    configure += " --prefix " + prefix
    run(configure, pcre)

    #make -j
    run("make -j", pcre)

    #make insatll
    run("make install", pcre)

def compile_pcre(args):
    #unix
    if os.name == "posix":
        compile_pcre_posix(args)
    #windows
    elif os.name == "nt":
        pass

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="compile pcre")
    #unix
    if os.name == "posix":
        parser.add_argument("--pcre",dest="pcre", default=os.getcwd())
        parser.add_argument("--prefix",dest="prefix")    
    #windows
    elif os.name == "nt":
        pass

    args =  parser.parse_args()        
    compile_pcre(args)