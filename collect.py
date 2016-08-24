#! /usr/bin/env python


import sys
import os
import paramiko


def run(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()
    return stdout.read()


if __name__ == '__main__':
    devices = sys.argv[1].split(',') if len(sys.argv) >= 2 else []
    username = sys.argv[2] if len(sys.argv) >= 3 else 'cumulus'
    password = sys.argv[3] if len(sys.argv) >= 4 else 'CumulusLinux!'

    # Create directories
    for device in devices:
        try:
            os.makedirs('roles/autonet/files/%s/network'%device)
            os.makedirs('roles/autonet/files/%s/quagga'%device)
            os.makedirs('roles/autonet/files/%s/cumulus'%device)
        except os.error:
            pass

    # Log into each device and collect network and quagga information
    for device in devices:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(device, username=username, password=password)

        # Figure out all the files we're gonna hit
        files = "/etc/network:\n"
        files += run(ssh, 'ls -pR1 /etc/network')
        files += "\n"
        files += "/etc/quagga:\n"
        files += run(ssh, 'ls -pR1 /etc/quagga')
        files += "\n"
        files += "/etc/cumulus:\n"
        files += run(ssh, 'ls -pR1 /etc/cumulus')
        files += "\n"

        current_dir = ''
        for l in files.splitlines():
            l = l.strip()
            if l.endswith(':'):
                current_dir = l.split(':')[0]
            elif l and not l.endswith('/'):
                content = run(ssh, "cat %s/%s"%(current_dir, l))
                try:
                    os.makedirs('roles/autonet/files/%s/%s'%(device, current_dir.split('etc', 1)[-1]))
                except os.error:
                    pass
                with file('roles/autonet/files/%s/%s/%s'%(device, current_dir.split('etc', 1)[-1], l), 'w') as f:
                    f.write(content)
