#!/usr/bin/env python3
import argparse
import paramiko
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('host', action='store', help='host to connect to')
parser.add_argument('-p', '--port', action='store', dest='port', default='22', help='port to connect to')
parser.add_argument('--known_hosts', action='store', dest='known_hosts', default='~/.ssh/known_hosts', help='known_hosts file')
args = parser.parse_args()

host = args.host
address = args.host+':'+args.port
known_hosts = os.path.expanduser(args.known_hosts)

if os.path.isfile(known_hosts) is False:
    open(known_hosts, 'w').close()

transport = paramiko.Transport(address)
transport.connect()
key = transport.get_remote_server_key()
transport.close()

print(dir(key))
print(f"Found fingerprint for {key.get_name()} key for {str(host)} of {str(key.get_fingerprint())}")
hostfile = paramiko.HostKeys(filename=known_hosts)
# if hostfile.check(hostname=host, key=key) is False:
#     print(f"Adding key to hostfile {known_hosts}")
    # hostfile.add(hostname=host, key=key, keytype=key.get_name())
    # hostfile.save(filename=known_hosts)
