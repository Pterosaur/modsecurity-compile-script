#!/usr/bin/python


from compile_nginx import *
from compile_modsecurity import *
from compile_pcre import *
from compile_utility import *

nginx = None
modsecurity = None
pcre = None
install_dir = None


def compile_nginx_with_modsecurity(args):
    global nginx
    global modsecurity
    global pcre
    global install_dir

    if args:
        if args.pcre:
            pcre = path_normalize(args.pcre)
        if args.modsecurity:
            modsecurity = path_normalize(args.modsecurity)
        if args.nginx:
            nginx = path_normalize(args.nginx)
        if args.install_dir:
            install_dir = args.install_dir
    else:
        class ARGS:
            pass
        args = ARGS()

    #compile pcre
    if pcre:
        args.pcre_dir = pcre
        args.prefix  = os.path.join(args.pcre_dir, "build")
        compile_pcre(args)

    #compile modsecurity
    if modsecurity:
        args.modsecurity_dir = modsecurity
        if pcre:
            args.pcre = os.path.join(args.prefix, "bin")
        args.enable_standalone_module = True
        compile_modsecurity(args)

    #compile nginx
    if nginx:
        args.nginx = nginx
        args.modsecurity = args.modsecurity_dir
        args.pcre = args.pcre
        args.prefix = install_dir
        compile_nginx(args)



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="compile nginx with modsecurity")
    parser.add_argument("--nginx", dest="nginx")
    parser.add_argument("--modsecurity", dest="modsecurity")
    parser.add_argument("--pcre", dest="pcre")
    parser.add_argument("--install_dir", dest="install_dir")

    args = parser.parse_args()
    compile_nginx_with_modsecurity(args)
