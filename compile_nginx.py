#!/usr/bin/python

import os
import sys
from compile_utility import *

def check_nginx(nginx):
    import sys
    if not os.path.exists(nginx):
        sys.stderr.write(nginx + " not exists\n")
        return False
    
    if not os.path.exists(os.path.join(nginx, "src/core/nginx.c")):
        sys.stderr.write(nginx + " may be not a right nginx directory\n")
        return False

    return True


def compile_nginx(args):
    nginx = path_normalize(args.nginx)
    
    if not check_nginx(nginx):
        return False
    
    #make clean
    try:
        run("make clean", nginx)
    except:
        pass

    #configure
    configure = os.path.join(nginx, "configure")
    ld_opt = ""
    cc_opt = ""

    if hasattr(args, "modsecurity") and args.modsecurity:
        modsecurity = args.modsecurity
        modsecurity = os.path.join(modsecurity, "nginx/modsecurity")
        modsecurity = path_normalize(modsecurity)
        configure += " --add-module="+modsecurity

    if hasattr(args, "prefix") and args.prefix:
        prefix = args.prefix
        prefix = path_normalize(prefix)
        configure += " --prefix="+prefix
    
    if hasattr(args, "pcre") and args.pcre:
        pcre_config = os.path.join(args.pcre, "pcre-config")
        pcre_config = path_normalize(pcre_config)
        import subprocess
        if not os.path.exists(pcre_config):
            sys.stderr.write(pcre_config + " not exists\n")
            return
        pcre_prefix = path_normalize(subprocess.check_output([pcre_config, "--prefix"]).strip())

        if not pcre_prefix.startswith("/usr"):
            pcre_lib = os.path.join(pcre_prefix, "lib")
            run("mkdir -p nginx_linker_dir/", pcre_lib)
            try:
                run("cp * nginx_linker_dir/", pcre_lib)
            except:
                pass
            pcre_link = os.path.join(pcre_lib, "nginx_linker_dir")    
            #TODO more gracefule 

            # remove softlinker
            run("rm $(find . -regex './libpcre.so')", pcre_link)
            # mv libpcre.so.1.x to libpcre.so.1
            run("mv $(find . -regex './libpcre.so.[0-9].+') $(find . -regex './libpcre.so.[0-9]')", pcre_link)
            
            #TODO more gracefule 
            
        else:
            pcre_link = os.path.join(pcre_prefix, "lib")

        pcre_lib = "-L"+pcre_link+" -lpcre"
        # pcre_lib = subprocess.check_output([pcre_config, "--libs"]).strip()
        
        pcre_include = os.path.join(pcre_prefix, "include")

        ld_opt += pcre_lib
        ld_opt += " -Wl,-rpath="+pcre_link
        cc_opt += "-I"+pcre_include
        configure += " --with-pcre "

    if ld_opt:
        configure += " --with-ld-opt=\""+ld_opt+"\" "
    if cc_opt:
        configure += " --with-cc-opt=\""+cc_opt+"\" "

    if hasattr(args, "opt") and args.opt:
        configure += args.opt


    run(configure, nginx)

    #make -j
    run("make -j", nginx)
    #make install
    run("make install", nginx)

    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="compile nginx")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--nginx", dest="nginx",default=os.getcwd())
    parser.add_argument("--modsecurity", dest="modsecurity", help="the directory of modsecurity")
    parser.add_argument("--pcre", dest="pcre", help="the directory of pcre-config")
    parser.add_argument("--prefix", dest="prefix", help="nginx install directory")
    
    args = parser.parse_args()
    import compile_utility
    compile_utility.verbose = args.verbose
    compile_nginx(args)
