#!/usr/bin/python

import sys
import pexpect
import re
import os

def execute_remote_command(args):
    if not args.remote_username \
        or not args.remote_password \
        or not args.remote_address \
        or not args.remote_command:
        return False
    command = "ssh %s@%s '%s'" % \
        (args.remote_username, args.remote_address, args.remote_command)
    child = pexpect.spawn(command)
    #first login 
    #Are you sure you want to continue connecting (yes/no)?
    try:
        child.expect('yes',timeout=1)
        child.sendline("yes")
    except:
        pass
    #input password
    #remote_username@remote_address's password:
    try:
        child.expect('password', timeout = 1)
        child.sendline(args.remote_password)
    except:    
        sys.stderr.write(command + ' error\n')
        return False
    buffer = child.read()
    return buffer

def record_data(args, raw_data):

    #Failed request
    failed_request = re.search("Failed requests\D*(\d+)", raw_data)
    if not failed_request:
        sys.stderr.write("Format error : " + raw_data+"\n")
        return False
    failed_request = int(failed_request.group(1))
    # if failed_request > 0:
    #     sys.stderr.write("Failed request : " + failed_request +"\n")
    #     return False
    print "Failed request:" + str(failed_request)

    #Request per second
    request_per_second = re.search("Requests per second\D*([\d.]+)", raw_data)
    if not request_per_second:
        sys.stderr.write("Format error : " + raw_data+"\n")
        return False
    request_per_second = float(request_per_second.group(1).strip())
    print "Request per second: " + str(request_per_second)

    #Latency
    time_per_request = re.search("", raw_data)
    
    return True

def modify_timeout_check_interval(args, number):
    if os.name == "posix":
        from compile_nginx_with_modsecurity import compile_nginx_with_modsecurity
        compile_nginx_with_modsecurity(args)
        from compile_utility import run, path_normalize
        run("pkill nginx")
        nginx_execute = os.path.join(args.install_dir, "sbin/nginx")
        path_normalize(nginx_execute)
        run(nginx_execute)

def execute_testing(args):
    modify_timeout_check_interval(args, 1)
    raw_data = execute_remote_command(args)
    print raw_data
    if args.raw_data_file:
        raw_data_file = open(args.raw_data_file, "a+")
        raw_data_file.write(raw_data + "\n")
    # record_data(args, raw_data)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="test pcre timeout performance")
    parser.add_argument("--remote_username", dest="remote_username")
    parser.add_argument("--remote_password", dest="remote_password")
    parser.add_argument("--remote_address", dest="remote_address")
    parser.add_argument("--remote_command", dest="remote_command")
    parser.add_argument("--nginx", dest="nginx")
    parser.add_argument("--modsecurity", dest="modsecurity")
    parser.add_argument("--pcre", dest="pcre")
    parser.add_argument("--install_dir", dest="install_dir")
    parser.add_argument("-o", dest="raw_data_file")
    

    args = parser.parse_args()
    execute_testing(args)
















