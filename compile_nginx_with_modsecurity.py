#!/usr/bin/python


from compile_nginx import *
from compile_modsecurity import *
from compile_pcre import *
from compile_utility import *
import argparse

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
        args = argparse.Namespace()

    #compile pcre
    if pcre:
        args.pcre = pcre
        args.prefix  = os.path.join(args.pcre, "build")
        compile_pcre(args)

    #compile modsecurity
    if modsecurity:
        args.modsecurity = modsecurity
        if pcre:
            args.pcre = os.path.join(args.prefix, "bin")
        args.enable_standalone_module = True
        compile_modsecurity(args)

    #compile nginx
    if nginx:
        args.nginx = nginx
        args.modsecurity = args.modsecurity
        args.pcre = args.pcre
        args.prefix = install_dir
        args.opt = " --with-http_ssl_module "
        compile_nginx(args)
    
    print("Compile Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compile nginx with modsecurity")
    parser.add_argument("--nginx", dest="nginx")
    parser.add_argument("--modsecurity", dest="modsecurity")
    parser.add_argument("--pcre", dest="pcre")
    parser.add_argument("--install_dir", dest="install_dir")

    args = parser.parse_args()
    compile_nginx_with_modsecurity(args)
