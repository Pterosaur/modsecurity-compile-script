#!/usr/bin/python

from compile_utility import *
import os
import sys

def check_modsecurity(modsecurity):
    if not os.path.exists(modsecurity):
        sys.stderr.write(modsecurity + " not exists\n")
        return False
    if not os.path.exists(os.path.join(modsecurity, "apache2/modsecurity.c")):
        sys.stderr.write(modsecurity + " may be not a right modsecurity directory\n")
        return False
    return True
    

def compile_modsecurity_posix(args):
    modsecurity = path_normalize(args.modsecurity)
    if not check_modsecurity(modsecurity):
        return
    #autogen.sh
    autogen = os.path.join(modsecurity, "autogen.sh")
    run(autogen, modsecurity)


    #configure
    configure = os.path.join(modsecurity, "configure")
    if hasattr(args, "enable_standalone_module") and args.enable_standalone_module:
        configure += " --enable-standalone-module "
    if hasattr(args, "pcre") and args.pcre:
        pcre = args.pcre
        pcre = path_normalize(pcre)
        pcre_config = os.path.join(pcre , "pcre-config")
        if not os.path.exists(pcre_config):
            sys.stderr.write(pcre_config + " not exists\n")
            return
        configure += " --with-pcre="+pcre
    if hasattr(args, "opt") and args.opt:
        configure += args.opt
    
    run(configure, modsecurity)

    #make clean
    run("make clean", modsecurity)

    #make -j
    run("make -j", modsecurity)


def compile_modsecurity(args):
    #unix
    if os.name == "posix":
        compile_modsecurity_posix(args)
    #windows
    elif os.name == "nt":
        pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="compile modsecurity")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--modsecurity", dest="modsecurity", default=os.getcwd())
    parser.add_argument("--pcre",dest="pcre", help="the directory of pcre-config")
    #unix
    if os.name == "posix":
        parser.add_argument("--enable-standalone-module",dest="enable_standalone_module", action="store_true")    
    
    args =  parser.parse_args()       
    import compile_utility
    compile_utility.verbose = args.verbose     
    compile_modsecurity(args)
