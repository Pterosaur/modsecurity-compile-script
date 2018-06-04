#!/usr/bin/python

import os
from compile_utility import *

def check_pcre(pcre_dir):
    import sys
    if not os.path.exists(pcre_dir):
        sys.stderr.write(pcre_dir + " not exists\n")
        return False
    if not os.path.exists(os.path.join(pcre_dir, "pcre_exec.c")):
        sys.stderr.write(pcre_dir + " may be not a right pcre directory\n")
        return False
    configure = os.path.join(pcre_dir, "configure")
    if not os.path.exists(configure):
        sys.stderr.write(configure + " not exists\n")
        return False
    return True

def compile_pcre_posix(args):
    pcre_dir = args.pcre_dir
    prefix = args.prefix
    pcre_dir = path_normalize(pcre_dir)
    if not check_pcre(pcre_dir):
        return
    #configure
    configure = "./configure"
    if prefix is None:
        prefix = pcre_dir + "/build"
        prefix = path_normalize(prefix)
        run("mkdir build", pcre_dir)
    else:    
        prefix = path_normalize(prefix)
    configure += " --prefix " + prefix
    run(configure, pcre_dir)

    #make -j
    run("make -j", pcre_dir)

    #make insatll
    run("make install", pcre_dir)

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
        parser.add_argument("--pcre_dir",dest="pcre_dir", default=os.getcwd())
        parser.add_argument("--prefix",dest="prefix")    
    #windows
    elif os.name == "nt":
        pass

    args =  parser.parse_args()        
    compile_pcre(args)